class Tritemy:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', **kwargs):
        self.alph = alph
        # генерируем таблицу Тритемия
        self.alph_matrix = [
            alph[shift:] + alph[:shift]
            for shift in range(len(alph))
        ]

    def encrypt(self, mes):
        '''
        Функция шифрования
        '''
        encrypted = ''
        i = 0
        for l in mes:
            encrypted += self.alph_matrix[i % len(self.alph)][self.alph.index(l)]
            i += 1
        
        return encrypted
    
    def decrypt(self, mes):
        '''
        Функция расшифрования
        '''
        decrypted = ''
        i = 0
        for l in mes:
            decrypted += self.alph[self.alph_matrix[i % len(self.alph)].index(l)]
            i += 1
        
        return decrypted
