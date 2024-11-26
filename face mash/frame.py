import cv2
import mediapipe as mp
import face_recognition
import numpy as np
import time
import pickle

# تنظیمات MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def capture_and_store_encodings():
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot access webcam.")

    print("Please rotate your head in different directions (up, down, left, right) to capture all angles.")

    face_encodings = []
    total_landmarks = 10000  # تعداد کل نقاط صورت در مدل FaceMesh
    landmarks_scanned = 0  # تعداد نقاطی که اسکن شده‌اند
    scan_complete = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Face Recognition: شناسایی چهره و انکدینگ
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # MediaPipe Face Mesh: رسم مش
        mesh_results = face_mesh.process(rgb_frame)
        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                # رسم دایره دور صورت
                x_values = [landmark.x for landmark in face_landmarks.landmark]
                y_values = [landmark.y for landmark in face_landmarks.landmark]
                min_x, max_x = min(x_values), max(x_values)
                min_y, max_y = min(y_values), max(y_values)
                center_x = int((min_x + max_x) * frame.shape[1] / 2)
                center_y = int((min_y + max_y) * frame.shape[0] / 2)
                radius = int(max(max_x - min_x, max_y - min_y) * frame.shape[0] / 2)

                # رسم دایره سبز که به تدریج پر می‌شود
                circle_color = (0, 255, 0) if landmarks_scanned >= total_landmarks else (0, 0, 255)
                cv2.circle(frame, (center_x, center_y), radius, circle_color, 2)

                # رنگ‌آمیزی سبز برای نقاطی که اسکن شده‌اند
                for i, landmark in enumerate(face_landmarks.landmark):
                    if 0 < landmark.x < 1 and 0 < landmark.y < 1:
                        landmarks_scanned += 1
                        cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 2,
                                   (0, 255, 0), -1)

                # وضعیت اسکن شدن تمام صورت
                if landmarks_scanned >= total_landmarks:
                    scan_complete = True
                    cv2.putText(frame, "Face fully scanned!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    # ذخیره انکودینگ‌ها
                    if encodings:
                        face_encodings.append(encodings[0])

        # راهنمایی برای حرکت سر
        if not scan_complete:
            cv2.putText(frame, "Move your head slowly to complete the circle", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # نمایش فریم
        cv2.imshow("Face Enrollment", frame)

        # اگر کاربر کلید 'q' را فشار دهد یا تعداد کافی از زوایا ثبت شود
        if cv2.waitKey(1) & 0xFF == ord('q') or scan_complete:
            if len(face_encodings) > 10:  # می‌توان تعداد انکودینگ‌ها را با توجه به تعداد زوایا تنظیم کرد
                print("Enough angles captured. Saving data...")
                break

    # ذخیره داده‌ها
    if face_encodings:
        avg_encoding = np.mean(face_encodings, axis=0)
        with open("saved_face.pkl", "wb") as f:
            pickle.dump(avg_encoding, f)
        print("Face data saved successfully.")
    else:
        print("No face data captured.")

    cap.release()
    cv2.destroyAllWindows()


# This code is recognize_face from video
def recognize_face_with_video():
    # بارگذاری داده‌های ذخیره‌شده
    try:
        with open("saved_face.pkl", "rb") as f:
            saved_encoding = pickle.load(f)
    except FileNotFoundError:
        print("No saved face data found. Please run the enrollment step first.")
        return

    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot access webcam.")

    print("Looking for a match...")
    start_time = time.time()
    match_start_time = None  # مقداردهی اولیه

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Face Recognition: شناسایی و تطبیق چهره
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        match_status = "Unknown"
        matched = False  # وضعیت تطابق
        min_distance = 1.0  # مقدار اولیه بزرگ

        for face_encoding, face_location in zip(face_encodings, face_locations):
            distances = face_recognition.face_distance([saved_encoding], face_encoding)
            current_distance = distances[0]

            if current_distance < 0.3:  # مقدار آستانه دقیق‌تر
                match_status = "Matched"
                matched = True
                min_distance = current_distance

                # ذخیره زمان شروع تطابق موفق
                if match_start_time is None:
                    match_start_time = time.time()

            # رسم مستطیل روی چهره
            top, right, bottom, left = face_location
            color = (0, 255, 0) if match_status == "Matched" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # نمایش فاصله
            cv2.putText(frame, f"Distance: {current_distance:.2f}", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # MediaPipe Face Mesh: رسم مش
        mesh_results = face_mesh.process(rgb_frame)
        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )

        # نمایش وضعیت تطابق
        cv2.putText(frame, f"Status: {match_status}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # نمایش فریم
        cv2.imshow("Face Recognition", frame)

        # اگر چهره تطابق داشت
        if matched and time.time() - match_start_time >= 10:
            print(f"Match Found: The person matches the saved data. Distance: {min_distance:.2f}")
            cv2.putText(frame, "Matched", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Face Recognition", frame)
            cv2.waitKey(8000)  # نمایش ۲ ثانیه پیام
            break

        # اگر زمان بیشتر از ۳۰ ثانیه شد
        if time.time() - start_time > 30:
            print("Timeout: No match found within 30 seconds.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # خروج دستی
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_face_with_photo():
    # بارگذاری داده‌های ذخیره‌شده
    try:
        with open("saved_face.pkl", "rb") as f:
            saved_encoding = pickle.load(f)
    except FileNotFoundError:
        print("No saved face data found. Please run the enrollment step first.")
        return

    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot access webcam.")

    print("Position yourself properly in front of the camera.")
    print("Press 's' to capture a photo for recognition.")
    print("Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe Face Mesh: رسم شبکه توری
        mesh_results = face_mesh.process(rgb_frame)
        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )

        # نمایش فریم
        cv2.imshow("Face Recognition", frame)

        # ذخیره عکس با زدن کلید 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Photo captured. Processing for recognition...")
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if not face_encodings:
                print("No face detected. Please try again.")
                continue

            # مقایسه انکدینگ عکس گرفته‌شده با داده‌های ذخیره‌شده
            match_status = "Unknown"
            min_distance = 1.0  # مقدار اولیه بزرگ

            for face_encoding, face_location in zip(face_encodings, face_locations):
                distances = face_recognition.face_distance([saved_encoding], face_encoding)
                current_distance = distances[0]

                if current_distance < 0.5:  # مقدار آستانه دقیق‌تر
                    match_status = "Matched"
                    min_distance = current_distance
                else:
                    match_status = "Not Matched"

                # رسم مستطیل دور چهره
                top, right, bottom, left = face_location
                color = (0, 255, 0) if match_status == "Matched" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # نمایش وضعیت و فاصله
                cv2.putText(frame, f"Status: {match_status}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(frame, f"Distance: {current_distance:.2f}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # نمایش فریم نهایی
            cv2.imshow("Recognition Result", frame)
            cv2.waitKey(8000)  # نمایش نتیجه برای چند ثانیه
            break

        # خروج با کلید 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting without recognition.")
            break

    cap.release()
    cv2.destroyAllWindows()



print("Select an option:")
print("1. Enroll a face")
print("2. Recognize a face with video")
print("3. Recognize a face with photo ")
choice = input("Enter your choice  (1/2/3):")

if choice == '1':
    capture_and_store_encodings()
elif choice == '2':
    recognize_face_with_video()

elif choice == '3':
    recognize_face_with_photo()
else:
    print("Invalid choice.")
