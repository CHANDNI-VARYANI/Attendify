import streamlit as st
from deepface import DeepFace
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Attendify", layout="centered")
st.title("📸 Attendify - Smart AI Attendance System")

STUDENTS_FOLDER = "Students"

# Load student faces
known_encodings = []
known_names = []

for file in os.listdir(STUDENTS_FOLDER):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        img = face_recognition.load_image_file(
            os.path.join(STUDENTS_FOLDER, file)
        )
        enc = face_recognition.face_encodings(img)
        if enc:
            known_encodings.append(enc[0])
            known_names.append(file.split(".")[0])

uploaded_file = st.file_uploader("Upload Group Photo", type=["jpg","jpeg","png"])

if uploaded_file:

    present = []
    absent = []

    image = face_recognition.load_image_file(uploaded_file)
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

present = []
absent = []

for face_encoding in face_encodings:
    matches = face_recognition.compare_faces(known_encodings, face_encoding)
    if True in matches:
        matched_index = matches.index(True)
        name = known_names[matched_index]
        if name not in present:
            present.append(name)

for name in known_names:
    if name not in present:
        absent.append(name)


    st.success("Attendance Marked")
    st.write("Present:", present)
    st.write("Absent:", absent)

    attendance = []
    for name in known_names:
        if name in present:
            attendance.append([name, "Present"])
        else:
            attendance.append([name, "Absent"])

    df = pd.DataFrame(attendance, columns=["Name","Status"])
    st.success("Attendance Marked Successfully")
    st.dataframe(df)

    filename = f"attendance_{datetime.now().date()}.csv"
    df.to_csv(filename, index=False)

    with open(filename, "rb") as f:
        st.download_button("Download Attendance CSV", f, file_name=filename)




