import socket
import threading
import funciones


class Servidor:
    def __init__(self, host: str, port: int) -> None:
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((host, port))
        self.socket_servidor.listen()
        self.clientes = {}              # {address: sock_cliente}
        self.lock = threading.Lock()
        print(f"Servidor escuchando en {host}:{port}")

    def aceptar_clientes(self) -> None:
        while True:
            # TODO 1: aceptar un cliente
            sock_cliente, addres = self.socket_servidor.accept()

            # TODO 2: agregarlo a self.clientes (¿con o sin lock?)
            with self.lock:
                self.clientes[addres] = sock_cliente
            # TODO 3: crear y lanzar un thread que ejecute self.atender_cliente
            #         con el socket de ese cliente y su address
            thread_cliente = threading.Thread(target=self.atender_cliente, args=(sock_cliente, addres), daemon=True)
            thread_cliente.start()

    def atender_cliente(self, sock_cliente, address) -> None:
        print(f"Nuevo cliente: {address}")
        while True:
            # TODO 4: recibir un mensaje del cliente
            mensaje = funciones.recibir_mensaje(sock_cliente)
            # TODO 5: si es None → desconectar: sacarlo de self.clientes,
            #         cerrar su socket, imprimir aviso y salir del loop
            if mensaje is None:
                with self.lock:
                    del self.clientes[address]
                sock_cliente.close()
                print("No llego ningun mensaje")
                break
            # TODO 6: si no, imprimirlo y llamar a self.reenviar(mensaje)
            print(f"{mensaje.texto}")
            self.reenviar(mensaje)

    def reenviar(self, mensaje) -> None:
        # TODO 7: enviar el mensaje a TODOS los clientes conectados
        with self.lock:
            for addres_entrada in self.clientes:
                funciones.enviar_mensaje(self.clientes[addres_entrada], mensaje) 


if __name__ == "__main__":
    servidor = Servidor("localhost", 8998)
    servidor.aceptar_clientes()