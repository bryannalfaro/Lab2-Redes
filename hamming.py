#Class for hamming correction
#Extraido de: https://www.geeksforgeeks.org/hamming-code-implementation-in-python/

class Hamming(object):
    def __init__(self, bitarray):
        self.bitarray = bitarray

    #Calcula el numero de bits redundates
    def redundant_bit(self):
        bitlen = len(self.bitarray)
        for i in range(bitlen):
            if(2**i >= bitlen+i+1):
                return i

    #Encuentra la posicion de los bits redundantes
    def get_pos_redundant(self,redundant):
        bitlen = len(self.bitarray)
        j = 0
        k = 1
        error_pos = ""
        for i in range(1, bitlen+redundant+1):
            if(i == 2**j):
                error_pos = error_pos + "0"
                j = j + 1
            else:
                error_pos = error_pos + self.bitarray[-1*k]
                k = k + 1
        return error_pos[::-1]

    #Calcula bits de paridad
    def calculate_parity_bits(self, array_pos, redundant):
        len_array = len(array_pos)
        for i in range(redundant):
            sum = 0
            for j in range(1, len_array+1):
                if(j & (2**i)==(2**i)):
                    sum = sum ^ int(array_pos[-1*j])
            array_pos = array_pos[:len_array-(2**i)] + str(sum)+array_pos[len_array-(2**i)+1:]

        return array_pos

    #Detecta error
    def detect_error(self,received_arr, redundant):
        len_received = len(received_arr)
        result = ""
        for i in range(redundant):
            sum = 0
            for j in range(1, len_received+1):
                if(j & (2**i)==(2**i)):
                    sum = sum ^ int(received_arr[-1*j])
            result = result + sum*(10**1)
        return int(str(result),2)

