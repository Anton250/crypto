from src.elliptical_curve import EllipticalCurve
from rest_framework.serializers import ValidationError
from random import randint


class ECC:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}, **kwargs):
        self.p = int(keys.get('p'))
        self.a = int(keys.get('a'))
        self.b = int(keys.get('b'))
        self.elliptical_curve = EllipticalCurve(self.p, self.a, self.b)
        self.alph = alph
        self.G = self._validate_point(keys.get('G'), 'G')        
        self.D = keys.get('D')
        self.c = keys.get('c')
        self.q = self.elliptical_curve.get_point_order(self.G)

    def _validate_point(self, point, name):
        '''
        Метод для валидации формата введенной точки
        '''
        try:
            point = list(map(int,point.split(',')))
            if len(point) != 2:
                raise ValueError('Bad len')
        except:
            raise ValidationError(f'Точка {name} указана в неверном формате, должна быть x,y')
        return point

    def encrypt(self, mes):
        '''
        Метод для шифрования
        '''
        # оцифровываем буквы
        mes = [
            self.alph.index(l) + 1 for l in mes
        ]

        # если не передали открытый ключ, то расчитываем его и возвращаем
        if not self.D:
            c = int(self.c)
            D = self.elliptical_curve.multiplicate_point(self.G, c)
            return f'Окрытый ключ: {D}'

        D = self._validate_point(self.D, 'D')

        encrypted = ''
        max_len = len(str(self.p))

        for m in mes:
            k = randint(1, self.q - 1) # рандомизатор
            R = self.elliptical_curve.multiplicate_point(self.G, k)
            P = self.elliptical_curve.multiplicate_point(D, k)
            e = (m * P[0]) % self.p # шифруем
            encrypted += str(R[0]).zfill(max_len) + str(R[1]).zfill(max_len) + str(e).zfill(max_len)

        return encrypted

    def decrypt(self, mes):
        '''
        Метод для расшифрования
        '''
        max_len = len(str(self.p))
        if len(mes) % (max_len * 3) != 0:
            raise ValidationError('Сообщение имеет неправильную длину.')
        # разбиваем сообщение на формат ((x,y), e)
        mes = [
            (
                (int(mes[i * max_len:i * max_len + max_len]), int(mes[(i+1) * max_len:(i+1) * max_len + max_len])),
                int(mes[(i+2) * max_len:(i+2) * max_len + max_len])
            )      
            for i in range(len(mes) // max_len) if i % 3 == 0
        ]

        c = int(self.c)

        decrypted = ''

        for R, e in mes:
            Q = self.elliptical_curve.multiplicate_point(R, c)
            index = (e * (Q[0]**(self.p - 2))) % self.p # расшифровываем
            decrypted += self.alph[index - 1]

        return decrypted
