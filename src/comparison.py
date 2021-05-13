from math import pow

class Comparison:
    def __init__(self, m):
        self.m = m
    

    def _NOD_array(self, a, b):
        '''
        Метод для расчета неполных частных
        '''
        result = []
        r = 1
        while r != 0:
            r = a % b
            k = a // b
            a = b
            b = r
            result.append(k)
        return result

    @staticmethod
    def NOD(a, b):
        r = 1
        while r != 0:
            r = a % b
            a = b
            b = r
        return a


    def _get_suitable_fractions(self, a, b):
        '''
        Метод для расчета числителей подходящих дробей
        '''
        p = 1
        p_prev = 0
        result = []
        nod = self._NOD_array(a, b)
        for i in nod:
            val = i * p + p_prev
            result.append(val)
            p_prev = p
            p = val
        return result


    def solve_comparsion(self, a, b):
        '''
        Метод для решения сравнения
        '''
        divisions = self._get_suitable_fractions(self.m, a)
        m = divisions[-2] * int(pow(-1,(len(divisions)-1))) * b
        return m % self.m

class Eratosthene:
    def __init__(self, N):
        self.arr = [
            i + 1 for i in range(N)
        ]
        self.arr.pop(0)
        p = 2
        i = 0
        not_ready = True
        while p ** 2 <= N:
            cur_ind = 2
            while p * cur_ind <= N:
                if p * cur_ind in self.arr:
                    self.arr.remove(p * cur_ind)
                cur_ind += 1
            i += 1
            p = self.arr[i]
