class Poliby:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', **kwargs):
        # подыскиваем сторону квадрата
        for i in range(len(alph)):
            if i**2 >= len(alph):
                self.side = i
                break
        
        self.encode_alph = {}
        self.decode_alph = {}

        # составляем словари с шифрвеличинами и шифробозначениями
        for i in range(self.side):
            for j in range(self.side):
                ind = (i * self.side) + j
                if ind >= len(alph):
                    break
                self.encode_alph[alph[ind]] = str(i + 1) + str(j + 1)
                self.decode_alph[str(i + 1) + str(j + 1)] = alph[ind]
    
    # функция шифрования
    def encrypt(self, mes):
        encoded = ''
        for l in mes:
            encoded += self.encode_alph.get(l, l)

        return encoded

    # функция расшифрования
    def decrypt(self, mes):
        decoded = ''
        # разбиваем строчку на "двойки"
        symbols_array = [
            mes[i:i + 2]
            for i, letter in enumerate(mes)
            if i % 2 == 0
        ]

        for l in symbols_array:
            decoded += self.decode_alph.get(l, l)

        return decoded
    