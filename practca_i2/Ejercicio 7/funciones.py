import json
import pickle
from threading import Lock

class Usuario:
    def __init__(self, nombre: str, id_: int):
        self.nombre = nombre
        self.id_ = id_

class Mensaje:
    def __init__(self, autor: Usuario, texto: str, sala: str):
        self.autor = autor        # ¡es otra instancia!
        self.texto = texto
        self.sala = sala

class ChatEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, Usuario):
            return {"nombre": obj.nombre, "id_": obj.id_, "tipo": "Usuario"}
        elif isinstance(obj, Mensaje):
            return {"autor": obj.autor, "texto": obj.texto, "sala": obj.sala, "tipo": "Mensaje"}
        return super().default(obj)


def chat_hook(dic):
    if dic.get("tipo") == "Usuario":
        return Usuario(dic["nombre"], dic["id_"])
    elif dic.get("tipo") == "Mensaje":
        return Mensaje(dic["autor"], dic["texto"], dic["sala"])
    return dic

def procesar_entrada(texto: str):
    try:
        return json.loads(texto, object_hook=chat_hook)
    except json.JSONDecodeError:
        print("Mensaje corrupto")
        return None



class Sala:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.historial = []          # lista de Mensaje → SÍ se guarda
        self.conectados = {}         # {id_usuario: socket} → NO se puede guardar
        self.lock = Lock()           # NO se puede serializar
        self.veces_cargada = 0
    def __getstate__(self):
        nuevo = self.__dict__.copy()
        del nuevo["conectados"]
        del nuevo["lock"]
        return nuevo
    def __setstate__(self, state):
        state["lock"] = Lock()
        state["conectados"] = {}
        state["veces_cargada"] += 1
        self.__dict__ = state


def guardar_sala(sala, ruta):
    with open(ruta, "wb") as archivo:
        pickle.dump(sala, archivo)

def cargar_sala(ruta):
    with open(ruta, "rb") as archivo:
        sala = pickle.load(archivo)
        return sala


def codificar(mensaje: Mensaje) -> bytes:
    contenido = json.dumps(mensaje, cls=ChatEncoder).encode("utf-8")
    largo = len(contenido).to_bytes(4, "big")
    return largo + contenido

def decodificar(datos: bytes) -> Mensaje:
    largo = int.from_bytes(datos[:4], "big")

    contenido = datos[4: largo + 4]
    contenido_final = contenido.decode("UTF-8")
    return json.loads(contenido_final, object_hook=chat_hook)
    
def dividir_en_chunks(datos: bytes, tamano: int) -> list:
    chunk = 0
    lista = []
    for i in range(0, len(datos), tamano):
        chunk = datos[i:i+ tamano]
        lista.append(chunk)
    return lista 

def enviar_mensaje(sock, mensaje: Mensaje) -> None:
    mensaje_codificado = codificar(mensaje)
    sock.sendall(mensaje_codificado)

def recibir_mensaje(sock) -> Mensaje:
    # 1. Encabezado: los primeros 4 bytes dicen cuánto mide el contenido
    largo = int.from_bytes(sock.recv(4), "big")

    # 2. Contenido: juntar bytes hasta tener exactamente 'largo'
    datos = bytearray()
    while len(datos) < largo:
        bytes_leer = min(4096, largo - len(datos))
        datos.extend(sock.recv(bytes_leer))

    # 3. bytes → str JSON → Mensaje
    texto = datos.decode("utf-8")
    return procesar_entrada(texto)



