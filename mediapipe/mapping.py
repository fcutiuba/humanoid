import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Indices for important facial landmarks
EYEBROWS_LEFT = list(range(52, 69))
EYEBROWS_RIGHT = list(range(282, 299))
CHIN = list(range(152, 166))
CHEEKS_LEFT = list(range(205, 212))
CHEEKS_RIGHT = list(range(425, 432))
MOUTH = list(range(0, 18))
EYES_LEFT = list(range(133, 145))
EYES_RIGHT = list(range(362, 374))
NOSE = list(range(1, 20)) + list(range(168, 198))

# Function to extract key points from specific facial regions
def extract_facial_keypoints(landmarks, indices):
    key_points = []
    for idx in indices:
        landmark = landmarks[idx]
        key_points.append((landmark.x, landmark.y, landmark.z))
    return key_points

# Function to draw key points in blue (BGR: 255, 0, 0)
def draw_key_points(image, key_points, color=(255, 0, 0)):
    height, width, _ = image.shape
    for x, y, _ in key_points:
        # Convert normalized coordinates to pixel values
        pixel_x = int(x * width)
        pixel_y = int(y * height)
        # Draw each point as a blue circle
        cv2.circle(image, (pixel_x, pixel_y), radius=2, color=color, thickness=-1)  # Blue color (BGR)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

  with open('keypoints_facial_regions.txt', 'w') as f:  # Open the file to write the key points
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        continue

      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = face_mesh.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
          # Extracting key points for specific facial regions
          keypoints_eyebrows_left = extract_facial_keypoints(face_landmarks.landmark, EYEBROWS_LEFT)
          keypoints_eyebrows_right = extract_facial_keypoints(face_landmarks.landmark, EYEBROWS_RIGHT)
          keypoints_chin = extract_facial_keypoints(face_landmarks.landmark, CHIN)
          keypoints_cheeks_left = extract_facial_keypoints(face_landmarks.landmark, CHEEKS_LEFT)
          keypoints_cheeks_right = extract_facial_keypoints(face_landmarks.landmark, CHEEKS_RIGHT)
          keypoints_mouth = extract_facial_keypoints(face_landmarks.landmark, MOUTH)
          keypoints_eyes_left = extract_facial_keypoints(face_landmarks.landmark, EYES_LEFT)
          keypoints_eyes_right = extract_facial_keypoints(face_landmarks.landmark, EYES_RIGHT)
          keypoints_nose = extract_facial_keypoints(face_landmarks.landmark, NOSE)

          # Draw key points for each facial region in blue
          draw_key_points(image, keypoints_eyebrows_left, color=(255, 0, 0))
          draw_key_points(image, keypoints_eyebrows_right, color=(255, 0, 0))
          draw_key_points(image, keypoints_chin, color=(255, 0, 0))
          draw_key_points(image, keypoints_cheeks_left, color=(255, 0, 0))
          draw_key_points(image, keypoints_cheeks_right, color=(255, 0, 0))
          draw_key_points(image, keypoints_mouth, color=(255, 0, 0))
          draw_key_points(image, keypoints_eyes_left, color=(255, 0, 0))
          draw_key_points(image, keypoints_eyes_right, color=(255, 0, 0))
          draw_key_points(image, keypoints_nose, color=(255, 0, 0))

          # Write the key points to the text file
          for region, keypoints in zip(
              ['Eyebrows Left', 'Eyebrows Right', 'Chin', 'Cheeks Left', 'Cheeks Right', 'Mouth', 'Eyes Left', 'Eyes Right', 'Nose'],
              [keypoints_eyebrows_left, keypoints_eyebrows_right, keypoints_chin, keypoints_cheeks_left, keypoints_cheeks_right, keypoints_mouth, keypoints_eyes_left, keypoints_eyes_right, keypoints_nose]):
              
              f.write(f"{region}:\n")
              for point in keypoints:
                  f.write(f"x: {point[0]:.6f}, y: {point[1]:.6f}, z: {point[2]:.6f}\n")

          # Draw the full face mesh landmarks in grey (default style)
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_CONTOURS,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_IRISES,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())

      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('Facial Key Points with Full Face Mesh (Eyebrows, Chin, Cheeks, Mouth, Eyes, Nose)', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
