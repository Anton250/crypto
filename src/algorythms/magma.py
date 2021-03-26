class MagmaSubsitution:
    def __init__(self, **kwargs):
        self.matrix = [
            '0123456789ABCDEF',
            'C462A5B9E8D703F1',
            '68239A5C1E47BD0F',
            'B3582FADE174C960',
            'C821D4F670A53E9B',
            '7F5A816D093EB42C',
            '5DF692CAB78143E0',
            '8E25691CF4B0DA37',
            '17ED05834FA69CB2',
        ]

    def encrypt(self, mes):
        if len(mes) % 2 != 0:
            mes += 'Ф'
        hx = bytes(mes, 'utf-8').hex().upper()
        i = 1
        encrypted = ''
        for l in hx:
            encrypted += self.matrix[-(i + 1)][self.matrix[0].index(l)]
            i += 1
            if i > 8:
                i = 1
        return encrypted

    def decrypt(self, mes):
        
        i = 1
        decrypted = ''
        for l in mes:
            decrypted += self.matrix[0][self.matrix[-(i + 1)].index(l)]
            i += 1
            if i > 8:
                i = 1
        decrypted = bytearray.fromhex(decrypted.lower()).decode('utf-8')
        return decrypted
    