# Class for Fletcher's checksum
# Extraido de: https://www.geeksforgeeks.org/fletcher-checksum-implementation-in-python/

class Fletcher16(object):
    def __init__(self, bitarray):
        self.bitarray = bitarray

    def get_checksum(self):
        bitlen = len(self.bitarray)
        sum1 = 0
        sum2 = 0
        for i in range(bitlen):
            sum1 = sum1 + int(self.bitarray[i])
            sum2 = sum2 + sum1
        sum1 = (sum1 % 255) + 1
        sum2 = (sum2 % 255) + 1
        return sum1 * 256 + sum2

    def get_checksum_bits(self):
        checksum = self.get_checksum()
        checksum_bits = []
        for _ in range(16):
            checksum_bits.append(checksum % 2)
            checksum = checksum // 2
        return checksum_bits[::-1]

    def validate_checksum(self):
        checksum_bits = self.bitarray[-16:]
        self.bitarray = self.bitarray[:-16]
        new_checksum_bits = self.get_checksum_bits()
        for i in range(16):
            if checksum_bits[i] != new_checksum_bits[i]:
                return False
        return True

    def get_data_bits(self):
        if self.validate_checksum():
            return self.bitarray
        else:
            return None