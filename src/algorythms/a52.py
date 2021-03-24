from rest_framework.serializers import ValidationError

class A52:
    def __init__(self, keys={}, **kwargs):
        self.key = bin(int(keys.get('K', ''), 16))[2:].zfill(64)
        
        if len(self.key) > 64:
            raise ValidationError('Ключ не может быть длиннее 64 бит')

        self.R1 = self.key[:19]
        self.R2 = self.key[19:64 - 23]
        self.R3 = self.key[64 - 23:]
        self.R4 = keys.get('R4', '').zfill(17)

        if len(self.R4) > 17:
            raise ValidationError('Регистр R4 не может быть длиннее 17 бит')


    def _synchronization_func(self, x, y, z):
        '''
        Мажоритарная функция
        '''
        return int(x) & int(y) | int(x) & int(z) | int(y) & int(z)
    
    def _shift_registr_with_condition(self, r, func_result, synchro_pos, bits_pos=[]):
        '''
        Метод для смещения регистра с условием
        '''
        if (int(self.R4[synchro_pos]) == func_result):
            r = self._shift_registr(r, bits_pos=bits_pos)

        return r

    def _shift_registr(self, r, bits_pos=[]):
        '''
        Метод для смещения регистра
        '''
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
            func_result = self._synchronization_func(self.R4[10], self.R4[7], self.R3[3])
            self.R1 = self._shift_registr_with_condition(self.R1, func_result, 10, bits_pos=[18, 17, 16, 13])
            self.R2 = self._shift_registr_with_condition(self.R2, func_result, 7, bits_pos=[21, 20])
            self.R3 = self._shift_registr_with_condition(self.R3, func_result, 3, bits_pos=[22, 21, 20, 7])
            self.R4 = self._shift_registr(self.R4, bits_pos=[16, 11])
            encrypted += str(
                self._synchronization_func(self.R1[15], self.R1[14], self.R1[12]) ^\
                self._synchronization_func(self.R2[16], self.R2[13], self.R2[9]) ^\
                self._synchronization_func(self.R3[18], self.R3[16], self.R3[13]) ^\
                int(l)
            )
        return hex(int(encrypted, 2))[2:]


    def decrypt(self, mes):
        mes_len = len(mes)
        mes = bin(int(mes, 16))[2:].zfill(mes_len * 4)
        decrypted = ''
        for l in mes:
            func_result = self._synchronization_func(self.R4[10], self.R4[7], self.R3[3])
            self.R1 = self._shift_registr_with_condition(self.R1, func_result, 10, bits_pos=[18, 17, 16, 13])
            self.R2 = self._shift_registr_with_condition(self.R2, func_result, 7, bits_pos=[21, 20])
            self.R3 = self._shift_registr_with_condition(self.R3, func_result, 3, bits_pos=[22, 21, 20, 7])
            self.R4 = self._shift_registr(self.R4, bits_pos=[16, 11])
            decrypted += str(
                self._synchronization_func(self.R1[15], self.R1[14], self.R1[12]) ^\
                self._synchronization_func(self.R2[16], self.R2[13], self.R2[9]) ^\
                self._synchronization_func(self.R3[18], self.R3[16], self.R3[13]) ^\
                int(l)
            )
        return bytearray.fromhex(hex(int(decrypted, 2))[2:]).decode('utf-8')
