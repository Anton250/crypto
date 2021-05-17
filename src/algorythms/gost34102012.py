from rest_framework.serializers import ValidationError
from src.square_hash import square_hash
from random import randint
from src.elliptical_curve import EllipticalCurve


class GOST34102012:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}, **kwargs):
        self.p = int(keys.get('p'))
        self.a = int(keys.get('a'))
        self.b = int(keys.get('b'))
        self.elliptical_curve = EllipticalCurve(self.p, self.a, self.b)
        self.alph = alph
        self.G = self._validate_point(keys.get('G'), 'G')        
        self.x = keys.get('x')
        self.y = keys.get('y')
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
        Метод подписания сообщения
        '''
        # кодируем сообщение
        int_mes = [
            self.alph.index(l) + 1 for l in mes
        ]
        mes_hash = square_hash(int_mes, len(self.alph))
        r = 0
        s = 0
        x = int(self.x)
        while r == 0 or s == 0:
            k = randint(1, self.q - 1)
            P = self.elliptical_curve.multiplicate_point(self.G, k)
            r = P[0] % self.q
            s = (k * mes_hash + r * x) % self.q
        Y = self.elliptical_curve.multiplicate_point(self.G, x)
        return {'result': mes + f'_{r}_{s}', 'info': f'Ключ для проверки подписи: {Y[0]},{Y[1]}'}
    
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
        mes_hash = square_hash(int_mes, len(self.alph))
        s = int(s)
        r = int(r)
        Y = self._validate_point(self.y, 'Y')
        u1 = (s * mes_hash**(self.q-2)) % self.q
        u2 = (-r * mes_hash**(self.q-2)) % self.q
        p1 = self.elliptical_curve.multiplicate_point(self.G, u1)
        p2 = self.elliptical_curve.multiplicate_point(Y, u2)
        p = self.elliptical_curve.sum_points(p1, p2)
        if p == (0,0):
            return 'Подпись не верна.'
        
        if p[0] % self.q == r:
            return 'Подпись верна'
        else:
            return 'Подпись не верна.'
