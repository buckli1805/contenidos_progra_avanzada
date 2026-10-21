import socket
import funciones
from funciones import Mensaje, Usuario

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(("localhost", 8998))
    mensaje = (Mensaje(Usuario("Javi", 10), "Chupalo", "5"))
    funciones.enviar_mensaje(sock, mensaje)
    datos = funciones.recibir_mensaje(sock)
    print(datos.texto)
except ConnectionError as error:
    print(f"Ocurrio un {error}")
finally:
    sock.close()