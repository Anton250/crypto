from src.algorythms.tritemy import Tritemy

class VizhinerS(Tritemy):
    def __init__(self, keys={}, **kwargs):
        super().__init__(**kwargs)
        self.key = keys.get('t', '')

    def encrypt(self, mes):
        encrypted = ''
        cur_l = self.key
        for l in mes:
            encrypted += self.alph_matrix[self.alph.index(cur_l)][self.alph.index(l)]
            cur_l = self.alph_matrix[self.alph.index(cur_l)][self.alph.index(l)]
        
        return encrypted

    
    def decrypt(self, mes):
        decrypted = ''
        cur_l = self.key
        for l in mes:
            decrypted += self.alph[self.alph_matrix[self.alph.index(cur_l)].index(l)]
            cur_l = l
        
        return decrypted
