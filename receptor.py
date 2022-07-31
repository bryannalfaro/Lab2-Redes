import socket
from bitarray import bitarray
import pickle

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            message = pickle.loads(data)
            detection = input('Que Algoritmo de detección desea usar:\n1-Paridad \n2-Cheksum\n')
            if detection == "1":
                if (message.count(1) % 2) == 1:
                    print("Hay un error en el mensaje")
                    break
            a = message.tobytes().decode('ascii')
            if not data:
                break
            conn.sendall(data)
            break
