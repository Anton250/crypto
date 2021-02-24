class Caesar:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={'R': 1}, **kwargs):
        self.alph = alph
        key = int(keys.get('R', 1))
        self.shift_alph = alph[key:] + alph[:key] # алфавит со смещением

    # функция шифрования
    def encrypt(self, mes):
        encoded = ''
        for l in mes:
            if not l in self.alph:
                encoded += l
                continue
            encoded += self.shift_alph[self.alph.index(l)]
        
        return encoded

    # функция расшифрования
    def decrypt(self, mes):
        decoded = ''
        for l in mes:
            if not l in self.alph:
                decoded += l
                continue
            decoded += self.alph[self.shift_alph.index(l)]
        
        return decoded
