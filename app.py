import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import io

from database import (
    init_db,
    add_student,
    get_students,
    add_attendance,
    get_today_attendance,
    is_attendance_marked
)
from face_utils import encode_face, detect_and_recognize_faces

# Initialize database
init_db()

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----- Helper Function -----
def process_attendance(image):
    students = get_students()
    if not students:
        st.error("No students registered.")
        return

    recognized, unrecognized = detect_and_recognize_faces(image, students)

    st.subheader("Results")
    st.write(f"✅ Recognized Students: {len(recognized)}")
    st.write(f"❌ Unrecognized Faces: {unrecognized}")

    for roll in recognized:
        if not is_attendance_marked(roll, datetime.now().date()):
            add_attendance(roll, "Present")
            st.success(f"Attendance marked for {roll}")
        else:
            st.info(f"Attendance already marked for {roll} today")


# ----- Sidebar -----
st.sidebar.title("Attendify")
st.sidebar.markdown("**Team: Teen Titans**")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Admin Login", "Register Student", "Mark Attendance", "Dashboard", "Export Attendance"]
)

# ----- Pages -----
if page == "Home":
    st.title("Attendify – Smart AI Attendance System")
    st.markdown(
        """
Welcome to **Attendify**! This AI-powered app automatically marks attendance using face recognition from a single group photo.

### Features
- Register students with face samples
- Mark attendance from a group photo
- View & export attendance reports

Use the sidebar to navigate.
        """
    )

elif page == "Admin Login":
    st.title("Admin Login")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if password == "admin123":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Incorrect password.")

elif page == "Register Student":
    if not st.session_state.logged_in:
        st.error("Please log in as admin first.")
    else:
        st.title("Register Student")

        name = st.text_input("Name")
        roll = st.text_input("Roll No")
        branch = st.text_input("Branch")
        year = st.text_input("Year")

        option = st.radio("Capture Face", ["Webcam", "Upload Image"])

        if st.button("Register Student"):
            if not name or not roll or not branch or not year:
                st.error("Please fill all details before registering.")
            else:
                if option == "Webcam":
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        st.error("Webcam not found.")
                    else:
                        ret, frame = cap.read()
                        cap.release()
                        if ret:
                            encoding = encode_face(frame)
                            if encoding is not None:
                                add_student(name, roll, branch, year, encoding)
                                st.success("Student registered successfully!")
                            else:
                                st.error("No face detected in the image.")

                elif option == "Upload Image":
                    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
                    if uploaded_file is not None:
                        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                        image = cv2.imdecode(file_bytes, 1)

                        encoding = encode_face(image)
                        if encoding is not None:
                            add_student(name, roll, branch, year, encoding)
                            st.success("Student registered successfully!")
                        else:
                            st.error("No face detected in the image.")
                    else:
                        st.warning("Upload an image first.")

elif page == "Mark Attendance":
    if not st.session_state.logged_in:
        st.error("Please log in as admin first.")
    else:
        st.title("Mark Attendance")

        option = st.radio("Take Photo", ["Webcam", "Upload Image"])

        if option == "Webcam":
            if st.button("Capture Group Photo"):
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    st.error("Webcam not found.")
                else:
                    ret, frame = cap.read()
                    cap.release()
                    if ret:
                        process_attendance(frame)

        elif option == "Upload Image":
            uploaded_file = st.file_uploader("Upload Group Photo", type=["jpg", "png"])
            if uploaded_file is not None:
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, 1)
                process_attendance(image)

elif page == "Dashboard":
    if not st.session_state.logged_in:
        st.error("Please log in as admin first.")
    else:
        st.title("Attendance Dashboard")
        attendance = get_today_attendance()

        if attendance:
            df = pd.DataFrame(attendance, columns=["Name", "Roll", "Branch", "Year", "Date", "Time", "Status"])

            st.subheader("Today's Attendance")
            st.dataframe(df)
            st.write(f"✅ Total Present Today: {len(df)}")

            st.subheader("Filter Attendance")
            branch_filter = st.selectbox("Filter by Branch", ["All"] + sorted(df["Branch"].unique()))
            year_filter = st.selectbox("Filter by Year", ["All"] + sorted(df["Year"].unique()))

            filtered_df = df.copy()
            if branch_filter != "All":
                filtered_df = filtered_df[filtered_df["Branch"] == branch_filter]
            if year_filter != "All":
                filtered_df = filtered_df[filtered_df["Year"] == year_filter]

            st.dataframe(filtered_df)
        else:
            st.info("No attendance marked today.")

elif page == "Export Attendance":
    if not st.session_state.logged_in:
        st.error("Please log in as admin first.")
    else:
        st.title("Export Attendance")
        attendance = get_today_attendance()

        if attendance:
            df = pd.DataFrame(attendance, columns=["Name", "Roll", "Branch", "Year", "Date", "Time", "Status"])

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Attendance")
            buffer.seek(0)

            st.download_button(
                "Download Excel",
                buffer,
                "attendance.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.info("No attendance to export.")
