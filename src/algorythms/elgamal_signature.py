from src.comparison import Comparison, Eratosthene
from random import randint
from rest_framework.serializers import ValidationError
from src.square_hash import square_hash


class ElgamalSignature:
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
            if self.x < 1 or self.x >= (self.p - 1):
                raise ValidationError('x должно быть в диапазоне 1 < x < p - 1')
        self.y = keys.get('y')
        self.alph = alph

    def encrypt(self, mes):
        '''
        Метод подписания сообщения
        '''
        # оцифровываем сообщение
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        # составляем список доступных рандомизаторов
        k_array = []
        for i in range(self.p - 1):
            k = i + 1
            if Comparison.NOD(k, self.p - 1) == 1:
                k_array.append(k)
        # выбираем случайный рандомизатор
        k = k_array[randint(0, len(k_array) - 1)]
        # вычисляем a = g^k mod p
        a = self.g**k % self.p
        comparison = Comparison(self.p - 1)
        # вычисляем хэш-код сообщения
        mes_hash = square_hash(int_mes, len(self.alph))
        # решаем сравнение b*k = M - x*a mod (p-1)
        b = comparison.solve_comparsion(k, mes_hash - self.x * a)
        return {'result': mes + f'_{a}_{b}', 'info': f'Ключ для проверки подписи: {self.g**self.x % self.p}'}


    def decrypt(self, mes):
        try:
            mes, a, b = mes.split('_')
        except:
            raise ValidationError('Сообщение должно быть в формате {ТЕКСТ}_{a}_{b}.')
        # оцифровываем сообщение
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        # вычисляем хэш-код сообщения
        mes_hash = square_hash(int_mes, len(self.alph))
        y = int(self.y)
        # вычисляем a1 = (y^a * a^b) mod p
        a1 = ((y**int(a))*(int(a)**int(b))) % self.p
        # вычисляем a2 = g^M mod p
        a2 = self.g**mes_hash % self.p

        if a1 == a2:
            result = 'Подпись верна.' 
        else:
            result = 'Подпись не верна.'

        return result
