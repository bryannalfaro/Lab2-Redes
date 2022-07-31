from cmath import log
from copyreg import pickle
import socket
import pickle
import random
from bitarray import bitarray

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Enviar cadena
    message = input('Escribe el mensaje:\n')

    detection = input('Que Algoritmo de detección desea usar:\n1-Paridad \n2-Cheksum\n')

    # Enviar cadena segura
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    print(bits)


    if detection == "1":
        if (bits.count(1) % 2) == 0:
            parity = 0
        else:
            parity = 1

    # RUIDOOOOOOOOO
    for index, bit in enumerate(bits):
        P = 0.01
        error = random.random() < P # P en el rango [0, 1)
        if error:
            print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0

    if detection == "1":
        bits.append(parity)

    print(bits)

    # Empaquetando bits
    bits_pack = pickle.dumps(bits)

    # Envia al receptor
    s.sendall(bits_pack)

    # Recibe del receptor
    data = s.recv(1024)

print(f"Received {data!r}")
