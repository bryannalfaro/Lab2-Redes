# Universidad del Valle de Guatemala
# Redes - CC3067
# Laboratorio 2
# Bryann 19372, Diego 19422, Julio 19402

import random
from bitarray import bitarray
import matplotlib.pyplot as plt

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

# Grafica cantidad de errores por longitud de palabra
for i in json:
    message = json[i]
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    # RUIDOOOOOOOOO
    palabras.append(str(len(bits)))
    cont = 0
    for index, bit in enumerate(bits):
        '''# forzar a un solo bit de error
        if cont == 1:
            break'''
        P = 0.2
        error = random.random() < P # P en el rango [0, 1)
        if error:
            #print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0
            cont += 1
    errores.append(cont)

    print("Hubieron", cont, "errores en la oracion ", i, "con ", palabras[i-1], " palabras")
    #print(errores)
    #print(palabras)

plt.bar(palabras,errores)
plt.xlabel('Longitud en bits de palabra')
plt.ylabel('Cantidad de errores')
plt.show()
print()

# Grafica cantidad de errores por probabilidad de error en cada bit
errores.clear()
for i in json_probability:
    message = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    bits = bitarray()
    bits.frombytes(bytes(message, 'ascii'))
    # RUIDOOOOOOOOO
    probabilidad.append(str(json_probability[i]))
    cont = 0
    for index, bit in enumerate(bits):
        '''# forzar a un solo bit de error
        if cont == 1:
            break'''
        P = json_probability[i]
        error = random.random() < P # P en el rango [0, 1)
        if error:
            #print(f'da error en pos {index}')
            bits[index] = 1 if bits[index] == 0 else 0
            cont += 1
    errores.append(cont)

    print("Hubieron", cont, "errores para la probabilidad ", probabilidad[i-1])
    #print(errores)
    #print(probabilidad)

plt.bar(probabilidad,errores)
plt.xlabel('Probabilidad de errores')
plt.ylabel('Cantidad de errores')
plt.show()
print()

# Grafica de Porcentaje de exito entre emisor y receptor segun cantidad de mensajes correctos/con error
algorithms = ["Paridad Simple", "Fletcher", "Hamming"]
percents = []

error_detected = 0
errors_detected_recep = 0

with open("./txt_paridad.txt") as f:
    for line in f.readline():
        if line == "1":
            error_detected += 1

with open("./txt_paridad_recep.txt") as f:
    for line in f.readline():
        if line == "1":
            errors_detected_recep += 1

error_p = (errors_detected_recep / error_detected) * 100
percents.append(error_p)

print("porcentaje de errores que detecto el algoritmo de Paridad Simple:")
print(error_p, "%")
error_detected = 0
errors_detected_recep = 0

with open("./txt_fletcher.txt") as f:
    for line in f.readline():
        if line == "1":
            error_detected += 1

with open("./txt_fletcher_recep.txt") as f:
    for line in f.readline():
        if line == "1":
            errors_detected_recep += 1

error_p = (errors_detected_recep / error_detected) * 100
percents.append(error_p)

print("porcentaje de errores que detecto el algoritmo de Fletcher:")
print(error_p, "%")
error_detected = 0
errors_detected_recep = 0

with open("./txt_hamming.txt") as f:
    for line in f.readline():
        if line == "1":
            error_detected += 1

with open("./txt_hamming_recep.txt") as f:
    for line in f.readline():
        if line == "1":
            errors_detected_recep += 1

error_p = (errors_detected_recep / error_detected) * 100
percents.append(error_p)
print("porcentaje de errores que detecto el algoritmo de Hamming:")
print(error_p, "%")

plt.bar(algorithms, percents)
plt.ylabel('Porcentaje de aciertos')
plt.xlabel('Algoritmos')
plt.show()
