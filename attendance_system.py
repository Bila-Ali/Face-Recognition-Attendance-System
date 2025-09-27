import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import csv

# Path to the folder containing student images
STUDENTS_FOLDER = 'students'

# Initialize lists to store face encodings and names of known students
known_face_encodings = []
known_face_names = []

# Load student images and generate face encodings
for filename in os.listdir(STUDENTS_FOLDER):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(STUDENTS_FOLDER, filename)
        try:
            img_bgr = cv2.imread(img_path)
            if img_bgr is None:
                print(f"[Error] Could not load image: {filename}")
                continue

            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(img_rgb)

            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                name = os.path.splitext(filename)[0].replace("_", " ").title()
                known_face_names.append(name)
                print(f"Loaded and encoded face for: {name}")
            else:
                print(f"[Warning] No face found in: {filename}")

        except Exception as e:
            print(f"[Error] Could not process image {filename}: {e}")

# Initialize a copy of the known student names for attendance tracking
students_present = known_face_names.copy()

# Get the current date for the attendance CSV filename
now = datetime.now()
csv_filename = now.strftime("%Y-%m-%d") + '_attendance.csv'

# Open the attendance CSV file in write mode
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Name', 'Timestamp'])

    # Start webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Cannot open webcam")
        exit()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                if name in students_present:
                    now = datetime.now()
                    timestamp = now.strftime("%H:%M:%S")
                    csv_writer.writerow([name, timestamp])
                    students_present.remove(name)
                    print(f"Attendance marked for {name} at {timestamp}")

            # Draw rectangle and label
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        cv2.imshow('Attendance System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

print("Attendance marking complete. Check the CSV file.")
