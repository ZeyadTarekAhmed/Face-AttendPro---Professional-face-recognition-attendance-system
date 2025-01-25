import cv2
import numpy as np
import face_recognition
import os
import requests
from datetime import datetime

running = False  # Global variable to control face recognition process

# Telegram Bot Function to send message with more detailed response
def send_telegram_message(chat_id, message):
    bot_token = ''  # Replace with your bot's token
    url = ""
    payload = {'chat_id': chat_id, 'text': message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Message sent successfully: {response.json()}")
        else:
            print(f"Error sending message: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred while sending message: {e}")

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("Face not found in one of the images. Skipping...")
    return encodeList

recorded_students = {}

def markAttendance(name):
    now = datetime.now()
    dateString = now.strftime('%Y-%m-%d')
    timeString = now.strftime('%H:%M:%S')

    if name not in recorded_students or recorded_students[name] != dateString:
        with open('Attendance.csv', 'a') as f:
            f.writelines(f'\n{name},{dateString},{timeString}')
            print(f"{name} سجل الحضور في {dateString} {timeString}")

        if name == "ZEYAD TAREK":
            message = "Hi Zeyad, Your Attendance in DSP lecture has been marked."
            send_telegram_message('', message)
        elif name == "SARA HESHAM":
            message = "Hi Sara, Your Attendance in DSP lecture has been marked."
            send_telegram_message('', message)
        elif name == "AHMED SIEF ELESLAM":
            message = "Hi Ahmed, Your Attendance in DSP lecture has been marked."
            send_telegram_message('', message)
        elif name == "AHMED MOHAMED SALAH":
            message = "Hi Ahmed, Your Attendance in DSP lecture has been marked."
            send_telegram_message('', message)
        elif name == "ARWA SAAD":
            message = "Hi Arwa, Your Attendance in DSP lecture has been marked."
            send_telegram_message('', message)

        recorded_students[name] = dateString

def recognize_and_mark_attendance():
    global running
    running = True
    path = 'images'
    images = []
    classNames = []

    myList = os.listdir(path)
    print(f"Images found: {myList}")

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(f"Class names: {classNames}")

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
    else:
        print("Camera opened successfully.")

    frame_resizing = 0.25

    while running:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture image")
            break

        imgS = cv2.resize(img, (0, 0), fx=frame_resizing, fy=frame_resizing)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(f"Recognized: {name}")

                markAttendance(name)

                faceLoc = np.array(faceLoc)
                faceLoc = faceLoc / frame_resizing
                faceLoc = faceLoc.astype(int)

                y1, x2, y2, x1 = faceLoc[0], faceLoc[1], faceLoc[2], faceLoc[3]

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        key = cv2.waitKey(1)
        if key == 27 or not running:
            break

    cap.release()
    cv2.destroyAllWindows()

def stop_recognition():
    global running
    running = False
