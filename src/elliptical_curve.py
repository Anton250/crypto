class EllipticalCurve:
    def __init__(self, p, a, b, verbose=False):
        self.p = p
        self.a = a
        self.b = b
        self.squares = {}
        self.verbose = verbose
        for i in range(p):
            q = (i**2) % p
            self.squares.setdefault(q, []).append(i)
            if verbose:
                print(f'{i}^2 mod {p} = {q}')
        self.order, self.points = self._get_order_and_points()

    def _get_order_and_points(self):
        '''
        Метод для расчета порядка кривой и всех её точек
        '''
        order = 1
        points = [(0,0)]
        equation = lambda x: (x**3 + self.a * x + self.b) % self.p

        for x in range(self.p):
            result = equation(x)
            if self.squares.get(result):
                for y in self.squares.get(result):
                    points.append((x, y))
                    if self.verbose:
                        print((x, y))
                    order += 1
        if self.verbose:
            print(f'Order: {order}')
        return order, points


    def get_point_order(self, point: tuple):
        '''
        Метод для расчета порядка точки
        '''
        initial_point = point
        point = self.double_point(point)
        if point[0] == 0 and point[1] == 0:
            return 2
        order = 2
        while point != (0, 0):
            point = self.sum_points(point, initial_point)
            order += 1
            if self.verbose:
                print(f'{order}G = {point}')

        return order
    
    def double_point(self, point: tuple):
        '''
        Метод для удвоения точки
        '''
        x, y = point
        if y == 0:
            return (0,0)
        l = ((3 * x**2 + self.a) * (2 * y)**(self.p - 2)) % self.p
        x_result = (l**2 - 2*x) % self.p
        y_rusult = (l*(x - x_result) - y) % self.p

        return x_result, y_rusult
    
    def sum_points(self, point1: tuple, point2: tuple):
        '''
        Метод для сложения точек
        '''
        x1, y1 = point1
        x2, y2 = point2
        if point1 == point2:
            return self.double_point(point1)

        if x2 - x1 == 0:
            return (0,0)
        
        if point1 == (0,0):
            return point2

        if point2 == (0,0):
            return point1
        
        l = ((y2 - y1) * (x2 - x1)**(self.p - 2)) % self.p
        x_result = (l**2 - x1 - x2) % self.p
        y_result = (l*(x1 - x_result) - y1) % self.p

        return x_result, y_result

    def multiplicate_point(self, point:tuple, k, return_list=False):
        '''
        Метод для умножения точки на число
        '''
        if k == 1:
            return point
        initial_point = point
        point = self.double_point(point)
        result = [initial_point, point]
        if self.verbose:
                print(f'[1]P = {initial_point}')
                print(f'[2]P = {point}')
        for i in range(k-2):
            point = self.sum_points(point, initial_point)
            if return_list:
                result.append(point)
            if self.verbose:
                print(f'[{i + 3}]P = {point}')
        if return_list:
            return result
        return point
