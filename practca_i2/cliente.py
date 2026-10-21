import socket
import funciones
from funciones import Mensaje, Usuario

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(("localhost", 8998))
    sock.sendall(funciones.codificar(Mensaje(
        Usuario("Javi", 10), "Chupalo", "5")))
    datos = sock.recv(4096)
    print(funciones.decodificar(datos).texto)
except ConnectionError as error:
    print(f"Ocurrio un {error}")
finally:
    sock.close()