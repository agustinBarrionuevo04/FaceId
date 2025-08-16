"""
Face Vector Extraction Module
-----------------------------

This module provides utilities to process images (frames) and extract a unique
face embedding vector using the `face_recognition` library.

The embedding vector is a numerical representation of a detected face and can
be used for tasks such as user verification or identification.
"""

import os
import json
import face_recognition


def get_vector(frame, id_user: str | None = None):
    """
    Extract the embedding vector from a given image frame.

    Args:
        frame (numpy.ndarray): Image frame (BGR format, e.g., from OpenCV).
        id_user (str | None): Optional user ID associated with the frame.

    Returns:
        numpy.ndarray | None:
            - A 128-dimensional embedding vector if a face is detected and
              successfully encoded.
            - None if no face is detected or encoding fails.

    Workflow:
        1. Convert the image from BGR to RGB.
        2. Detect face locations in the frame.
        3. Encode the face into a numerical vector.
        4. Return the first detected face encoding.

    Exceptions:
        Prints an error message and returns None if any unexpected error occurs.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Convert the image from BGR (OpenCV) to RGB (face_recognition expects RGB)
        image = frame[:, :, ::-1].copy()

        # Detect faces in the image
        face_location = face_recognition.face_locations(image)
        if not face_location:
            print("No face detected in the captured frame.")
            return None

        # Encode the detected face into an embedding vector
        face_encoding = face_recognition.face_encodings(image, face_location)
        if not face_encoding:
            print("Failed to encode face vector :(")
            return None

        return face_encoding[0]

    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return None
