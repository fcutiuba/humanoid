import unittest
import numpy as np
import cv2
from keypoints import extract_facial_keypoints, compute_keypoint_changes, draw_key_points

class FakeLandmark:
    """ A mock class to simulate the landmark object from Mediapipe. """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class TestFacialKeypointProcessing(unittest.TestCase):

    def test_extract_facial_keypoints(self):
        """ Test that key points are correctly extracted based on indices. """
        landmarks = [FakeLandmark(0.1, 0.2, 0.3), FakeLandmark(0.4, 0.5, 0.6)]
        indices = [0, 1]
        result = extract_facial_keypoints(landmarks, indices)
        
        expected = [(0.1, 0.2, 0.3), (0.4, 0.5, 0.6)]
        self.assertEqual(result, expected)

    def test_compute_keypoint_changes(self):
        """ Test that keypoint changes are computed accurately. """
        keypoints_list = [
            [(0.1, 0.1, 0.1)],
            [(0.2, 0.2, 0.2)],
            [(0.3, 0.3, 0.3)], 
            [(0.4, 0.4, 0.4)], 
            [(0.5, 0.5, 0.5)],
            [(0.6, 0.6, 0.6)], 
            [(0.7, 0.7, 0.7)], 
            [(0.8, 0.8, 0.8)], 
            [(0.9, 0.9, 0.9)], 
            [(1.0, 1.0, 1.0)]
        ]
        
        result = compute_keypoint_changes(keypoints_list)
        expected = [(0.9, 0.9, 0.9)]  # Change from frame 1 to frame 10
        self.assertEqual(result, expected)

    def test_draw_key_points(self):
        """ Test that key points are drawn correctly on the image. """
        # Create a blank image (100x100 pixels)
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Define some key points in normalized coordinates (0-1)
        key_points = [(0.5, 0.5, 0.0), (0.25, 0.25, 0.0)]
        
        # Draw key points on the image
        draw_key_points(image, key_points, color=(255, 0, 0))
        
        # Convert normalized coordinates to pixel positions
        height, width, _ = image.shape
        expected_positions = [
            (int(0.5 * width), int(0.5 * height)),  # (50, 50)
            (int(0.25 * width), int(0.25 * height))  # (25, 25)
        ]
        
        # Check that the pixels at the expected positions are red
        for pos in expected_positions:
            pixel_value = image[pos[1], pos[0]]
            self.assertTrue((pixel_value == np.array([255, 0, 0])).all())

if __name__ == "__main__":
    unittest.main()
