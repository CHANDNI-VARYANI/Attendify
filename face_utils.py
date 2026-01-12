import face_recognition
import cv2
import numpy as np

def encode_face(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    if face_locations:
        encodings = face_recognition.face_encodings(rgb_image, face_locations)
        return encodings[0]  # Return the first encoding
    return None

def detect_and_recognize_faces(image, students):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    
    recognized = set()
    unrecognized = 0
    
    known_encodings = [data["encoding"] for data in students.values()]
    known_rolls = list(students.keys())
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
        if True in matches:
            first_match_index = matches.index(True)
            recognized.add(known_rolls[first_match_index])
        else:
            unrecognized += 1
    
    return list(recognized), unrecognized