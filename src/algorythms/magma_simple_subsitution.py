from rest_framework.serializers import ValidationError
from cached_property import cached_property
from random import randint


SUBSITUTION_BLOCK = [
    (12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1),
    (6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15),
    (11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0),
    (12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11),
    (7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12),
    (5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0),
    (8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7),
    (1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2),
]
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class MagmaSimpleSubsition:
    def __init__(self, keys={}, **kwargs):
        try:
            self.key = int(keys.get('K','').lower(), 16)
        except:
            raise ValidationError('Неверный формат ключа')
        if len(bin(self.key)[2:]) > 256:
            raise ValidationError('Неверная длина ключа')
        self.key = bin(self.key)[2:].zfill(256)


    @cached_property
    def sub_keys(self):
        return [self.key[i * 32:i * 32 + 32] for i in range(8)] # разбиваем на 8 блоков

    def _encrypt_function(self, part:int, key:int):
        '''
        Функция шифрования
        '''
        temp_val = hex((part + key) % (2**32))[2:].zfill(8) # складываем по модулю 2^32
        result = ''
        for i in range(8):
            # производим простую замену по таблице
            result += hex(SUBSITUTION_BLOCK[-(i + 1)][int(temp_val[i],16)])[2:]
        result = bin(int(result,16))[2:].zfill(32)
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
        
        return right_part, left_part

    def _decrypt_subsitution(self, left_part, right_part):
        '''
        Расшифрование простой заменой 
        '''    
        def round_decrypt(left_part, right_part, key):
            '''
            Шифруем правую часть
            XOR с левой
            Меняем местами
            '''
            key = int(key, 2)
            right_part = int(right_part, 2)
            left_part_int = int(left_part, 2)
            return bin(right_part ^ self._encrypt_function(left_part_int, key))[2:].zfill(32), left_part
        
        left_part, right_part = right_part, left_part
        for i in range(8):
            left_part, right_part = round_decrypt(left_part, right_part, self.sub_keys[i])

        for i in range(24):
            left_part, right_part = round_decrypt(left_part, right_part, self.sub_keys[7 - (i % 8)])

        return left_part, right_part


    def encrypt(self, mes):
        try:
            int(mes, 16)
        except:
            mes = bytes(mes, 'utf-8').hex()

        mod = len(mes) % 16
        if mod != 0:
            for i in range((16 - mod) // 2):
                mes += bytes(ENGLISH_ALPHABET[randint(0, len(ENGLISH_ALPHABET) - 1)], 'utf-8').hex()
        

        blocks = [
            bin(int(mes[i * 16:i * 16 + 16], 16))[2:].zfill(64) for i in range(len(mes) // 16)
        ]


        encrypted = ''

        for block in blocks:
            encrypted += ''.join(self._encrypt_subsitution(block[:32], block[32:]))


        return hex(int(encrypted, 2))[2:]
    
    def decrypt(self, mes):

        try:
            int(mes, 16)
        except:
            raise ValidationError('Сообщение должно быть в шестандцатиричном формате')

        mod = len(mes) % 16
        if mod != 0:
            raise ValidationError('Сообщение имеет некорректную длину')


        blocks = [
            bin(int(mes[i * 16:i * 16 + 16], 16))[2:].zfill(64) for i in range(len(mes) // 16)
        ]

        decrypted = ''

        for block in blocks:
            decrypted += ''.join(self._decrypt_subsitution(block[:32], block[32:]))

        return bytearray.fromhex(hex(int(decrypted, 2))[2:]).decode('utf-8')
