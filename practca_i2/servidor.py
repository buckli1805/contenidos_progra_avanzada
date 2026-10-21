import socket
import funciones


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8998))
sock.listen()


sock_cliente, address = sock.accept()
print(f"Conexion desde {address}")
mensaje = funciones.recibir_mensaje(sock_cliente)
sala = mensaje.sala
print(f"{sala} {mensaje.autor.nombre}: {mensaje.texto}")
mensaje_servidor = funciones.Mensaje(funciones.Usuario("Servidor",0),
                                      "Recibido", sala)
funciones.enviar_mensaje(sock_cliente, mensaje_servidor)


sock_cliente.close()

sock.close()