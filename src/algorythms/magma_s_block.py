from random import randint
SUBSITUTION_BLOCK = [
    (1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2),
    (8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7),
    (5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0),
    (7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12),
    (12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11),
    (11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0),
    (6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15),
    (12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1),
]
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class MagmaSubsitution:
    def __init__(self, **kwargs):
        pass

    def encrypt(self, mes):
        try:
            int(mes, 16)
        except:
            mes = bytes(mes, 'utf-8').hex()
        mod = len(mes) % 8
        if mod != 0:
            # дополняем буквами
            for i in range((8 - mod) // 2):
                mes += bytes(ENGLISH_ALPHABET[randint(0, len(ENGLISH_ALPHABET) - 1)], 'utf-8').hex()
        
        encrypted = ''
        # разбиваем на 8-байтовые блоки
        blocks = [mes[i * 8:i * 8 + 8] for i in range(len(mes) // 8)]
        for i in range(len(blocks)):
            block = blocks[i]
            for j in range(8):
                # заменяем j-ый байт i-ого блока
                encrypted += hex(SUBSITUTION_BLOCK[j][int(block[j],16)])[2:]
            
        return encrypted

    def decrypt(self, mes):
        decrypted = ''
        # разбиваем на 8-байтовые блоки
        blocks = [mes[i * 8:i * 8 + 8] for i in range(len(mes) // 8)]
        for i in range(len(blocks)):
            block = blocks[i]
            for j in range(8):
                # выполняем обратную замену j-ого байта i-ого блока
                decrypted += hex(SUBSITUTION_BLOCK[j].index(int(block[j],16)))[2:]
            
        decrypted = bytearray.fromhex(decrypted.lower()).decode('utf-8')
        return decrypted
    