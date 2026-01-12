# Attendify – Smart AI Attendance System

## Overview
Attendify is an AI-powered attendance system that uses face recognition to mark attendance from a single group photo. Built for hackathons, it features student registration, automatic attendance marking, and exportable reports.

## Tech Stack
- Python
- OpenCV
- face_recognition (dlib)
- Streamlit
- SQLite
- pandas
- openpyxl (for Excel export)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`
3. Access at http://localhost:8501

## Features
- Admin login (password: admin123)
- Register students with face capture/upload
- Mark attendance from webcam or uploaded group photo
- Dashboard with filters
- Export attendance to Excel (.xlsx)

## Notes
- Ensure webcam is available for capture.
- Face recognition uses dlib; may require additional setup on some systems (e.g., install dlib dependencies).
- Attendance is marked only once per day per student.
- Export generates a proper Excel file.