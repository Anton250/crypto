from rest_framework.serializers import ValidationError
from cached_property import cached_property
from math import ceil, pow

C1 = int('00000001000000010000000100000100', 2)
C2 = int('00000001000000010000000100000001', 2)
SUBSITUTION_BLOCK = [
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
    (12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1),
    (6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15),
    (11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0),
    (12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11),
    (7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12),
    (5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0),
    (8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7),
    (1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2),
]

class MagmaGamma:
    def __init__(self, keys={}, **kwargs):
        try:
            self.key = int(keys.get('K','').lower(), 16)
        except:
            raise ValidationError('Неверный формат ключа')
        if len(bin(self.key)[2:]) > 256:
            raise ValidationError('Неверная длина ключа')
        self.key = bin(self.key)[2:].zfill(256)
        try:
            self.synchro = int(keys.get('S', '').lower(), 16)
        except:
            raise ValidationError('Неверный формат синхропосылки')
        if len(bin(self.synchro)[2:]) > 64:
            raise ValidationError('Неверная длина синхропосылки')
        self.synchro = bin(self.synchro)[2:].zfill(64)


    @cached_property
    def sub_keys(self):
        return [self.key[i * 32:i * 32 + 32] for i in range(8)] # разбиваем на 8 блоков

    def _encrypt_function(self, part:int, key:int):
        '''
        Функция шифрования
        '''
        temp_val = bin((part + key) % (2**32))[2:].zfill(32) # складываем по модулю 2^32
        result = ''
        for i in range(8):
            # производим простую замену по таблице
            result += bin(SUBSITUTION_BLOCK[i + 1][SUBSITUTION_BLOCK[0].index(int(temp_val[i * 4:i * 4 + 4],2))])[2:].zfill(4)
        result = result[11:] + result[:11] # циклический сдвиг на 11 бит
        return int(result, 2)
        

    def _encrypt_subsitution(self, left_part, right_part):
        '''
        Шифрование простой заменой 
        '''    
        def round_encrypt(left_part, right_part, key):
            '''
            Шифруем правую часть
            XOR с левой
            Меняем местами
            '''
            key = int(key, 2)
            left_part = int(left_part, 2)
            right_part_int = int(right_part, 2)
            return right_part, bin(left_part ^ self._encrypt_function(right_part_int, key))[2:].zfill(32)
        

        for i in range(24):
            # 24 итерации шифрования
            left_part, right_part = round_encrypt(left_part, right_part, self.sub_keys[i % 8])

        for i in range(8):
            # в последних 8 итерациях подключи используем в другом порядке
            left_part, right_part = round_encrypt(left_part, right_part, self.sub_keys[7 - i])

        return left_part, right_part
    
    def gamma_overlay(self, mes):
        try:
            int(mes, 16)
        except:
            raise ValidationError('Сообщение должно быть в шестнадцатиричном формате')
        result = ''
        # разбиваем на блоки
        blocks = [
            mes[i * 16:i * 16 + 16]
            for i in range(ceil(len(mes)/16))
        ]

        N1, N2 = self.synchro[:32], self.synchro[32:] # заполняем начальными значениями
        N3, N4 = self._encrypt_subsitution(N2, N1) # заполняем начальными значениями N3 и N4


        for block in blocks:
            # складываем значение из N4 с константой C1 по модулю 2^32 - 1
            N4 = bin((int(N4,2) + C1) % int((2**32 - 1)))[2:].zfill(32)
            # складываем значение из N3 с константой C2 по модулю 2^32
            N3 = bin((int(N3,2) + C2) % int(2**32))[2:].zfill(32)
            N1, N2 = N3, N4
            # получаем гамму в двоичном формате
            gamma = ''.join(self._encrypt_subsitution(N2, N1)[::-1])
            # если длина блока меньше 64, то обрезаем гамму
            if len(gamma) > len(block):
                gamma = gamma[:len(block)]
            # XOR гаммы с блоком
            result += hex(int(gamma, 2) ^ int(block, 16))[2:].zfill(len(block) // 4)
        
        return result

    def encrypt(self, mes):
        try:
            int(mes, 16)
        except:
            mes = bytes(mes, 'utf-8').hex()
        
        return self.gamma_overlay(mes)
    
    def decrypt(self, mes):
        
        return bytearray.fromhex(self.gamma_overlay(mes)).decode('utf-8')
