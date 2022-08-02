from cmath import log
from copyreg import pickle
import socket
import pickle
import random
from bitarray import bitarray
from fletcher import Fletcher16
from hamming import Hamming
import binascii

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Enviar cadena
    message = input('Escribe el mensaje:\n')

    detection = input('Que Algoritmo de detección desea usar:\n1-Paridad\n2-Cheksum\n3-Hamming\n')

    # Enviar cadena segura
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    print(bits)

    if detection == "1":
        if (bits.count(1) % 2) == 0:
            parity = 0
        else:
            parity = 1
    elif detection == "2":
        checksum = Fletcher16(bits)
        bits_check = checksum.get_checksum_bits()

        for bit in bits_check:
            bits.append(bit)
    elif detection == "3":
        hamming = Hamming(bits)
        red_bit = hamming.redundant_bit()
        post_red = hamming.get_pos_redundant(red_bit)
        parity = hamming.calculate_parity_bits(post_red, red_bit)
        bits.clear()
        for bit in parity:
            bits.append(int(bit))

    print(bits)
    # RUIDOOOOOOOOO
    cont = 0
    for index, bit in enumerate(bits):
        P = 0.2
        error = random.random() < P # P en el rango [0, 1)
        if error:
            print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0
            cont += 1

    if cont > 0:
        if detection == "1":
            with open ('./txt_paridad.txt', "a") as f:
                f.write('1')
                f.close
        elif detection == "2":
            with open ('./fletcher.py.txt', "a") as f:
                f.write('1')
                f.close
        elif detection == "3":
            with open ('./txt_hamming.txt.txt', "a") as f:
                f.write('1')
                f.close
    else: 
        if detection == "1":
            with open ('./txt_paridad.txt', "a") as f:
                f.write('0')
                f.close
        elif detection == "2":
            with open ('./fletcher.py.txt', "a") as f:
                f.write('0')
                f.close
        elif detection == "3":
            with open ('./txt_hamming.txt.txt', "a") as f:
                f.write('0')
                f.close


    if detection == "1":
        bits.append(parity)
    elif detection == "3":
        if cont > 1:
            print('Hamming no puede resolver mas de un bit error')
            exit()

    print(bits)

    # Empaquetando bits
    bits_pack = pickle.dumps(bits)

    # Envia al receptor
    s.sendall(bits_pack)

    # Recibe del receptor
    data = s.recv(1024)

print(f"Received {pickle.loads(data)!r}")
