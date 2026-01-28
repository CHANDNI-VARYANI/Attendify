import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Attendify", layout="centered")
st.title("📸 Attendify - Smart AI Attendance System")

# Registered Students (database simulation)
students = ["Chandni","Gargi","Himakshi","Jhanvi","Khooshbu"]

st.success(f"Registered Students: {students}")

uploaded = st.file_uploader("Upload Group Photo", type=["jpg","jpeg","png"])

if uploaded:
    st.image(uploaded, caption="Uploaded Group Photo")

    st.info("AI Processing...")

    # Simulated recognition (demo)
    present = students[:3]   # first 3 present
    absent = students[3:]

    st.success("Attendance Marked")

    st.write("### Present Students")
    st.write(present)

    st.write("### Absent Students")
    st.write(absent)

    attendance = []
    for s in students:
        if s in present:
            attendance.append([s,"Present"])
        else:
            attendance.append([s,"Absent"])

    df = pd.DataFrame(attendance, columns=["Name","Status"])
    st.dataframe(df)

    filename = f"attendance_{datetime.now().date()}.csv"
    df.to_csv(filename, index=False)

    with open(filename,"rb") as f:
        st.download_button("Download Attendance CSV", f, file_name=filename)

