from src.algorythms.tritemy import Tritemy

class Belazo(Tritemy):
    def __init__(self, keys={}, **kwargs):
        super().__init__(**kwargs)
        self.key = keys.get('M')

    def encrypt(self, mes):
        encrypted = ''
        i = 0
        key_len = len(self.key)
        for l in mes:
            encrypted += self.alph_matrix[self.alph.index(self.key[i % key_len])][self.alph.index(l)]
            i += 1

        return encrypted


    def decrypt(self, mes):
        decrypted = ''
        i = 0
        key_len = len(self.key)
        for l in mes:
            decrypted += self.alph[self.alph_matrix[self.alph.index(self.key[i % key_len])].index(l)]
            i += 1

        return decrypted
