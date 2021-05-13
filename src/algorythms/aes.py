from functools import reduce
from src.gfield import GField
from cached_property import cached_property
from rest_framework.serializers import ValidationError
from random import randint


SUB_BYTES = [
    ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'], 
    ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'], 
    ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'], 
    ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'], 
    ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'], 
    ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'], 
    ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', 'F7', '50', '3C', '9F', 'A8'], 
    ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'], 
    ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'], 
    ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DE'], 
    ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'], 
    ['E7', 'CB', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'], 
    ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'], 
    ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'], 
    ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'], 
    ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16'],
]

INV_SUB_BYTES = [
    ['52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB'], 
    ['7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB'], 
    ['54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E'], 
    ['08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25'], 
    ['72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92'], 
    ['6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84'], 
    ['90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06'], 
    ['D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B'], 
    ['3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73'], 
    ['96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DE', '6E'], 
    ['47', 'E1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B'], 
    ['FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4'], 
    ['1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F'], 
    ['60', '51', '7E', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF'], 
    ['A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'CB', 'EB', 'BB', '3C', '83', '53', '99', '61'], 
    ['17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D'],
]

POLYNOM = 2 ** 8 + 2 ** 4 + 2 ** 3 + 2 + 1
MULTYPLICATION_CONST = 3 * 2 ** 3 + 2 ** 2 + 2 + 2
INV_MULTYPLICATION_CONST = 11 * 2 ** 3 + 13 *  2 ** 2 + 9 * 2 + 14
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def print_hex_row_from_block(block):
    result = ''
    for i in range(4):
        for j in range(4):
            result += block[j][i]
    print(hex(int(result, 2))[2:])

class AES:
    def __init__(self, keys={}, **kwargs):
        self.key = bin(int(keys.get('K'), 16))[2:].zfill(128)
        self.gfield = GField(8, POLYNOM)

    @cached_property
    def iter_keys(self):
        '''
        Функция для развертывания ключа
        '''
        keys = [
            self.key[i * 32:i * 32 + 32]
            for i in range(4)
        ]
        round_const = int('01000000', 16)
        for i in range(10):
            prev_keys = keys[i * 4:i * 4 + 4]
            first_prev_key = int(prev_keys[0], 2)
            last_prev_key = prev_keys[3]
            last_prev_key = last_prev_key[8:] + last_prev_key[:8]
            last_prev_key = [last_prev_key[i * 8:i * 8 + 8] for i in range(4)]
            for i in range(4):
                row = last_prev_key[i][:4]
                col = last_prev_key[i][4:]
                last_prev_key[i] = bin(int(SUB_BYTES[int(row,2)][int(col,2)], 16))[2:].zfill(8)
            last_prev_key = int(''.join(last_prev_key), 2) ^ round_const
            new_key = last_prev_key ^ first_prev_key
            keys.append(bin(new_key)[2:].zfill(32))
            for i in range(3):
                new_key = new_key ^ int(prev_keys[i+1], 2)
                keys.append(bin(new_key)[2:].zfill(32))
            round_const = hex(round_const)[2:].zfill(8)
            round_const = hex(self.gfield.multyplication(int(round_const[:2], 16), 2))[2:].zfill(2) + round_const[2:]
            round_const = int(round_const, 16)

        return keys


    def _sub_bytes(self, block):
        for i in range(4):
            for j in range(4):
                row = block[i][j][:4]
                col = block[i][j][4:]
                block[i][j] = bin(int(SUB_BYTES[int(row,2)][int(col,2)], 16))[2:].zfill(8)
        return block

    
    def _inv_sub_bytes(self, block):
        for i in range(4):
            for j in range(4):
                row = block[i][j][:4]
                col = block[i][j][4:]
                block[i][j] = bin(int(INV_SUB_BYTES[int(row,2)][int(col,2)], 16))[2:].zfill(8)
        return block


    def _shift_rows(self, block):
        for i in range(4):
            block[i] = block[i][i:] + block[i][:i]
        return block

    def _inv_shift_rows(self, block):
        for i in range(4):
            block[i] = block[i][-i:] + block[i][:-i]
        return block
    
    def _mix_columns(self, block):
        for i in range(4):
            tmp_block = ''
            for j in range(4):
                tmp_block += block[j][i]

            result = bin(self.gfield.multyplication(int(tmp_block, 2), MULTYPLICATION_CONST) % 2**4 + 1)[2:].zfill(32)

            for j in range(4):
                block[j][i] = result[j * 8:j * 8 + 8]
        
        return block

    def _inv_mix_columns(self, block):
        for i in range(4):
            tmp_block = ''
            for j in range(4):
                tmp_block += block[j][i]

            result = bin(self.gfield.multyplication(int(tmp_block, 2), INV_MULTYPLICATION_CONST) % 2**4 + 1)[2:].zfill(32)

            for j in range(4):
                block[j][i] = result[j * 8:j * 8 + 8]
        
        return block

    def _create_matrix_from_row(self, block):
        block = block.zfill(128)
        blocks = [block[i * 8:i * 8 + 8] for i in range(16)]
        matrix = [
            [],
            [],
            [],
            [],
        ]

        for i in range(4):
            for j in range(4):
                matrix[j].append(blocks[i * 4 + j])
        
        return matrix
    
    def _sum_with_key(self, block, key):
        for i in range(4):
            for j in range(4):
                block[i][j] = bin(int(block[i][j], 2) ^ int(key[i][j], 2))[2:].zfill(8)
        
        return block

    def _encrypt_function(self, block):
        block = self._create_matrix_from_row(block)
        key = self._create_matrix_from_row(''.join(self.iter_keys[:4]))

        block = self._sum_with_key(block, key)

        for i in range(9):
            block = self._sub_bytes(block)
            block = self._shift_rows(block)
            print_hex_row_from_block(block)
            block = self._mix_columns(block)
            key = self._create_matrix_from_row(''.join(self.iter_keys[(i + 1) * 4: (i + 1) * 4 + 4]))
            block = self._sum_with_key(block, key)
        
        block = self._sub_bytes(block)
        block = self._shift_rows(block)
        key = self._create_matrix_from_row(''.join(self.iter_keys[40:]))
        block = self._sum_with_key(block, key)

        result = ''
        
        for i in range(4):
            for j in range(4):
                result += block[j][i]

        return result

    def _decrypt_function(self, block):
        block = self._create_matrix_from_row(block)
        key = self._create_matrix_from_row(''.join(self.iter_keys[40:]))

        block = self._sum_with_key(block, key)

        for i in range(9):
            block = self._inv_shift_rows(block)
            block = self._inv_sub_bytes(block)
            key = self._create_matrix_from_row(''.join(self.iter_keys[-(i + 2) * 4: -(i + 2) * 4 - 4]))
            block = self._sum_with_key(block, key)
            block = self._inv_mix_columns(block)
        
        block = self._inv_shift_rows(block)
        block = self._inv_sub_bytes(block)
        key = self._create_matrix_from_row(''.join(self.iter_keys[:4]))
        block = self._sum_with_key(block, key)

        result = ''
        
        for i in range(4):
            for j in range(4):
                result += block[j][i]

        return result


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

