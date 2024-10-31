import cv2
import mediapipe as mp

""" Initialize mediapipe drawing and face mesh utilities """
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

""" Define key facial feature regions by indices """
EYEBROWS_LEFT = list(range(52, 59))
EYEBROWS_RIGHT = list(range(282, 291))
CHIN = list(range(152, 160))

CHEEKS_LEFT = list(range(205, 209))
CHEEKS_RIGHT = list(range(425, 429))
MOUTH = list(range(0, 12))

EYES_LEFT = list(range(143, 156))  
EYES_RIGHT = list(range(373, 386))
NOSE = list(range(1, 12)) + list(range(168, 187))

""" Combine all key facial features into a single list for ease of use """
ALL_KEYPOINT_INDICES = EYEBROWS_LEFT + EYEBROWS_RIGHT + CHIN + CHEEKS_LEFT + CHEEKS_RIGHT + MOUTH + EYES_LEFT + EYES_RIGHT + NOSE

""" 
Function to extract specified key points based on landmark indices 
Arguments:
- landmarks: all facial landmarks detected
- indices: list of landmark indices to extract
Returns:
- list of extracted key points as (x, y, z, confidence) tuples
"""
def extract_facial_keypoints(landmarks, indices):
    return [(float(landmarks[idx].x), float(landmarks[idx].y), float(landmarks[idx].z),
         float(getattr(landmarks[idx], 'visibility', 1.0))) for idx in indices]

""" 
Function to compute changes in key points between current and initial frames
Arguments:
- keypoints_list: list of key points over multiple frames
Returns:
- list of changes in (x, y, z) coordinates or None if insufficient frames
"""
def compute_keypoint_changes(keypoints_list):
    if len(keypoints_list) < 10:
        return None
    first_frame_keypoints = keypoints_list[-10]
    current_frame_keypoints = keypoints_list[-1]
    return [
        (current_frame_keypoints[i][0] - first_frame_keypoints[i][0],
         current_frame_keypoints[i][1] - first_frame_keypoints[i][1],
         current_frame_keypoints[i][2] - first_frame_keypoints[i][2])
        for i in range(len(first_frame_keypoints))
    ]

""" 
Function to draw key points on the image 
Arguments:
- image: the video frame to draw on
- key_points: list of (x, y, z, confidence) coordinates to draw
- color: color for key points in BGR format
"""
def draw_key_points(image, key_points, color=(255, 0, 0)):
    height, width, _ = image.shape
    for x, y, _, _ in key_points:
        pixel_x = int(x * width)
        pixel_y = int(y * height)
        cv2.circle(image, (pixel_x, pixel_y), radius=3, color=color, thickness=-1)

""" 
Main function to capture video feed, process face mesh, 
and compute/draw key points and their changes 
"""
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    
    keypoints_per_frame = []
    
    """ Open text files to record key points and key point differences """
    with open('keypoints.txt', 'w') as keypoint_file, open('difference.txt', 'w') as difference_file:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            """ Process the image with face mesh to find landmarks """
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image_rgb)
            image.flags.writeable = True 

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Extract key points
                    combined_keypoints = extract_facial_keypoints(face_landmarks.landmark, ALL_KEYPOINT_INDICES)
                    keypoints_per_frame.append(combined_keypoints)

                    """ Write key points with confidence scores to file """
                    keypoint_file.write("Keypoints:\n")
                    keypoint_file.writelines(
                        f"Keypoint {i + 1}:\n ({x:.6f}, {y:.6f}, {z:.6f}, Confidence: {conf:.2f})\n"
                        for i, (x, y, z, conf) in enumerate(combined_keypoints)
                    )

                    """ Compute and record changes in key points """
                    keypoint_changes = compute_keypoint_changes(keypoints_per_frame)
                    if keypoint_changes:
                        difference_file.write("Keypoint changes:\n")
                        difference_file.writelines(
                            f"Keypoint {i + 1}:\n ({dx:.6f}, {dy:.6f}, {dz:.6f})\n"
                            for i, (dx, dy, dz) in enumerate(keypoint_changes)
                        )
                        difference_file.write("\n")

                    """ Draw current key points on the frame """
                    draw_key_points(image, combined_keypoints, color=(255, 0, 0))

            """ Display the frame with drawn key points """
            cv2.imshow('Facial Key Points and Changes', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break

""" Release resources """
cap.release()
cv2.destroyAllWindows()
