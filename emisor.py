# Universidad del Valle de Guatemala
# Redes - CC3067
# Laboratorio 2
# Bryann 19372, Diego 19422, Julio 19402

from copyreg import pickle
import socket
import pickle
import random
from bitarray import bitarray
from fletcher import Fletcher16
from hamming import Hamming

# based on https://realpython.com/python-sockets/

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Enviar cadena
    message = input('Escribe el mensaje:\n')

    detection = input('Que Algoritmo de detección desea usar:\n1-Paridad\n2-Cheksum\n3-Hamming\n')

    # Enviar cadena segura
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    print(f'raw bits:\n{bits}')

    # Paridad
    if detection == "1":
        if (bits.count(1) % 2) == 0:
            parity = 0
        else:
            parity = 1
        bits.append(parity)
    # Fletcher
    elif detection == "2":
        checksum = Fletcher16(bits)
        bits_check = checksum.get_checksum_bits()

        for bit in bits_check:
            bits.append(bit)
    # Hamming
    elif detection == "3":
        hamming = Hamming(bits)
        redundant_bit = hamming.redundant_bit()
        pos_redundant = hamming.get_pos_redundant(redundant_bit)
        parity = hamming.calculate_parity_bits(pos_redundant, redundant_bit)
        bits.clear()
        for bit in parity:
            bits.append(int(bit))

    print(f'secure bits:\n{bits}')

    # RUIDOOOOOOOOO
    error_cont = 0
    for index, bit in enumerate(bits):
        P = 0.001 # Probabilidad de error en cada bit
        error = random.random() < P # P en el rango [0, 1)
        if error:
            print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0
            error_cont += 1

    # Escribir resultados en archivo para metricas
    if error_cont > 0:
        value = "1"
        if detection == "1":
            filename = "./txt_paridad.txt"
        elif detection == "2":
            filename = "./fletcher.py.txt"
        elif detection == "3":
            filename = "./txt_hamming.txt.txt"
    else: 
        value = "0"
        if detection == "1":
            filename = "./txt_paridad.txt"
        elif detection == "2":
            filename = "./fletcher.py.txt"
        elif detection == "3":
            filename = "./txt_hamming.txt.txt"

    with open (filename, "a") as f:
        f.write(value)
        f.close

    # validacion para evitar error en Hamming
    if detection == "3" and error_cont > 1:
        print('Hamming no puede resolver mas de un bit error\n')
        exit()

    print(f'bits a enviar:\n{bits}')

    # Empaquetando bits
    bits_pack = pickle.dumps(bits)

    # Envia al receptor
    s.sendall(bits_pack)

    # Recibe del receptor
    data = s.recv(1024)

print(f"Received {pickle.loads(data)!r}")
