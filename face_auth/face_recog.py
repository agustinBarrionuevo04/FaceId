import os
import face_recognition
import json

"""Realizamos el escaneo de las imagenes para obtener un json con informacion
de la persona mas un vector embebido el cual es unico"""


def get_vector(id_user):
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(BASE_DIR, "img", f"{id_user}.png")

        image = face_recognition.load_image_file(img_path)
        if not os.path.exists(img_path):
            print("Ocurrio un error al seleccionar la imagen")
            exit()

        image = face_recognition.load_image_file(img_path)

        """Obtenemos informacion del rostro y sus embedding"""
        face_location = face_recognition.face_locations(image)
        face_encoding = face_recognition.face_encodings(image, face_location)

        data = []
        for encoding in face_encoding:
            data.append({
                "name": id_user,
                "embedding": encoding.tolist()
            })

        json_path = os.path.join(BASE_DIR, "ids", f"{id_user}.json")
        with open(json_path, "w") as json_end:
            json.dump(data, json_end, indent=4)
        
        
        #chequear las dos funciones siguiente ya que generan que salte el execept
        cur_vector = get_current_vector(id_user)
        
        arr_embeddings = get_info_vectors_json()
        
        for e in arr_embeddings:
            if cur_vector != e:
                print("Su informacion se obtuvo correctamente \n")
                return True        
            else:
                print("Ya estas registrado")
        
    except Exception as e:
        print("Ocurrió un error inesperado:", str(e))

"""
obtenemos el vector embebido del usuario que se esta registrando actualmente
"""
def get_current_vector(id_user):
    with open(id_user, "r") as f:
        vector_check = json.load(f)
    vector = vector_check[0]["embbeding"]
    return vector
    
"""Obtenemos un array con los vectores embebidos de los usuarios ya registrados"""
def get_info_vectors_json():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ids")
    embeddings = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_path = os.path.join(directory, filename)
            with open(json_path, "r") as f:
                data_vector = json.load(f)
                for entry in data_vector:
                    embedding = entry.get("embedding")
                    if embedding is not None:
                        embeddings.append(embedding)
    return embeddings

