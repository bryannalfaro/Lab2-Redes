from emisor import *
from receptor import *

emisor = Emisor('192.168.1.14', 3030)

emisor.enviar_cadena('Hola')

receptor = Receptor('localhost', 3030)
print(receptor.recibir_cadena())