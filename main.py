from matrix import Matrix
from vector import Vector
from solvers import JacobiSolver, GaussSeidlerSolver, DirectSolver
import matplotlib.pyplot as plt
#193667
e = 6
a1 = 5 + e
a2 = a3 = -1
N = 967
#A
b = Vector(N, 3)
A = Matrix(N, N, a1, a2, a3)
A.addValues()

sizes = [100, 500, 1000, 2000, 3000]
jacobi_times = []
gauss_times = []
direct_times = []
e = 6
a1 = 5 + e
a2 = a3 = -1
for size in sizes:
    A = Matrix(size, size, a1, a2, a3)
    A.addValues()
    b = Vector(size, 3)
    jacobi = JacobiSolver(A, b, size)
    jacobi_times.append(jacobi.duration)

    gaussSeidler = GaussSeidlerSolver(A, b, size)
    gauss_times.append(gaussSeidler.duration)

    direct = DirectSolver(A, b, size)
    direct_times.append(direct.duration)

plt.plot(sizes, jacobi_times, label='Jacobi')
plt.plot(sizes, gauss_times, label='Gauss-Seidel')
plt.plot(sizes, direct_times, label='Direct')
plt.xlabel('Iterations)')
plt.ylabel('Time (seconds)')
plt.legend()
plt.grid(True)

plt.show()
