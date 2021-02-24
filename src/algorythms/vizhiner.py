from src.algorythms.tritemy import Tritemy

class Vizhiner(Tritemy):
    def __init__(self, keys={}, **kwargs):
        super().__init__(**kwargs)
        self.key = keys.get('t', '')

    def encrypt(self, mes):
        encrypted = ''
        prev_l = self.key
        for l in mes:
            encrypted += self.alph_matrix[self.alph.index(prev_l)][self.alph.index(l)]
            prev_l = l
        
        return encrypted

    
    def decrypt(self, mes):
        decrypted = ''
        prev_l = self.key
        for l in mes:
            decrypted += self.alph[self.alph_matrix[self.alph.index(prev_l)].index(l)]
            prev_l = self.alph[self.alph_matrix[self.alph.index(prev_l)].index(l)]
        
        return decrypted
