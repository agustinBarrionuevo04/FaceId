import psycopg
import os
import json
import numpy as np


def np_array_to_Json(vector):
    return json.dumps(vector.tolist())


def json_to_np_array(vector_string):
    return np.array(json.loads(vector_string))


def get_db_connection():
    db_url = os.getenv("DATA_BASE")
    if not db_url:
        raise ValueError("La variable de entorno DATA_BASE no está definida.")
    return psycopg.connect(db_url, sslmode='require')


def new_user(name, vector_json):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "usuarios" (name, vector) VALUES (%s, %s)', (name, vector_json))
    conn.commit()
    conn.close()


def exist_user(vector_json):
    conn = get_db_connection()
    cursor = conn.cursor()
    vector = json_to_np_array(vector_json)
    cursor.execute('SELECT * FROM usuarios')
    row = cursor.fetchone()
    while row is not None:
        vector_db = json_to_np_array(row[2])
        exist_face = compare_vectors(vector, vector_db)
        if exist_face:
            conn.close()
            return exist_face, row[1]
        row = cursor.fetchone()
    conn.close()
    return False, None


def compare_vectors(vec1, vec2, threshold=0.6):
    dist = np.linalg.norm(vec1 - vec2)
    return dist < threshold
