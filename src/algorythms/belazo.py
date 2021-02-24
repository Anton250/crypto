from src.algorythms.tritemy import Tritemy

class Belazo(Tritemy):
    def __init__(self, keys={}, **kwargs):
        super().__init__(**kwargs)
        self.key = keys.get('M')

    def encrypt(self, mes):
        encrypted = ''
        i = 0
        for l in mes:
            encrypted += self.alph_matrix[self.alph.index(self.key[i])][self.alph.index(l)]
            i += 1
            if (i == len(self.key)):
                i = 0

        return encrypted


    def decrypt(self, mes):
        decrypted = ''
        i = 0
        for l in mes:
            decrypted += self.alph[self.alph_matrix[self.alph.index(self.key[i])].index(l)]
            i += 1
            if (i == len(self.key)):
                i = 0

        return decrypted
