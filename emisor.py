import pickle
import socket

class Emisor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.connect((host, port))

    def enviar_cadena(self, mensaje):
        self.socket.send(pickle.dumps(mensaje))

    def enviar_cadena_segura(self, mensaje):
        pass

    def agregar_ruido(self, mensaje):
        pass

    def cerrar(self):
        self.socket.close()
