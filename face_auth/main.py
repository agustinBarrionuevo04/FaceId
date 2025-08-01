import cv2
import get_face
import face_recog
import compare

print("******************************Bienvenido******************************\n")
print("En caso de querer salir del programa preciona Ctrl+C o Ctrl+D")
try:    
    while 1:
        response_user = input("0 == Start sesion || 1 == Register :")
        if int(response_user) == 0:
            print("Vamos a utilizar su camara para obtener su id\n")
            get_face.get_face()
            id_user = input("Introduci tu Usuario:")
            face_recog.get_vector(id_user)
            compare.compare_faces(id_user)
            exit()
        elif int(response_user) == 1:
            print("Vamos a utilizar su camara para añadir su cara a la base de datos\n")
            print("Al momento de guardar la imagen, guardarla con su nombre de usuario\n")
            get_face.get_face()
            id_user = input("Introduci un nombre de usuario: ")
            true_register = face_recog.get_vector(id_user)
            if true_register :
                print("Te registraste correctamente, inicia sesion con los datos que proporcionaste")
                continue
            else :
                print("\nInicia sesion con tu nombre de usuario con el que te registrate la primera vez")
                continue
except (KeyboardInterrupt, EOFError):
    print("\nSaliendo del programa")  
    exit(0)  
            
            