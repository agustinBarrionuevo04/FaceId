"""
Face Recognition Login/Registration Client
------------------------------------------

This script provides a command-line interface for user login and registration
through face recognition. It communicates with a backend API to verify or 
register users using their facial feature vectors.

Modules:
    - requests: for sending HTTP requests to the backend API.
    - json: to handle JSON serialization/deserialization.
    - face_recognition: used for encoding/decoding face features (indirectly).
    - conn_db: custom module for database vector serialization.
    - face_recog: custom module for extracting facial embeddings.
    - get_face: custom module for capturing a user's face via the webcam.

Execution:
    Run the script directly with Python. The program will continuously prompt
    the user to log in or register until the process is completed or the user
    exits.
"""

import json
import requests
import face_recognition

import conn_db
import face_recog
import get_face


def main():
    """
    Entry point of the face recognition login/registration client.

    This function continuously prompts the user to either log in (option "0")
    or register (option "1") using facial recognition. It captures the user's
    face through the camera, generates a feature vector, and sends it to a
    backend API for verification or registration.

    Workflow:
        1. Prompt the user to log in or register.
        2. Capture face data from the webcam.
        3. Convert the facial vector to JSON format.
        4. Send the vector to the backend API to verify if the user exists.
        5. If login:
            - Grant access if the user exists.
            - Otherwise, ask the user to register.
        6. If register:
            - Prevent duplicate registrations.
            - Request a username and register the new user in the backend.
        7. Handle errors from the server gracefully.
        8. Exit cleanly on Ctrl+C or Ctrl+D.

    Exceptions:
        KeyboardInterrupt, EOFError:
            Exits the program gracefully when the user interrupts.
    """

    print("\n*** Press Ctrl+C or Ctrl+D to exit the program ***")

    try:
        while True:
            # Prompt the user for login (0) or registration (1)
            response_user = input(
                "\n0 == Login or 1 == Register\n"
            ).strip()

            if response_user not in ("0", "1"):
                print("Invalid option, please try again.")
                continue

            print("We will now use your camera to capture your ID...\n")

            # Capture the face, extract the feature vector, and serialize it
            vector = face_recog.get_vector(get_face.get_face())
            vector_string = conn_db.np_array_to_Json(vector)

            # Send the vector to the verification endpoint
            url_verify = "http://127.0.0.1:8000/procesar-vector"
            payload_verify = {"vector": vector_string}

            response = requests.post(url_verify, json=payload_verify)

            if response.status_code != 200:
                print(
                    f"Server error ({response.status_code}): "
                    f"{response.text}"
                )
                continue

            data = response.json()
            val = data.get("Exist")
            name_db = data.get("Name")

            # Handle login flow
            if response_user == "0":
                if val:
                    print(
                        f"Welcome back, {name_db}! "
                        "Glad to see you again :)"
                    )
                    exit(0)
                else:
                    print("User not found in the database. Please register.")
                    continue

            # Handle registration flow
            elif response_user == "1":
                if val:
                    print(
                        f"You are already registered as {name_db}. "
                        "Please log in."
                    )
                    continue

                name = input("Enter a username: ").strip()

                url_register = "http://127.0.0.1:8000/register"
                payload_register = {
                    "vector": vector_string,
                    "name": name
                }

                response_reg = requests.post(
                    url_register, json=payload_register
                )

                if response_reg.status_code == 200:
                    data_reg = response_reg.json()
                    print(f"{data_reg.get('message')}")
                else:
                    print(
                        f"Error registering user "
                        f"({response_reg.status_code}): {response_reg.text}"
                    )

    except (KeyboardInterrupt, EOFError):
        # Graceful exit when the user terminates the program
        print("\nExiting program...")
        exit(0)


if __name__ == "__main__":
    main()
