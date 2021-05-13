from functools import reduce
from src.gfield import GField
from cached_property import cached_property
from rest_framework.serializers import ValidationError
from random import randint


SUBSITUTION_BLOCK = (
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46,
    153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142,
    79, 5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72, 171,
    242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135, 21,
    161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177, 50, 117, 25, 61, 255, 53, 138, 126,
    109, 84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3,
    224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68, 26,
    184, 56, 130, 100, 159, 38, 65,173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88,
    179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83,
    170, 144, 202, 216, 133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166,
    116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182,
)

POLYNOM = 2 ** 8 + 2 ** 7 + 2 ** 6 + 2 + 1
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Kuznyechik:
    def __init__(self, keys={}, **kwargs):
        self.key = bin(int(keys.get('K'), 16))[2:].zfill(256)
        self.gfield = GField(8, POLYNOM)


    @cached_property
    def iter_keys(self):
        '''
        Свойство, которое развертывает ключ
        '''
        keys = [
            self.key[:128],
            self.key[128:],
        ]
        prev_val = self.key
        for iteration in range(4):
            for i in range(8):
                iter_const = self._L(bin(i + iteration * 8 + 1)[2:])
                prev_val = prev_val.zfill(256)
                prev_val = ''.join(self._F(prev_val[:128], prev_val[128:], iter_const))  

            prev_val = prev_val.zfill(256)
            keys.extend(
                [
                    prev_val[:128],
                    prev_val[128:]
                ]
            )

        return keys

    def _S(self, block: str):
        '''
        Функия подстановки
        '''
        block = block.zfill(128)
        blocks = [
            int(block[i * 8: i * 8 + 8], 2) for i in range(16)
        ]
        result = ''
        for block in blocks:
            result += bin(SUBSITUTION_BLOCK[block])[2:].zfill(8)
        return result

    def _S_reversed(self, block: str):
        '''
        Функия обратной подстановки
        '''
        block = block.zfill(128)
        blocks = [
            int(block[i * 8: i * 8 + 8], 2) for i in range(16)
        ]
        result = ''
        for block in blocks:
            result += bin(SUBSITUTION_BLOCK.index(block))[2:].zfill(8)
        return result

    def _t(self, blocks: list):
        '''
        Функция для линейного преобразования
        '''
        CONSTANTS = (148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1)
        blocks = [
            (i, b) for i, b in enumerate(blocks)
        ]
        initial = self.gfield.multyplication(blocks[0][1], CONSTANTS[0])
        return bin(reduce(lambda x,y: x ^ self.gfield.multyplication(y[1], CONSTANTS[y[0]]), blocks[1:], initial))[2:].zfill(8)

    def _R(self, block: str):
        '''
        Линейное преобразование с конкатенацией
        '''
        block = block.zfill(128)
        blocks = [
            block[i * 8: i * 8 + 8] for i in range(16)
        ]
        int_blocks = list(map(lambda x: int(x, 2), blocks))
        
        result = self._t(int_blocks) + ''.join(blocks[:15])

        return result

    def _R_reversed(self, block):
        '''
        Обратное линейное преобразование с конкатенацией
        '''
        block = block.zfill(128)
        blocks = [
            block[i * 8: i * 8 + 8] for i in range(16)
        ]
        int_blocks = list(map(lambda x: int(x, 2), blocks))

        result = ''.join(blocks[1:]) + self._t(int_blocks[1:] + [int_blocks[0]])

        return result

    def _L(self, block):
        '''
        Линейное преобразование 16 раз
        '''
        for i in range(16):
            block = self._R(block)
        return block

    def _L_reversed(self, block):
        '''
        Обратное линейное преобразование 16 раз
        '''
        for i in range(16):
            block = self._R_reversed(block)
        return block

    def _F(self, left_part, right_part, key):
        '''
        Функция шифрования
        '''
        int_left_part = int(left_part, 2)
        int_right_part = int(right_part, 2)
        key = int(key, 2)
        int_left_part = int_left_part ^ key
        int_left_part = int(self._L(self._S(bin(int_left_part)[2:].zfill(128)).zfill(128)).zfill(128), 2) ^ int_right_part
        return bin(int_left_part)[2:].zfill(128), left_part.zfill(128)
    
    def _encrypt_function(self, block):
        '''
        Метод для шифрования с использованием итерационных ключей
        '''
        for i in range(9):
            int_block = int(block, 2)
            int_block = int_block ^ int(self.iter_keys[i], 2)
            block = self._L(self._S(bin(int_block)[2:]))
        return bin(int(block,2) ^ int(self.iter_keys[-1], 2))[2:].zfill(128)

    def _decrypt_function(self, block):
        '''
        Метод для расшифрования с использованием итерационных ключей
        '''
        for i in range(9):
            int_block = int(block, 2)
            int_block = int_block ^ int(self.iter_keys[-(i + 1)], 2)
            block = self._S_reversed(self._L_reversed(bin(int_block)[2:]))
        
        return bin(int(block,2) ^ int(self.iter_keys[0], 2))[2:].zfill(128)

    def encrypt(self, mes):
        try:
            int(mes, 16)
        except:
            mes = bytes(mes, 'utf-8').hex()

        mod = len(mes) % 32
        if mod != 0:
            for i in range((32 - mod) // 2):
                mes += bytes(ENGLISH_ALPHABET[randint(0, len(ENGLISH_ALPHABET) - 1)], 'utf-8').hex()

        blocks = [
            bin(int(mes[i * 32:i * 32 + 32], 16))[2:].zfill(128) for i in range(len(mes) // 32)
        ]
        
        encrypted = ''

        for block in blocks:
            encrypted += self._encrypt_function(block)
        
        return hex(int(encrypted, 2))[2:]

    def decrypt(self, mes):
        try:
            int(mes, 16)
        except:
            raise ValidationError('Сообщение должно быть в шестандцатиричном формате')

        mod = len(mes) % 32
        if mod != 0:
            raise ValidationError('Сообщение имеет некорректную длину')


        blocks = [
            bin(int(mes[i * 32:i * 32 + 32], 16))[2:].zfill(128) for i in range(len(mes) // 32)
        ]
        
        decrypted = ''

        for block in blocks:
            decrypted += self._decrypt_function(block)
        
        return bytearray.fromhex(hex(int(decrypted, 2))[2:]).decode('utf-8')
