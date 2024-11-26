# face mash okay
import cv2
import mediapipe as mp

# تنظیمات Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
drawing_utils = mp.solutions.drawing_utils
drawing_styles = mp.solutions.drawing_styles

# استفاده از وب‌کم
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # تبدیل تصویر از BGR به RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # پردازش Face Mesh
    results = face_mesh.process(rgb_frame)

    # رسم Face Mesh روی تصویر
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # رسم توری سه‌بعدی صورت
            drawing_utils.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
            )
            # رسم کانتور لب‌ها، چشم‌ها و ابروها با رنگ خاص
            drawing_utils.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_LIPS,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
            drawing_utils.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_LEFT_EYE | mp_face_mesh.FACEMESH_RIGHT_EYE,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)
            )
            drawing_utils.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_LEFT_EYEBROW | mp_face_mesh.FACEMESH_RIGHT_EYEBROW,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

    # نمایش تصویر
    cv2.imshow('Face Mesh', frame)

    # خروج از برنامه با فشردن کلید 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# آزادسازی منابع
cap.release()
cv2.destroyAllWindows()
