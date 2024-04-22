from matrix import Matrix
from math import sin

class Vector(Matrix):
    def __init__(self, N, f):
        self.f = f
        self.N = N
        self.vector = []
        for i in range(self.N):
            self.vector.append(sin(i * (self.f + 1)))