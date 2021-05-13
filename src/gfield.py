from functools import reduce

class GField:
    '''
    Класс для умножения в поле Галуа
    '''
    def __init__(self, m, polynom):
        self.m = m
        self.polynom = bin(polynom)[2:]
        self.multyplication_results = {}

    def sum(self, a, b):
        return a ^ b

    def get_pows(self, bin_num):
        a = [l for l in bin_num]
        a.reverse()
        pows = []
        for i in range(len(a)):
            if a[i] == '1':
                pows.append(i)
        return pows

    def _remainder_from_polynom_division(self, a:int):
        '''
        Остаток от деления полинома получившегося при полиномиальном умножении
        на порождающий полином
        '''
        a = bin(a)[2:]
        b = self.polynom
        a_pows = self.get_pows(a)
        b_pows = self.get_pows(b)
        if len(a_pows) == 0:
            return 0

        while max(a_pows) >= max(b_pows):
            pow = max(a_pows) - max(b_pows)
            tmp = set(map(lambda x: x + pow, b_pows))
            a_pows = list(set(a_pows).symmetric_difference(tmp))
            if len(a_pows) == 0:
                return 0
        return reduce(lambda x, y: x + 2 ** y, a_pows, 0)


    def _polynominal_multiplication(self, a, b):
        '''
        Полиномиальное произведение чисел
        '''
        a = bin(a)[2:]
        b = bin(b)[2:]
        a_pows = self.get_pows(a)
        b_pows = self.get_pows(b)
        result_pows = []
        for ap in a_pows:
            for bp in b_pows:
                result_pows.append(ap + bp)
        
        return reduce(lambda x, y: x ^ 2 ** y, result_pows, 0)

    
    def multyplication(self, a, b):
        '''
        Метод для умножения чисел в конечном поле
        Он также сохраняет результат, чтобы не делать повторных вычислений
        '''
        result = self.multyplication_results.get(a, {}).get(b) or self.multyplication_results.get(b, {}).get(a) 
        if result:
            return result
        result = self._remainder_from_polynom_division(self._polynominal_multiplication(a, b))
        self.multyplication_results.setdefault(a, {})[b] = result
        self.multyplication_results.setdefault(b, {})[a] = result
        return result
