class VerticalPermutation:
    def __init__(self, keys={}, **kwargs):
        key = keys.get('P')
        sorted_key = sorted([l for l in keys.get('P')])
        self.key = []
        for l in key:
            i = sorted_key.index(l)
            while i + 1 < len(sorted_key):
                if sorted_key[i] == sorted_key[i + 1] and i in self.key:
                    i += 1
                else:
                    break
            self.key.append(i)
        
        
    def encrypt(self, mes):
        encrypted = ''

        size = [len(mes) // len(self.key) + 1,len(self.key)]
        if len(mes) % len(self.key) == 0:
            size[0] = len(mes) // len(self.key)
        table = []
        mes = [l for l in mes]
        for i in range(size[0]):
            row = mes[i * size[1]:i * size[1] + size[1]]
            if i % 2 == 1:
                row.reverse()

            table.append(row)
        for k in self.key:
            for i in range(size[0]):
                if k >= len(table[i]):
                    continue
                encrypted += table[i][k]

        return {'result': encrypted, 'info': self.key}


    def decrypt(self, mes):
        decrypted = ''   
        size = [len(mes) // len(self.key) + 1,len(self.key)]
        if len(mes) % len(self.key) == 0:
            size[0] = len(mes) // len(self.key)
        table = []
        mes = [l for l in mes]
        empty_cols_after = len(mes) % len(self.key)
        blocks = {}
        shift = 0
        for i in range(size[1]):
            key_index = self.key[i]
            to_index = i * size[0] + size[0] - shift
            if key_index >= empty_cols_after:
                to_index -= 1
                
            blocks[key_index] = mes[i * size[0] - shift:to_index]
            if key_index >= empty_cols_after:
                shift += 1

        for i in range(size[0]):
            loop_genetator = range(size[1])
            if i % 2 == 1:
                loop_genetator = reversed(loop_genetator)
            for j in loop_genetator:
                if i >= len(blocks[j]):
                    continue
                decrypted += blocks[j][i]
            
        return {'result': decrypted, 'info': self.key}
