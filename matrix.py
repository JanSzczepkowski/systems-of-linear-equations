class Matrix:
    def __init__(self, m, n, a1, a2, a3):
        self.m = m
        self.n = n
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        matrix = []
        for _ in range(m):
            row = []
            for _ in range(n):
                    row.append(0)
            matrix.append(row)
        self.matrix = matrix

    def add(self, other):
        if self.m != other.m or self.n != other.n:
            print("Sizes dont match!")
            return
        result = Matrix(self.m, self.n, self.a1, self.a2, self.a3)
        for i in range(self.n):
            for j in range(self.m):
                 result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return result
    
    def sub(self, other):
        if self.m != other.m or self.n != other.n:
            print("Sizes dont match!")
            return
        result = Matrix(self.m, self.n, self.a1, self.a2, self.a3)
        for i in range(self.n):
            for j in range(self.m):
                 result.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
        return result
    
    def mul(self, other):
        if isinstance(other, Matrix):
            if self.m != other.n:
                print("Sizes dont match!")
                return
            result = Matrix(self.m, other.n, self.a1, self.a2, self.a3)
            for i in range(self.m):
                for j in range(other.n):
                    for k in range(self.n):
                        result.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
            return result
        elif isinstance(other, list):
            if self.n != len(other):
                print("Sizes dont match!")
                return
            result = [0] * self.m
            for i in range(self.m):
                for j in range(self.n):
                    result[i] += self.matrix[i][j] * other[j]
            return result
        else:
            print("Invalid type for multiplication!")
            return None
    
    def addValues(self):
        self.matrix = []
        for i in range(self.m):
            row = []
            for j in range(self.n):
                if i == j:
                    row.append(self.a1)
                elif i == j - 1 or i == j + 1:
                    row.append(self.a2)
                elif i == j - 2 or i == j + 2:
                    row.append(self.a3)
                else:
                    row.append(0)
            self.matrix.append(row)

    def norm(self):
        result = 0
        for i in range(self.m):
            for j in range(self.n):
                result += self.matrix[i][j] ** 2
        return result ** 0.5
    
    def get_lower(self):
        result = Matrix(self.m, self.n, self.a1, self.a2, self.a3)
        for i in range(self.m):
            for j in range(self.n):
                if i > j:
                    result.matrix[i][j] = self.matrix[i][j]
                else:
                    result.matrix[i][j] = 0
        return result
    
    def get_upper(self):
        result = Matrix(self.m, self.n, self.a1, self.a2, self.a3)
        for i in range(self.m):
            for j in range(self.n):
                if i < j:
                    result.matrix[i][j] = self.matrix[i][j]
                else:
                    result.matrix[i][j] = 0
        return result
    
    def get_diagonal(self):
        result = Matrix(self.n, self.m, self.a1, self.a2, self.a3)
        for i in range(self.n):
            for j in range(self.m):
                if i == j:
                    result.matrix[i][j] = self.matrix[i][j]
                else:
                    result.matrix[i][j] = 0
        return result
    
    def get_determinant(self):
        if self.n != self.m:
            raise ValueError("Matrix is not square")
        
        if self.n == 1:
            return self.matrix[0][0]
        
        if self.n == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        
        result = 0
        for i in range(self.n):
            result += ((-1) ** i) * self.matrix[0][i] * self.get_minor(0, i).get_determinant()
        return result
    
    def get_minor(self, i, j):
        result = Matrix(self.n - 1, self.m - 1, self.a1, self.a2, self.a3)
        for k in range(self.n):
            for l in range(self.m):
                if k != i and l != j:
                    result.matrix[k - (k > i)][l - (l > j)] = self.matrix[k][l]
        return result
    
    def get_transposed(self):
        result = Matrix(self.m, self.n, self.a1, self.a2, self.a3)
        for i in range(self.n):
            for j in range(self.m):
                result.matrix[j][i] = self.matrix[i][j]
        return result
    
    def get_inverted(self):
        determinant = self.get_determinant()
        if determinant == 0:
            raise ValueError("Matrix is not invertible")
        
        result = Matrix(self.n, self.m, self.a1, self.a2, self.a3)
        for i in range(self.n):
            for j in range(self.m):
                result.matrix[i][j] = ((-1) ** (i + j)) * self.get_minor(i, j).get_determinant()
        result = result.get_transposed()
        result = result * (1 / determinant)
        return result