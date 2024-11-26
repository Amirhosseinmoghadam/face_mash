# import cv2
# import mediapipe as mp
# import face_recognition
# import numpy as np
# import time
#
# # تنظیمات MediaPipe Face Mesh
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#
# # تنظیمات Face Recognition
# image_path = "reference2.jpg"  # مسیر عکس مرجع
# image = cv2.imread(image_path)
# if image is None:
#     raise ValueError("Input image cannot be found.")
#
# rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# face_locations = face_recognition.face_locations(rgb_image)
# if len(face_locations) == 0:
#     raise ValueError("No face found in the reference image.")
#
# reference_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
#
# # رسم تور روی چهره مرجع
# for face_location in face_locations:
#     top, right, bottom, left = face_location
#     face_landmarks = face_recognition.face_landmarks(rgb_image, [face_location])[0]
#     for key, points in face_landmarks.items():
#         for x, y in points:
#             cv2.circle(image, (x, y), 1, (0, 255, 0), -1)
#
# cv2.imshow("Reference Image", image)
# cv2.waitKey(2000)
# cv2.destroyAllWindows()
#
# # پردازش ویدیو با وب‌کم
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     raise RuntimeError("Cannot access webcam.")
#
# matched = False
# match_start_time = None
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     # Face Recognition برای تشخیص و انکدینگ
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#     # MediaPipe Face Mesh برای رسم مش
#     mesh_results = face_mesh.process(rgb_frame)
#
#     # بررسی تطابق چهره‌ها
#     match_status = "Unknown"
#     for face_encoding, face_location in zip(face_encodings, face_locations):
#         matches = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=0.6)
#         if True in matches:
#             match_status = "Matched"
#             matched = True
#             if match_start_time is None:
#                 match_start_time = time.time()
#
#         # رسم مستطیل روی چهره
#         top, right, bottom, left = face_location
#         color = (0, 255, 0) if match_status == "Matched" else (0, 0, 255)
#         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#
#     # رسم تور MediaPipe روی چهره‌ها
#     if mesh_results.multi_face_landmarks:
#         for face_landmarks in mesh_results.multi_face_landmarks:
#             for landmark in face_landmarks.landmark:
#                 h, w, _ = frame.shape
#                 x, y = int(landmark.x * w), int(landmark.y * h)
#                 cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)
#
#     # نمایش وضعیت تطابق
#     cv2.putText(frame, f"Status: {match_status}", (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#     # نمایش فریم
#     cv2.imshow("Face Recognition and Mesh", frame)
#
#     # اگر تطابق پیدا شد، 10 ثانیه صبر کرده و برنامه را ببند
#     if matched and time.time() - match_start_time >= 10:
#         print("Match Found: The person matches the reference image.")
#         break
#
#     # خروج با کلید 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # آزادسازی منابع
# cap.release()
# cv2.destroyAllWindows()

#
# import cv2
# import mediapipe as mp
# import face_recognition
# import numpy as np
# import time
#
# # تنظیمات MediaPipe Face Mesh
# mp_face_mesh = mp.solutions.face_mesh
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# face_mesh = mp_face_mesh.FaceMesh(
#     static_image_mode=False,
#     max_num_faces=1,
#     refine_landmarks=True,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )
#
# # تنظیمات Face Recognition
# image_path = "reference2.jpg"  # مسیر عکس مرجع
# image = cv2.imread(image_path)
# if image is None:
#     raise ValueError("Input image cannot be found.")
#
# rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# face_locations = face_recognition.face_locations(rgb_image)
# if len(face_locations) == 0:
#     raise ValueError("No face found in the reference image.")
#
# reference_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
#
# # پردازش ویدیو با وب‌کم
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     raise RuntimeError("Cannot access webcam.")
#
# matched = False
# match_start_time = None
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     # Face Recognition برای تشخیص و انکدینگ
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#     # MediaPipe Face Mesh برای رسم مش
#     mesh_results = face_mesh.process(rgb_frame)
#
#     # بررسی تطابق چهره‌ها
#     match_status = "Unknown"
#     for face_encoding, face_location in zip(face_encodings, face_locations):
#         matches = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=0.6)
#         if True in matches:
#             match_status = "Matched"
#             matched = True
#             if match_start_time is None:
#                 match_start_time = time.time()
#
#         # رسم مستطیل روی چهره
#         top, right, bottom, left = face_location
#         color = (0, 255, 0) if match_status == "Matched" else (0, 0, 255)
#         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#
#     # رسم تور MediaPipe روی چهره‌ها
#     if mesh_results.multi_face_landmarks:
#         for face_landmarks in mesh_results.multi_face_landmarks:
#             mp_drawing.draw_landmarks(
#                 frame,
#                 face_landmarks,
#                 mp_face_mesh.FACEMESH_TESSELATION,
#                 landmark_drawing_spec=None,
#                 connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
#             )
#
#     # نمایش وضعیت تطابق
#     cv2.putText(frame, f"Status: {match_status}", (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#     # نمایش فریم
#     cv2.imshow("Face Recognition and Mesh", frame)
#
#     # اگر تطابق پیدا شد، 10 ثانیه صبر کرده و برنامه را ببند
#     if matched and time.time() - match_start_time >= 10:
#         print("Match Found: The person matches the reference image.")
#         break
#
#     # خروج با کلید 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # آزادسازی منابع
# cap.release()
# cv2.destroyAllWindows()



import cv2
import mediapipe as mp
import face_recognition
import numpy as np
import time

# تنظیمات MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,  # چون تصویر ثابت است
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

# تنظیمات Face Recognition
image_path = "reference2.jpg"  # مسیر عکس مرجع
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Input image cannot be found.")

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
face_locations = face_recognition.face_locations(rgb_image)
if len(face_locations) == 0:
    raise ValueError("No face found in the reference image.")

# محاسبه انکدینگ چهره مرجع
reference_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]

# پردازش تصویر مرجع با MediaPipe و رسم مش
mesh_results = face_mesh.process(rgb_image)
if mesh_results.multi_face_landmarks:
    for face_landmarks in mesh_results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image,
            face_landmarks,
            mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
        )

# نمایش تصویر مرجع با مش رسم‌شده
cv2.imshow("Reference Image with Face Mesh", image)
cv2.waitKey(2000)
cv2.destroyAllWindows()

# پردازش ویدیو با وب‌کم
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot access webcam.")

matched = False
match_start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Face Recognition برای تشخیص و انکدینگ
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # MediaPipe Face Mesh برای رسم مش
    mesh_results = face_mesh.process(rgb_frame)

    # بررسی تطابق چهره‌ها
    match_status = "Unknown"
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=0.6)
        if True in matches:
            match_status = "Matched"
            matched = True
            if match_start_time is None:
                match_start_time = time.time()

        # رسم مستطیل روی چهره
        top, right, bottom, left = face_location
        color = (0, 255, 0) if match_status == "Matched" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    # رسم تور MediaPipe روی چهره‌ها
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
    cv2.imshow("Face Recognition and Mesh", frame)

    # اگر تطابق پیدا شد، 10 ثانیه صبر کرده و برنامه را ببند
    if matched and time.time() - match_start_time >= 10:
        print("Match Found: The person matches the reference image.")
        break

    # خروج با کلید 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# آزادسازی منابع
cap.release()
cv2.destroyAllWindows()
