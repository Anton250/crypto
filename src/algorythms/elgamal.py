from src.comparison import Comparison, Eratosthene
from random import randint
from rest_framework.serializers import ValidationError


class Elgamal:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}):
        self.p = int(keys.get('p'))
        e = Eratosthene(self.p)
        if self.p < len(alph):
            raise ValidationError('P должно быть больше длины алфавита')
        if not self.p in e.arr:
            raise ValidationError('P не является простым числом')
        self.g = keys.get('g')
        if self.g:
            self.g = int(self.g)
            if self.g < 1 or self.g >= self.p:
                raise ValidationError('g должно быть в диапазоне 1 < g < p')
        self.x = keys.get('x')
        if self.x:
            self.x = int(self.x)
            if self.x < 1 or self.x >= self.p:
                raise ValidationError('x должно быть в диапазоне 1 < x < p')
        self.y = keys.get('y')
        self.alph = alph

    def encrypt(self, mes):
        '''
        Метод для шифрования
        '''
        p = int(self.p)
        g = int(self.g)
        # если не передан открытый ключ, вычисляем его и возвращаем
        if not self.y:
            x = int(self.x)
            return f'Открытый ключ: {(g ** x) % p}'

        y = int(self.y)
        # оцифровываем сообщение
        mes = [
            self.alph.index(l) for l in mes
        ]
        encrypted = ''
        # составляем список доступных рандомизаторов
        k_array = []
        for i in range(self.p - 1):
            k = i + 1
            if Comparison.NOD(k, self.p - 1) == 1:
                k_array.append(k)
        max_len = len(str(p))
        for i, m in enumerate(mes):
            # выбираем рандомизатор
            k = k_array[randint(0, len(k_array) - 1)]
            # вычисляем a по формуле a = g^k mod p
            a = (g**k) % p
            # вычисляем b по формуле b = y^k * m mod p
            b = (y**k * m) % p
            encrypted += str(a).zfill(max_len) + str(b).zfill(max_len)

        return encrypted

    def decrypt(self, mes):
        p = int(self.p)
        x = int(self.x)
        max_len = len(str(p))
        if len(mes) % (max_len * 2) != 0:
            raise ValidationError('Сообщение имеет неправильную длину.')
        # разбиваем сообщение на формат (a,b)
        mes = [
            (int(mes[i * max_len:i * max_len + max_len]), int(mes[(i+1) * max_len:(i+1) * max_len + max_len])) for i in range(len(mes) // max_len) if i % 2 == 0
        ]
        comparison = Comparison(p)
        decrypted = ''
        for a, b in mes:
            decrypted += self.alph[comparison.solve_comparsion(a**x, b)] # решаем сравнение

        return decrypted
