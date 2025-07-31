import os
import face_recognition
import json

"""Realizamos el escaneo de las imagenes para obtener un json con informacion 
de la persona mas un vector embebido el cual es unico"""

def get_vector(id_user):
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
            "name": id_user ,
            "embedding": encoding.tolist()
        })
        
    json_path = f"ids/{id_user}.json"
    with open(json_path , "w") as json_end:
        json.dump(data,json_end,indent=4)

    print("Su informacion se obtuvo correctamente \n")

