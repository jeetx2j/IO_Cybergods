import cv2
import numpy as np
import csv
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the TensorFlow Face model
model = load_model('face_model.h5')

# Load the known faces and their corresponding names
known_faces = []
known_face_names = []
face_labels = []

with open('realtime_immage.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        image_path = row[0]
        name = row[1]
        image = cv2.imread(image_path)
        image = cv2.resize(image, (160, 160))  # Resize to 160x160 for TensorFlow Face
        image = image / 255.0  # Normalize pixel values to [0, 1]
        known_faces.append(image)
        known_face_names.append(name)
        face_labels.append(len(known_face_names) - 1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(known_faces, face_labels, test_size=0.2, random_state=42)

# Train the TensorFlow Face model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Initialize the video capture object
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = []
    for face_location in face_locations:
        x, y, w, h = face_location
        face_image = rgb_small_frame[y:y+h, x:x+w]
        face_image = cv2.resize(face_image, (160, 160))  # Resize to 160x160 for TensorFlow Face
        face_image = face_image / 255.0  # Normalize pixel values to [0, 1]
        face_encodings.append(face_image)

    for face_encoding in face_encodings:
        # Use the trained TensorFlow Face model to predict the face label
        predictions = model.predict(face_encoding.reshape(1, 160, 160, 3))
        face_label = np.argmax(predictions)

        # Get the corresponding face name
        name = known_face_names[face_label]
        print(f"Recognized {name}!")

        # Mark attendance
        current_time = datetime.now().strftime("%H:%M:%S")
        with open('attendance.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([name, current_time])

    cv2.imshow('Attendance System', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()