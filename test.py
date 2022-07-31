import pickle
from tabnanny import check
from bitarray import bitarray
from fletcher import Fletcher16
import random

# Enviar cadena
message = input('Escribe el mensaje:\n')

# Enviar cadena segura
bits = bitarray()
bits.frombytes(bytes(message, 'ascii'))
print(bits)

checksum = Fletcher16(bits)
bits_check = checksum.get_checksum_bits()

print(bits_check)
for bit in bits_check:
    bits.append(bit)

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

print(bits_pack)



message = pickle.loads(bits_pack)
print(message)
checksum = Fletcher16(message)
dec_bits = checksum.get_data_bits()
print(dec_bits)
a = dec_bits.tobytes().decode('ascii')
print(a)