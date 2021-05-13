from rest_framework.serializers import ValidationError


class DiffieHellman:
    def __init__(self, keys={}, **kwargs):
        self.K = int(keys.get('K'))
        self.n = int(keys.get('n'))
        if self.K >= self.n or self.K <= 1:
            raise ValidationError('K должно быть в диапазоне 1 < K < n')
        self.a = keys.get('a')
        self.Y = keys.get('Y')

    def encrypt(self, *args, **kwargs):
        '''
        Метод для вычисления открытого ключа
        '''
        if not self.a:
            raise ValidationError('a должно быть указано для вычисления открытого ключа')
        K = self.K
        n = self.n
        a = int(self.a)
        if a >= n or a <= 1:
            raise ValidationError('a должно быть в диапазоне 1 < a < n')
        Y = a^K % n
        if Y == 1:
            raise ValidationError('Y получилось равным 1')
        if Y == K:
            raise ValidationError('Y получилось равным K выберите другой K')

        return Y
    
    def decrypt(self, *args, **kwargs):
        '''
        Метод для вычисления общего секретного ключа
        '''
        n = self.n
        Y = int(self.Y)
        if Y >= n or Y <= 1:
            raise ValidationError('Y должно быть в диапазоне 1 < Y < n')
        K = self.K
        K = Y^K % n
        if K == 1:
            raise ValidationError('K получилось равным 1')

        return K
