import requests
import json
import face_recognition
import conn_db, face_recog, get_face

def main():
    print("\n***En caso de querer salir del programa preciona Ctrl+C o Ctrl+D***")

    try:
        while True:
            response_user = input(
                "\nIniciar sesion = 0 o Registrarse = 1\n").strip()

            if response_user not in ("0", "1"):
                print("Opción inválida, intenta nuevamente.")
                continue

            print("Vamos a utilizar su camara para obtener su id\n")
            vector = face_recog.get_vector(get_face.get_face())
            vector_string = conn_db.np_array_to_Json(vector)

            url_verify = "https://https://faceidapi.onrender.com/procesar-vector"
            payload_verify = {"vector": vector_string}

            response = requests.post(url_verify, json=payload_verify)

            if response.status_code != 200:
                print(
                    f"Error en el servidor ({response.status_code}): {response.text}")
                continue

            data = response.json()
            val = data.get("Exist")
            name_db = data.get("Name")

            if response_user == "0":
                if val:
                    print(
                        f"Bienvenido {name_db}, que gusto verte de nuevo :)!!")
                    exit(0)
                else:
                    print("No te encontramos en la base. Prueba registrándote.")
                    continue

            elif response_user == "1":
                if val:
                    print(
                        f"Ya estás registrado como {name_db}. Iniciá sesión.")
                    continue
                else:
                    name = input("Introducí un nombre de usuario: ").strip()

                    url_register = "https://https://faceidapi.onrender.com/register"
                    payload_register = {"vector": vector_string, "name": name}

                    response_reg = requests.post(
                        url_register, json=payload_register)

                    if response_reg.status_code == 200:
                        data_reg = response_reg.json()
                        print(f"{data_reg.get('message')}")
                    else:
                        print(
                            f"Error registrando usuario ({response_reg.status_code}): {response_reg.text}")

    except (KeyboardInterrupt, EOFError):
        print("\nSaliendo del programa...")
        exit(0)


main()
    




    
    
