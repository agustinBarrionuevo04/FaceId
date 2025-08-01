# FaceId

El objetivo del proyecto es desarrollar un identidicador de rostros, dichos rostros van a estar cargados en una base de datos (actualmente solo estan cargados en una carpeta con archivos json que tienen la informacion necesaria para realizar la requerido). Funciona todo por consola y en modo local, proximamente lo podemos hostear localmente y que se puedan conectar mediante http y mandar su foto a la base de datos y asi poder registrarse o entrar al sistema.


Requisitos para utilizarlo: 

Tener un entorno virtual en python: python3 -m .venm venm

Dicho entorno virtual tiene que tener instalado:

Opencv: pip install opencv-python3

Face_recognition: pip install face_recognition

Face_recognition_model: pip install git+https://github.com/ageitgey/face_recognition_models

Set_tools = pip install setuptools



The objective of the project is to develop a face identifier. These faces will be stored in a database (currently they are only stored in a folder with JSON files containing the necessary information to perform the required tasks). The system currently works entirely via the console and in local mode. Soon, we plan to host it locally so users can connect via HTTP and send their photo to the database, allowing them to register or log into the system.

Requirements to use it:

Have a Python virtual environment:
python3 -m venv venv

The virtual environment must have the following installed:

pip install opencv-python3  

pip install face_recognition  

pip install git+https://github.com/ageitgey/face_recognition_models  

pip install setuptools  
