from src.comparison import Comparison, Eratosthene
from rest_framework.serializers import ValidationError


class RSA:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}, **kwargs):
        self.P = keys.get('P')
        self.Q = keys.get('Q')
        P = int(self.P)
        Q = int(self.Q)
        if Q > P:
            e = Eratosthene(Q)
        else:
            e = Eratosthene(P)
        if not P in e.arr:
            raise ValidationError('Число P не является простым')
        if not Q in e.arr:
            raise ValidationError('Число Q не является простым')
        self.E = keys.get('E')
        if self.E:
            E = int(self.E)
            if Comparison.NOD(E, (P-1)*(Q-1)) != 1:
                raise ValidationError('E не взаимно просто с f(N)')
        self.N = P * Q
        if self.N < len(alph):
            raise ValidationError('P * Q должно быть больше длины алфавита')
        self.alph = alph

    def encrypt(self, mes):
        # кодируем сообщение
        mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        encrypted = []
        self.N = int(self.N)
        self.E = int(self.E)
        for m in mes:
            # шифруем по формуле m^E mod N
            encrypted.append((m**self.E) % self.N)
        
        max_len = len(str(self.N))
        encrypted = list(map(lambda x: str(x).zfill(max_len), encrypted))

        return ''.join(encrypted)

    def decrypt(self, mes):
        self.N = int(self.P) * int(self.Q)
        max_len = len(str(self.N))
        if len(mes) % max_len != 0:
            raise ValidationError('Сообщение имеет неправильную длину.')
        mes = [
            int(mes[i * max_len:i * max_len + max_len]) for i in range(len(mes) // max_len)
        ]
        comparison = Comparison((int(self.P) - 1) * (int(self.Q) - 1))
        # вычисляем секретный ключ решая сравнение D*E = 1 mod F(N)
        D = comparison.solve_comparsion(int(self.E), 1)
        decrypted = []

        for m in mes:
            # расшифровываем по формуле m^D mod N
            decrypted.append((m**D) % self.N)

        # декодируем сообщение
        decrypted = ''.join([self.alph[i - 1] for i in decrypted])

        return decrypted
