# Face Recognition and Mesh Visualization
This project provides a face recognition system with features to enroll, recognize faces via video feed, and recognize faces from captured photos. The program utilizes OpenCV, MediaPipe, and Face Recognition libraries to create a real-time, interactive experience.

# Features
1. Face Enrollment
Captures face encodings using MediaPipe Face Mesh and face_recognition libraries.
Guides the user to rotate their head in different directions for better face data collection.
Saves face data as a pickle file (saved_face.pkl) for future recognition.
2. Real-time Face Recognition with Video
Matches the live feed from the webcam with the previously saved face data.
Displays the match status and distance on-screen in real-time.
Highlights faces with a bounding box and shows "Matched" or "Unknown" status.
3. Face Recognition from a Captured Photo
Allows the user to capture a photo and matches it against the saved face data.
Displays the match status, distance, and highlights faces in the photo.


# Installation
1. Clone the repository or download the script file.

2. Install the required Python libraries:
  "pip install opencv-python mediapipe face-recognition numpy"

3. Ensure that your system has a working webcam.


# Usage
1. Run the script:
     "python face_recognition_system.py"

2. Select an option from the menu:
     1. Enroll a face
     2. Recognize a face with video
     3. Recognize a face from a photo
  
# Instructions for Each Option
Option 1: Enroll a Face
  The program will open the webcam.
  Follow the on-screen instructions to move your head in different directions.
  Once enough face data is captured, it will save the data in saved_face.pkl.
Option 2: Recognize Face with Video
  The webcam will open, and the system will try to match live faces with the saved face data.
  If a match is found:
  The match status (Matched) will be displayed on-screen.
  The program will stop after confirming the match for 10 seconds.
  If no match is found within 30 seconds, the program will exit.
Option 3: Recognize Face with Photo
  The webcam will open, and you can press s to capture a photo.
  The system will analyze the captured photo and compare it with the saved face data.
  The match status (Matched or Not Matched) will be displayed on-screen.
# Requirements
Python 3.6+
# Libraries:
OpenCV (cv2)
MediaPipe
Face Recognition
NumPy
Pickle (for saving/loading face data)
A webcam or video feed.
# Notes
Ensure the saved face data file (saved_face.pkl) exists before attempting face recognition.
Adjust recognition thresholds in the code if needed for better accuracy:
Matching threshold: current_distance < 0.3 (in video recognition).
Recognition timeout is set to 30 seconds for video recognition.
Known Issues
Low-light conditions or obstructed faces may reduce recognition accuracy.
Requires only one face in the frame for proper enrollment/recognition.
# License
This project is open-source and licensed under the MIT License. Feel free to modify and adapt it to your needs.
