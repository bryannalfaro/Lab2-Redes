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

    # Enviar cadena segura
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    print(bits)

    # RUIDOOOOOOOOO
    for index, bit in enumerate(bits):
        P = 0.01
        error = random.random() < P # P en el rango [0, 1)
        if error:
            print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0

    print(bits)

    # Empaquetando bits
    bits_pack = pickle.dumps(bits)

    # Envia al receptor
    s.sendall(bits_pack)

    # Recibe del receptor
    data = s.recv(1024)

print(f"Received {data!r}")
