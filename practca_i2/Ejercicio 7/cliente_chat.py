import socket
import threading
import funciones
from funciones import Mensaje, Usuario


def escuchar(sock) -> None:
    while True:
        # TODO 1: recibir un mensaje; si es None, avisar que el servidor
        #         se desconectó y salir del loop
        mensaje_recibido = funciones.recibir_mensaje(sock)
        if mensaje_recibido is None:
            print("El servidor se desconecto")
            break
        # TODO 2: imprimirlo como "[sala] nombre: texto"
        print(f"{mensaje_recibido.sala} {mensaje_recibido.autor.nombre}: {mensaje_recibido.texto}")
        


if __name__ == "__main__":
    nombre = input("Tu nombre: ")
    usuario = Usuario(nombre, 0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", 8998))
        # TODO 3: lanzar el thread que escucha (¿daemon o no?)
        cliente_thread = threading.Thread(target=funciones.recibir_mensaje, args=(sock), daemon=True)
        while True:
            texto = input()
            # TODO 4: enviar un Mensaje con ese texto a la sala "general"
            funciones.enviar_mensaje(sock, Mensaje(usuario, texto, "general"))
            

    except ConnectionError:
        print("Se perdió la conexión")
    finally:
        sock.close()