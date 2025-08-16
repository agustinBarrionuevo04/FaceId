"""
Face Capture Module
-------------------

This module provides functionality to capture a single face frame using the 
default webcam. The captured frame can later be used for face recognition 
processing (e.g., generating embedding vectors).
"""

import cv2
import time
import face_recog


def get_face():
    """
    Capture a single frame from the default webcam.

    This function opens the system's default camera (device 0), displays a 
    fullscreen preview window, and waits until the user presses the 's' key 
    to capture a frame. The frame is then returned for further processing.

    Returns:
        numpy.ndarray | None:
            - Captured frame as a NumPy array (BGR format, OpenCV standard).
            - None if capturing fails.

    Raises:
        IOError: If the camera cannot be accessed.

    Workflow:
        1. Initialize the webcam.
        2. Set resolution to 1080p (1920x1080).
        3. Display the live feed in a fullscreen resizable window.
        4. Wait until the user presses 's' to capture a frame.
        5. Release the camera and close the window.
    """
    # 1. Open the default webcam (device 0)
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise IOError("Could not access the camera.")

    # 2. Set resolution to 1080p
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Small delay to allow camera to initialize
    time.sleep(2)

    window_name = "Face Capture - Press 's' to take a snapshot"

    # Create a resizable fullscreen window
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
    )
    cv2.resizeWindow(window_name, 1920, 1080)

    ret, frame = False, None

    while True:
        ret, frame = cam.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)
        if key == ord("s"):
            break

    # Release resources and close windows
    cam.release()
    cv2.destroyAllWindows()

    if not ret:
        print("Failed to capture frame.\n")
        return None

    return frame
