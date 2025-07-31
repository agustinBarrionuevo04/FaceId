import cv2
import get_face
import face_recog
import compare

print("******************************Bienvenido******************************\n")
response_user = input("0 == Start sesion || 1 == Register :")
if int(response_user) == 0:
    print("Vamos a utilizar su camara para obtener su id\n")
    get_face.get_face()
    id_user = input("Usuario:")
    face_recog.get_vector(id_user)
    compare.compare_faces(id_user)
    