from random import randint

class Cardano:
    def __init__(self, keys={}, **kwargs):
        self.key = keys.get('R')
        self.alph = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        # add check key

    
    # перевернуть по вертикали
    def rotate_vertical(self):
        for i in range(len(self.key)):
            for j in range(len(self.key[i]) // 2):
                self.key[i][j], self.key[i][-(j + 1)] = self.key[i][-(j + 1)], self.key[i][j]

    # перевернуть по горизонтали
    def rotate_horizontal(self):
        for i in range(len(self.key) // 2):
            self.key[i], self.key[-(i + 1)] = self.key[-(i + 1)], self.key[i]

        
    def create_table(self):
        table = []

        for i in range(len(self.key)):
            table.append([])
            for j in range(len(self.key[0])):
                table[i].append('')
            
        return table
        

    def encrypt(self, mes):
        encrypted = ''
        max_len = len(self.key) * len(self.key[0])
        if len(mes) > max_len:
            raise ValueError('Сообщение больше карточки')
        
        if len(mes) % max_len != 0:
            for i in range(max_len - len(mes) % max_len):
                mes += self.alph[randint(0, len(self.alph) - 1)]
        
        table = self.create_table()

        l = 0
        for r in range(4):
            for i, row in enumerate(self.key):
                for j, col in enumerate(row):
                    if int(col) == 1:
                        table[i][j] = mes[l]
                        l += 1
            if r == 0:
                self.rotate_horizontal()
                self.rotate_vertical()
                continue
            elif r == 1:
                self.rotate_vertical()
            elif r == 2:
                self.rotate_horizontal()
                self.rotate_vertical()
            else:
                self.rotate_vertical()

        for row in table:
            for col in row:
                encrypted += col
        
        return encrypted


    def decrypt(self, mes):
        decrypted = ''
        if len(mes) != len(self.key) * len(self.key[0]):
            raise ValueError('Неправильная длина сообщения')
        
        table = self.create_table()

        l = 0

        for i in range(len(self.key)):
            for j in range(len(self.key[0])):
                table[i][j] = mes[l]
                l += 1

        for r in range(4):
            for i, row in enumerate(self.key):
                for j, col in enumerate(row):
                    if int(col) == 1:
                        decrypted += table[i][j]
            if r == 0:
                self.rotate_horizontal()
                self.rotate_vertical()
                continue
            elif r == 1:
                self.rotate_vertical()
            elif r == 2:
                self.rotate_horizontal()
                self.rotate_vertical()
            else:
                self.rotate_vertical()

        return decrypted
