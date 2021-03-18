class GammaGenerator:
    '''
    Класс для генерации гаммы
    '''
    def __init__(self, a, c, m, X):
        self.a = a
        self.c = c
        self.m = m
        self.prev_value = X
        self.init_value = X
    def next(self):
        self.prev_value = (self.a*self.prev_value+self.c)%self.m
        return self.prev_value

    def reset(self):
        self.prev_value = self.init_value

class Shannon:
    def __init__(self, alph='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}, **kwargs):
        self.alph = alph
        self.generator = GammaGenerator(int(keys['a']), int(keys['c']), int(keys['m']), int(keys['X']))
        self.module = len(alph)

    def encrypt(self, message):
        self.generator.reset()
        result = ''
        gamma = []
        for l in message:
            num = self.generator.next() # получаем следующее значение гаммы
            gamma.append(str(num))
            ind = self.alph.index(l)
            result += self.alph[(num + ind)%self.module] # накладываем гамму
        return {'result': encoded, 'info': ','.join(gamma)}
        
    def decrypt(self, message):
        self.generator.reset()
        result = ''
        gamma = []
        for l in message:
            num = self.generator.next() # получаем следующее значение гаммы
            gamma.append(str(num))
            ind = self.alph.index(l)
            result += self.alph[(ind + (self.module - num))%self.module] # снимаем гамму
        return {'result': encoded, 'info': ','.join(gamma)}
