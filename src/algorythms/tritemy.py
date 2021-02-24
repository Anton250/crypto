class Tritemy:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', **kwargs):
        self.alph = alph
        self.alph_matrix = [
            alph[shift:] + alph[:shift]
            for shift in range(len(alph))
        ]

    def encrypt(self, mes):
        encrypted = ''
        i = 0
        for l in mes:
            encrypted += self.alph_matrix[i][self.alph.index(l)]
            i += 1
            if (i == len(self.alph)):
                i = 0
        
        return encrypted
    
    def decrypt(self, mes):
        decrypted = ''
        i = 0
        for l in mes:
            decrypted += self.alph[self.alph_matrix[i].index(l)]
            i += 1
            if (i == len(self.alph)):
                i = 0
        
        return decrypted

        