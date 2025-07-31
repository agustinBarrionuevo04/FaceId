import cv2

"""Abrimos la webcam (0 es decir, la default) para obtener la cara 
de la persona y asi luego poder compararla con la base de datos"""

def get_face():
    cv2.namedWindow('Camara - Deteccion Facial', cv2.WINDOW_NORMAL)

    # Cargar el clasificador Haar
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty() == True:
        print ("Error al cargar el clasificardor haar")
        exit()

    # Abrir cámara una sola vez
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara")
        exit()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error al capturar frame")
                break

            # Convertir a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar caras
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            # # Dibujar bounding boxes
            # for (x, y, w, h) in faces:
            #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Mostrar en la misma ventana
            cv2.imshow('Camara - Deteccion Facial', frame)

            # Salir con ESC
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

