import time
import copy
from matrix import Matrix

class JacobiSolver:
    def __init__(self, A, b, N):
        self.A = A
        self.b = b
        self.N = N
        self.x, self.duration, self.error = self.solve(A, b)

    def solve(self, A, b):
        x = [1] * self.N
        x_new = [1] * self.N
        errors = []
        eps = 1e-9
        start_time = time.time()
        for _ in range(200):
            for i in range(self.N):
                s = b.vector[i]
                for j in range(self.N):
                    if i != j:
                        s -= A.matrix[i][j] * x[j]
                x_new[i] = s / self.A.matrix[i][i]
            x = copy.deepcopy(x_new)
            res = A.mul(x)
            
            for i in range(len(res)):
                res[i] -= b.vector[i]
            
            res_norm = 0
            for i in range(len(res)):
                res_norm += res[i] ** 2
            res_norm = res_norm ** 0.5

            
            errors.append(res_norm)
            if res_norm < eps:
                break
        duration = time.time() - start_time
        return x, duration, errors
    

class GaussSeidlerSolver:
    def __init__(self, A, b, N):
        self.A = A
        self.b = b
        self.N = N
        self.x, self.duration, self.error = self.solve(A, b)

    def solve(self, A, b):
        x = [1] * self.N
        x_new = [1] * self.N
        errors = []
        eps = 1e-9
        start_time = time.time()
        for _ in range(200):
            for i in range(self.N):
                s = b.vector[i]
                for j in range(i):
                    s -= A.matrix[i][j] * x_new[j]
                for j in range(i + 1, self.N):
                    s -= A.matrix[i][j] * x[j]
                x_new[i] = s / self.A.matrix[i][i]
            
            x = copy.deepcopy(x_new)
            res = A.mul(x)
            for i in range(len(res)):
                res[i] -= b.vector[i]
            
            res_norm = 0
            for i in range(len(res)):
                res_norm += res[i] ** 2
            res_norm = res_norm ** 0.5

            errors.append(res_norm)
            if res_norm < eps:
                break
        duration = time.time() - start_time
        return x, duration, errors
    
class DirectSolver:
    def __init__(self, A, b, N):
        self.A = A
        self.b = b
        self.N = N
        self.x, self.duration, self.error = self.solve(A, b)

    def solve(self, A, b):
        U = copy.deepcopy(A)
        L = Matrix(A.n, A.n, 0, 0, 0)
        for i in range(A.n):
            L.matrix[i][i] = 1
        x = A.n * [0]
        y = A.n * [0]

        start = time.time()
        for i in range(2, A.n + 1):
            for j in range(1, i):
                L.matrix[i - 1][j - 1] = U.matrix[i - 1][j - 1] / U.matrix[j - 1][j - 1]
                for k in range(j, A.n):
                    U.matrix[i - 1][k] -= L.matrix[i - 1][j - 1] * U.matrix[j - 1][k]

        for i in range(A.n):
            y[i] = b.vector[i]
            for j in range(i):
                y[i] -= L.matrix[i][j] * y[j]

        for i in range(A.n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, A.n):
                x[i] -= U.matrix[i][j] * x[j]
            x[i] /= U.matrix[i][i]
        end = time.time()

        res = A.mul(x)
        for i in range(len(res)):
            res[i] -= b.vector[i]
            
        error = 0
        for i in range(len(res)):
            error += res[i] ** 2
        error = error ** 0.5
        return x, end - start, [error]