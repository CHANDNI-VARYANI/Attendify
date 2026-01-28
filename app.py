import streamlit as st
import face_recognition
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Attendify", layout="centered")
st.title("📸 Attendify - Smart AI Attendance System")

STUDENTS_FOLDER = "Students"

known_encodings = []
known_names = []

# Load registered students
for file in os.listdir(STUDENTS_FOLDER):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        img = face_recognition.load_image_file(
            os.path.join(STUDENTS_FOLDER, file)
        )
        enc = face_recognition.face_encodings(img)
        if enc:
            known_encodings.append(enc[0])
            known_names.append(file.split(".")[0])

st.success(f"Registered Students: {known_names}")

uploaded_file = st.file_uploader("Upload Group Photo", type=["jpg","jpeg","png"])

if uploaded_file:
    group_img = face_recognition.load_image_file(uploaded_file)
    group_locations = face_recognition.face_locations(group_img)
    group_encodings = face_recognition.face_encodings(group_img, group_locations)

    present = []

    for face in group_encodings:
        matches = face_recognition.compare_faces(known_encodings, face)
        if True in matches:
            name = known_names[matches.index(True)]
            present.append(name)

    absent = [name for name in known_names if name not in present]

    st.success("Attendance Marked")

    st.write("### Present Students")
    st.write(present)

    st.write("### Absent Students")
    st.write(absent)

    attendance = []
    for name in known_names:
        if name in present:
            attendance.append([name, "Present"])
        else:
            attendance.append([name, "Absent"])

    df = pd.DataFrame(attendance, columns=["Name","Status"])
    st.dataframe(df)

    filename = f"attendance_{datetime.now().date()}.csv"
    df.to_csv(filename, index=False)

    with open(filename,"rb") as f:
        st.download_button("Download Attendance CSV", f, file_name=filename)

