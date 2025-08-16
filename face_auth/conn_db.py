"""
Database Manager for Face Recognition System
--------------------------------------------

This module provides utility functions for managing a SQLite database that 
stores user information and their corresponding face vectors.

Main responsibilities:
    - Serialize and deserialize NumPy arrays to/from JSON.
    - Manage database connections and queries.
    - Insert new users into the database.
    - Check for the existence of tables or users based on facial recognition.

Database:
    - File: data_base.db (stored in the same directory as this module)
    - Table: usuarios
        Columns:
            id (INTEGER PRIMARY KEY AUTOINCREMENT)
            name (TEXT)
            vector (TEXT, JSON representation of NumPy array)
"""

import os
import json
import sqlite3
import numpy as np
import face_recognition

import face_recog
import get_face

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def np_array_to_json(vector: np.ndarray) -> str:
    """
    Convert a NumPy array to a JSON string.

    Args:
        vector (np.ndarray): NumPy array to serialize.

    Returns:
        str: JSON string representation of the array.
    """
    return json.dumps(vector.tolist())


def json_to_np_array(vector_string: str) -> np.ndarray:
    """
    Convert a JSON string back to a NumPy array.

    Args:
        vector_string (str): JSON string to deserialize.

    Returns:
        np.ndarray: Reconstructed NumPy array.
    """
    return np.array(json.loads(vector_string))


def exist_table(table_name: str) -> bool:
    """
    Check if a given table exists in the database.

    Args:
        table_name (str): Name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    conn = sqlite3.connect(f"{BASE_DIR}/data_base.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(name) 
        FROM SQLITE_MASTER 
        WHERE TYPE = 'table' AND name = ?
        """,
        (table_name,),
    )
    exists = cursor.fetchone()[0] == 1

    conn.close()
    return exists


def new_user(name: str, vector_json: str) -> None:
    """
    Insert a new user into the database.

    Args:
        name (str): Username to insert.
        vector_json (str): JSON string of the face vector.

    Notes:
        Assumes that the table "usuarios" exists in the database.
    """
    conn = sqlite3.connect(f"{BASE_DIR}/data_base.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO usuarios (name, vector) VALUES (?, ?)""",
        (name, vector_json),
    )

    conn.commit()
    conn.close()


def exist_user(vector_json: str) -> tuple[bool, str | None]:
    """
    Check if a user exists in the database based on face recognition.

    Args:
        vector_json (str): JSON string of the face vector to compare.

    Returns:
        tuple:
            - bool: True if a match is found, False otherwise.
            - str | None: The name of the matched user, or None if no match.
    """
    conn = sqlite3.connect(f"{BASE_DIR}/data_base.db")
    cursor = conn.cursor()

    vector = json_to_np_array(vector_json)
    cursor.execute("""SELECT * FROM usuarios""")
    row = cursor.fetchone()
    conn.close()

    while row is not None:
        vector_db = json_to_np_array(row[2])
        exists = bool(face_recognition.compare_faces([vector_db], vector)[0])
        if exists:
            return True, row[1]
        row = cursor.fetchone()

    return False, None
