import pickle
import socket

class Receptor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def recibir_cadena(self):
        return pickle.loads(self.socket.recv(1024))

    def cerrar(self):
        self.socket.close()

