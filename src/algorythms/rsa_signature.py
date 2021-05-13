from src.comparison import Comparison, Eratosthene
from rest_framework.serializers import ValidationError
from src.utils import square_hash


class RSASignature:
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
        '''
        Метод подписания сообщения
        '''
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        mes_hash = square_hash(int_mes, len(self.alph))
        comparison = Comparison((int(self.P) - 1) * (int(self.Q) - 1))
        D = comparison.solve_comparsion(int(self.E), 1)
        signature = (mes_hash**D) % self.N
        return mes + '_' + str(signature)
        

    def decrypt(self, mes):
        '''
        Метод проверки подписи
        '''
        try:
            mes, signature = mes.split('_')
        except:
            raise ValidationError('Сообщение должно быть в формате {ТЕКСТ}_{ПОДПИСЬ}.')
        self.N = int(self.N)
        self.E = int(self.E)
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        mes_hash = square_hash(int_mes, len(self.alph))
        decrypted_mes_hash = (int(signature)**self.E) % self.N

        if mes_hash == decrypted_mes_hash:
            result = 'Подпись верна.' 
        else:
            result = 'Подпись не верна.'

        return result
