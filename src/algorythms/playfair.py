from rest_framework.serializers import ValidationError

class Playfair:
    alph = [
        l for l in 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЬЫЭЮЯ'
    ]

    def __init__(self, keys={}, **kwargs):
        self.key = keys.get('L')

        test_set = {
            l for l in self.key
        }
        if len(self.key) > 30:
            raise ValidationError('Лозунг не может быть длиннее 30 символов')
        if len(test_set) != len(self.key):
            raise ValidationError('Лозунг не может содержать одинаковые буквы')

        self.matrix = []

        alph = self.alph.copy()

        for i in range(5):
            self.matrix.append([])
            for j in range(6):
                ind = (i * 6) + j
                if ind < len(self.key):
                    self.matrix[i].append(self.key[ind])
                    alph.pop(alph.index(self.matrix[i][j]))
                else:
                    self.matrix[i].append(alph.pop(0))

    # функция шифрования
    def encrypt(self, mes):
        for l in mes:
            if l not in self.alph:
                raise ValidationError(f'Неизвестный символ {l}')
        mes = [l for l in mes]
        encoded = ''
        prepared = False
        while not prepared:
            prepared = True
            for i in range(len(mes)):
                if i + 1 != len(mes) and mes[i] == mes[i+1]:
                    mes.insert(i+1, 'Ф')
                    prepared = False
                    break
        if len(mes) % 2 != 0:
            mes.append('Ф' if mes[-1] != 'Ф' else 'Щ')
        
        couples = [
            mes[i:i + 2]
            for i in range(len(mes))
            if i % 2 == 0
        ]
            
        for first_l, second_l in couples:
            first_pos = [0, 0]
            second_pos = [0, 0]
            for i in range(5):
                row = self.matrix[i]
                first_pos[0], first_pos[1] = (first_pos[0], first_pos[1]) if not (first_l in row) else (i, row.index(first_l))
                second_pos[0], second_pos[1] = (second_pos[0], second_pos[1]) if not (second_l in row) else (i, row.index(second_l))
            
            if first_pos[0] == second_pos[0]:
                first_pos[1] = (first_pos[1] + 1) % 6
                second_pos[1] = (second_pos[1] + 1) % 6
            elif first_pos[1] == second_pos[1]:
                first_pos[0] = (first_pos[0] + 1) % 5
                second_pos[0] = (second_pos[0] + 1) % 5
            else:
                first_pos[1], second_pos[1] = second_pos[1], first_pos[1]

            encoded += self.matrix[first_pos[0]][first_pos[1]] + self.matrix[second_pos[0]][second_pos[1]]
        
        result_matrix = '\n'.join([' '.join(r) for r in self.matrix])
        
        return {'result': encoded, 'info': result_matrix}

    # функция расшифрования
    def decrypt(self, mes):
        decoded = ''
        couples = [
            mes[i:i + 2]
            for i in range(len(mes))
            if i % 2 == 0
        ]
        for first_l, second_l in couples:
            first_pos = [0, 0]
            second_pos = [0, 0]
            for i in range(5):
                row = self.matrix[i]
                first_pos[0], first_pos[1] = (first_pos[0], first_pos[1]) if not (first_l in row) else (i, row.index(first_l))
                second_pos[0], second_pos[1] = (second_pos[0], second_pos[1]) if not (second_l in row) else (i, row.index(second_l))
            
            if first_pos[0] == second_pos[0]:
                first_pos[1] = (first_pos[1] - 1) if (first_pos[1] - 1) >= 0 else 5
                second_pos[1] = (second_pos[1] - 1) if (second_pos[1] - 1) >= 0 else 5
            elif first_pos[1] == second_pos[1]:
                first_pos[0] = (first_pos[0] - 1) if (first_pos[0] - 1) >= 0 else 4
                second_pos[0] = (second_pos[0] - 1) if (second_pos[0] - 1) >= 0 else 4
            else:
                first_pos[1], second_pos[1] = second_pos[1], first_pos[1]

            decoded += self.matrix[first_pos[0]][first_pos[1]] + self.matrix[second_pos[0]][second_pos[1]]
        
        result_matrix = '\n'.join([' '.join(r) for r in self.matrix])
        
        return {'result': decoded, 'info': result_matrix}
