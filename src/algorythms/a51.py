from rest_framework.serializers import ValidationError

class A51:
    def __init__(self, keys={}, **kwargs):
        self.key = bin(int(keys.get('K', ''), 16))[2:].zfill(64)
        
        if len(self.key) > 64:
            raise ValidationError('Ключ не может быть длиннее 64 бит')

        self.R1 = self.key[:19]
        self.R2 = self.key[19:64 - 23]
        self.R3 = self.key[64 - 23:]


    def _synchronization_func(self, x, y, z):
        '''
        Мажоритарная функция
        '''
        return int(x) & int(y) | int(x) & int(z) | int(y) & int(z)
    
    def _shift_registr(self, r, func_result, synchro_pos, bits_pos=[]):
        '''
        Метод для смещения регистра
        '''
        if (int(r[synchro_pos]) == func_result):
            result = int(r[bits_pos[0]])
            for pos in bits_pos[1:]:
                result ^= int(r[pos])
            r = r[1:] + str(result)
        
        return r


    def encrypt(self, mes):
        mes_len = len(bytes(mes, 'utf-8'))
        mes = bin(int(bytes(mes, 'utf-8').hex(), 16))[2:].zfill(mes_len * 4)
        encrypted = ''
        for l in mes:
            func_result = self._synchronization_func(self.R1[8], self.R2[10], self.R3[10])
            self.R1 = self._shift_registr(self.R1, func_result, 8, bits_pos=[18, 17, 16, 13])
            self.R2 = self._shift_registr(self.R2, func_result, 10, bits_pos=[21, 20])
            self.R3 = self._shift_registr(self.R3, func_result, 10, bits_pos=[22, 21, 20, 7])
            encrypted += str(int(self.R1[0]) ^ int(self.R2[0]) ^ int(self.R3[0]) ^ int(l))

        return hex(int(encrypted, 2))[2:]


    def decrypt(self, mes):
        mes_len = len(mes)
        mes = bin(int(mes, 16))[2:].zfill(mes_len * 4)
        decrypted = ''
        for l in mes:
            func_result = self._synchronization_func(self.R1[8], self.R2[10], self.R3[10])
            self.R1 = self._shift_registr(self.R1, func_result, 8, bits_pos=[18, 17, 16, 13])
            self.R2 = self._shift_registr(self.R2, func_result, 10, bits_pos=[21, 20])
            self.R3 = self._shift_registr(self.R3, func_result, 10, bits_pos=[22, 21, 20, 7])
            decrypted += str(int(self.R1[0]) ^ int(self.R2[0]) ^ int(self.R3[0]) ^ int(l))

        return bytearray.fromhex(hex(int(decrypted, 2))[2:]).decode('utf-8')
