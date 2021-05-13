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
        mes_len = len(bytes(mes, 'utf-8').hex())
        mes = bin(int(bytes(mes, 'utf-8').hex(), 16))[2:].zfill(mes_len * 4)
        encrypted = ''
        for l in mes:
            # вычисляем значение мажоритарной функции
            func_result = self._synchronization_func(self.R1[-9], self.R2[-11], self.R3[-11])
            # если значение 8 бита регистра R1 равно значению мажоритарной функции смещаем его
            self.R1 = self._shift_registr(self.R1, func_result, -9, bits_pos=[-19, -18, -17, -14])
            # если значение 10 бита регистра R2 равно значению мажоритарной функции смещаем его
            self.R2 = self._shift_registr(self.R2, func_result, -11, bits_pos=[-22, -21])
            # если значение 10 бита регистра R3 равно значению мажоритарной функции смещаем его
            self.R3 = self._shift_registr(self.R3, func_result, -11, bits_pos=[-23, -22, -21, -8])
            # шифруем бит
            encrypted += str(int(self.R1[0]) ^ int(self.R2[0]) ^ int(self.R3[0]) ^ int(l))

        return hex(int(encrypted, 2))[2:]


    def decrypt(self, mes):
        mes_len = len(mes)
        mes = bin(int(mes, 16))[2:].zfill(mes_len * 4)
        decrypted = ''
        for l in mes:
            func_result = self._synchronization_func(self.R1[-9], self.R2[-11], self.R3[-11])
            self.R1 = self._shift_registr(self.R1, func_result, -9, bits_pos=[-19, -18, -17, -14])
            self.R2 = self._shift_registr(self.R2, func_result, -11, bits_pos=[-22, -21])
            self.R3 = self._shift_registr(self.R3, func_result, -11, bits_pos=[-23, -22, -21, -8])
            decrypted += str(int(self.R1[0]) ^ int(self.R2[0]) ^ int(self.R3[0]) ^ int(l))

        return bytearray.fromhex(hex(int(decrypted, 2))[2:]).decode('utf-8')
