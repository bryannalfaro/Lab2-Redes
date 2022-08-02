from cmath import log
from copyreg import pickle
import socket
import pickle
import random
from bitarray import bitarray
from fletcher import Fletcher16
from hamming import Hamming
import binascii
import matplotlib.pyplot as plt
import pandas as pd

errores = []
palabras = []
probabilidad = []
json = {
    1: "hola",
    2: "hola este mensaje es para probar el lab",
    3: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    4: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
    5: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
}

json_probability = {
    1: 0.01,
    2: 0.1,
    3: 0.4,
    4: 0.6,
    5: 0.7
}

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    # Enviar cadena
    #message = input('Escribe el mensaje:\n')

    #detection = input('Que Algoritmo de detección desea usar:\n1-Paridad\n2-Cheksum\n3-Hamming\n')

    # Enviar cadena segura

for i in json:
    message = json[i]
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    #print(bits)
    #print(bits)
    # RUIDOOOOOOOOO
    palabras.append(str(len(bits)))
    cont = 0
    for index, bit in enumerate(bits):
        '''if cont == 1:
            break'''
        P = 0.2
        error = random.random() < P # P en el rango [0, 1)
        if error:
            #print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0
            cont += 1
    errores.append(cont)

    print("Hubieron", cont, "errores")
    print(errores)
    print(palabras)

plt.bar(palabras,errores)
plt.xlabel('Longitud en bits de palabra')
plt.ylabel('Cantidad de errores')
plt.show()
errores.clear()
for i in json_probability:
    message = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    #print(bits)
    #print(bits)
    # RUIDOOOOOOOOO
    probabilidad.append(str(json_probability[i]))
    cont = 0
    for index, bit in enumerate(bits):
        '''if cont == 1:
            break'''
        P = json_probability[i]
        error = random.random() < P # P en el rango [0, 1)
        if error:
            #print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0
            cont += 1
    errores.append(cont)

    print("Hubieron", cont, "errores")
    print(errores)
    print(probabilidad)

plt.bar(probabilidad,errores)
plt.xlabel('Probabilidad de errores')
plt.ylabel('Cantidad de errores')
plt.show()
        #print(bits)
