# Universidad del Valle de Guatemala
# Redes - CC3067
# Laboratorio 2
# Bryann 19372, Diego 19422, Julio 19402

import socket
import pickle
import binascii
from fletcher import Fletcher16
from hamming import Hamming

# based on https://realpython.com/python-sockets/

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
            detection = input('Que Algoritmo de detección está recibiendo?:\n1-Paridad \n2-Cheksum\n3-Hamming\n')
            result = ""

            # Paridad
            if detection == "1":
                filename = "./txt_paridad_recep.txt"
                if (message.count(1) % 2) == 1:
                    print("Hay un error en el mensaje")
                    value = "1"
                else:
                    message.pop()
                    result = message.tobytes().decode('ascii')
                    value = "0"
                with open (filename, "a") as f:
                    f.write(value)
                    f.close

            # Fletcher
            elif detection == "2":
                checksum = Fletcher16(message)
                message = checksum.get_data_bits()
                filename = "./txt_fletcher_recep.txt"
                if message == None:
                    print("Hay un error en el mensaje")
                    value = "1"
                else:
                    result = message.tobytes().decode('ascii')
                    value = "0"
                with open (filename, "a") as f:
                    f.write(value)
                    f.close

            # Hamming
            elif detection == "3":
                hamming = Hamming(message)
                correction = hamming.detect_error(message, hamming.redundant_bit())
                filename = "./txt_hamming_recep.txt"
                if correction == 0:
                    message = hamming.decalcParityBits(message, hamming.redundant_bit())
                    bits_message = int(hamming.remove_redundant_bits(message, hamming.redundant_bit()), 2)
                    result = binascii.unhexlify('%x' % bits_message)
                    value = "0"
                else:
                    print("Hay un error en el mensaje")
                    print("La posicion del error es ", len(message)-correction, " desde la derecha")
                    # Arreglando bit
                    message = list(message)
                    message[len(message)-correction] = 1 if message[len(message)-correction]==0 else 0
                    for index in range(len(message)):
                        message[index] = str(message[index])
                    message = ''.join(message)
                    # decodeando parity bits
                    message = hamming.decalcParityBits(message, hamming.redundant_bit())
                    # bits string to text
                    n = int(hamming.remove_redundant_bits(message, hamming.redundant_bit()), 2)
                    result = binascii.unhexlify('%x' % n)
                    value = "1"
                with open (filename, "a") as f:
                    f.write(value)
                    f.close
            if not data:
                break
            if result:
                print(result)
                conn.sendall(pickle.dumps(result))
            break
