import socket
from bitarray import bitarray
import pickle
import binascii
from fletcher import Fletcher16
from hamming import Hamming

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    detection = input('Que Algoritmo de detección desea usar:\n1-Paridad \n2-Cheksum\n3-Hamming\n')
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            message = pickle.loads(data)
            if detection == "1":
                if (message.count(1) % 2) == 1:
                    print("Hay un error en el mensaje")
                    break
                a = message.tobytes().decode('ascii')
            elif detection == "2":
                checksum = Fletcher16(message)
                message = checksum.get_data_bits()
                print(message)
                a = message.tobytes().decode('ascii')
            elif detection == "3":
                print(message)
                hamming = Hamming(message)
                correction = hamming.detect_error(message, hamming.redundant_bit())
                if(correction==0):
                    print("There is no error in the received message.")
                    message = hamming.decalcParityBits(message, hamming.redundant_bit())
                    print(hamming.remove_redundant_bits(message, hamming.redundant_bit()))
                    n = int(hamming.remove_redundant_bits(message, hamming.redundant_bit()), 2)
                    a = binascii.unhexlify('%x' % n)
                else:
                    print("The position of error is ",len(message)-correction,"from the left")
                    print(message)
                    message = list(message)
                    #print(message)
                    message[len(message)-correction] = 1 if message[len(message)-correction]==0 else 0
                    #print(message)
                    for index in range(len(message)):
                        message[index] = str(message[index])
                    message = ''.join(message)
                    #print('debe ser str', message)
                    message = hamming.decalcParityBits(message, hamming.redundant_bit())
                    #print(hamming.remove_redundant_bits(message, hamming.redundant_bit()))
                    # bits string to text
                    n = int(hamming.remove_redundant_bits(message, hamming.redundant_bit()), 2)
                    a = binascii.unhexlify('%x' % n)
            print(a)
            if not data:
                break
            conn.sendall(pickle.dumps(a))
            break
