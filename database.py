import sqlite3
import json
import numpy as np
from datetime import datetime

DB_NAME = "attendify.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    roll TEXT PRIMARY KEY,
                    name TEXT,
                    branch TEXT,
                    year TEXT,
                    encoding TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll TEXT,
                    date TEXT,
                    time TEXT,
                    status TEXT,
                    FOREIGN KEY (roll) REFERENCES students(roll)
                )''')
    conn.commit()
    conn.close()

def add_student(name, roll, branch, year, encoding):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    encoding_str = json.dumps(encoding.tolist())
    c.execute("INSERT OR REPLACE INTO students (roll, name, branch, year, encoding) VALUES (?, ?, ?, ?, ?)",
              (roll, name, branch, year, encoding_str))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT roll, name, branch, year, encoding FROM students")
    rows = c.fetchall()
    conn.close()
    students = {}
    for row in rows:
        roll, name, branch, year, encoding_str = row
        encoding = np.array(json.loads(encoding_str))
        students[roll] = {"name": name, "branch": branch, "year": year, "encoding": encoding}
    return students

def add_attendance(roll, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now()
    date = now.date().isoformat()
    time = now.time().isoformat()
    c.execute("INSERT INTO attendance (roll, date, time, status) VALUES (?, ?, ?, ?)",
              (roll, date, time, status))
    conn.commit()
    conn.close()

def is_attendance_marked(roll, date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM attendance WHERE roll = ? AND date = ?", (roll, date.isoformat()))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_today_attendance():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    today = datetime.now().date().isoformat()
    c.execute("""
        SELECT s.name, s.roll, s.branch, s.year, a.date, a.time, a.status
        FROM attendance a
        JOIN students s ON a.roll = s.roll
        WHERE a.date = ?
    """, (today,))
    rows = c.fetchall()
    conn.close()
    return rows