from src.algorythms.tritemy import Tritemy

class Belazo(Tritemy):
    def __init__(self, keys={}, **kwargs):
        # генерация таблицы Тритемия происходит в родительском классе
        super().__init__(**kwargs)
        self.key = keys.get('M')

    def encrypt(self, mes):
        encrypted = ''
        i = 0
        key_len = len(self.key)
        for l in mes:
            row = self.alph.index(self.key[i % key_len])
            encrypted += self.alph_matrix[row][self.alph.index(l)]
            i += 1

        return encrypted


    def decrypt(self, mes):
        decrypted = ''
        i = 0
        key_len = len(self.key)
        for l in mes:
            row = self.alph.index(self.key[i % key_len])
            decrypted += self.alph[self.alph_matrix[row].index(l)]
            i += 1

        return decrypted
