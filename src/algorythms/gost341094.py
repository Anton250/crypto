from src.comparison import Eratosthene
from rest_framework.serializers import ValidationError
from src.square_hash import square_hash
from random import randint

class GOST341094:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}, **kwargs):
        self.p = int(keys.get('p'))
        self.q = int(keys.get('q'))
        P = self.p
        Q = self.q
        e = Eratosthene(P)
        if not P in e.arr:
            raise ValidationError('Число p не является простым')
        if not Q in e.arr:
            raise ValidationError('Число q не является простым')
        if not (P - 1) % Q == 0:
            raise ValidationError('Число q не является сомножителем p - 1')
        self.a = int(keys.get('a'))
        if not (self.a**Q) % P == 1:
            raise ValidationError('Число a не удовлетворяет условию: a^q mod p = 1')
        self.x = keys.get('x')
        self.y = keys.get('y')
        self.alph = alph

    def encrypt(self, mes):
        '''
        Метод подписания сообщения
        '''
        # кодируем сообщение
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        mes_hash = square_hash(int_mes, len(self.alph))
        r = 0
        s = 0
        self.x = int(self.x)
        if mes_hash % self.q == 0:
            mes_hash = 1
        while r == 0 or s == 0:
            k = randint(1, self.q - 1)
            r = (self.a**k % self.p) % self.q
            s = (self.x * r + k * mes_hash) % self.q
        
        return {'result': mes + f'_{r}_{s}', 'info': f'Ключ для проверки подписи: {self.a**self.x % self.p}'}

    def decrypt(self, mes):
        '''
        Метод проверки подписи
        '''
        try:
            mes, r, s = mes.split('_')
        except:
            raise ValidationError('Сообщение должно быть в формате {ТЕКСТ}_{r}_{s}.')
        # кодируем сообщение
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        self.y = int(self.y)
        s = int(s)
        r = int(r)
        mes_hash = square_hash(int_mes, len(self.alph))
        if mes_hash % self.q == 0:
            mes_hash = 1
        v = (mes_hash**(self.q - 2)) % self.q
        z1 = (s * v) % self.q
        z2 = ((self.q - r) * v) % self.q
        u = ((self.a**z1 * self.y**z2) % self.p) % self.q

        if u == r:
            result = 'Подпись верна.' 
        else:
            result = 'Подпись не верна.'

        return result
