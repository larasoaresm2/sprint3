"""S3_09 - Linear Algebra I: matrices and linear transformations.

Checks with NumPy every exercise solved by hand in README.md.
"""
import numpy as np

print("=== 1. Is it a linear transformation? ===")
def T(p):                      # T(x, y) = (2x, x + y)
    x, y = p
    return np.array([2 * x, x + y])

def S(p):                      # S(x, y) = (x + 1, y)
    x, y = p
    return np.array([x + 1, y])

u, w, k = np.array([1.0, 2.0]), np.array([3.0, -1.0]), 5.0
print("T(u + w) == T(u) + T(w):", np.allclose(T(u + w), T(u) + T(w)))
print("T(k u)   == k T(u):     ", np.allclose(T(k * u), k * T(u)))
print("S(0) =", S(np.zeros(2)), "-> not (0, 0), so S is not linear")

print("\n=== 2. Matrix of T and its dimensions ===")
T_matrix = np.array([[2.0, 0.0],
                     [1.0, 1.0]])
print(T_matrix, "shape", T_matrix.shape, "-> takes R^2 to R^2")
print("T_matrix @ u =", T_matrix @ u, "| T(u) =", T(u))

print("\n=== 3. Kernel and image of T ===")
print("det(T) =", np.linalg.det(T_matrix), "-> not zero, so kernel = {0} and image = R^2")
print("rank(T) =", np.linalg.matrix_rank(T_matrix))

print("\n=== 4. Geometric transformations of the plane ===")
rotation_90 = np.array([[0.0, -1.0], [1.0, 0.0]])
reflection_x = np.array([[1.0, 0.0], [0.0, -1.0]])
scale_2 = np.array([[2.0, 0.0], [0.0, 2.0]])
print("rotate (1, 0) by 90 degrees:", rotation_90 @ np.array([1.0, 0.0]))
print("reflect (2, 3) on the x axis:", reflection_x @ np.array([2.0, 3.0]))
print("scale (1, 2) by 2:          ", scale_2 @ np.array([1.0, 2.0]))

print("\n=== 5. Own risk b = M v (3 equipments, 4 vulnerabilities) ===")
#              V1   V2   V3   V4
M = np.array([[1.0, 0.0, 1.0, 0.0],    # E1 Server
              [1.0, 1.0, 0.0, 0.0],    # E2 WebApplication
              [0.0, 0.0, 1.0, 0.0]])   # E3 Database
v = np.array([9.8, 7.5, 5.0, 3.1])     # CVSS of V1..V4
b = M @ v
print("M shape", M.shape, "-> takes R^4 (vulnerabilities) to R^3 (equipments)")
print("b = M v =", b)

print("\n=== 6. Composition with F: F(Mv) == (FM)v ===")
F = np.diag([1.2, 1.5, 0.8])           # exposure factors: Server, WebApplication, Database
print("F (M v) =", F @ (M @ v))
print("(F M) v =", (F @ M) @ v)
print("equal:", np.allclose(F @ (M @ v), (F @ M) @ v))

print("\n=== 7. Null column and kernel of M ===")
print("column V4 =", M[:, 3], "-> no equipment has V4")
only_v4 = np.array([0.0, 0.0, 0.0, 3.1])
print("M @ [0, 0, 0, 3.1] =", M @ only_v4, "-> a severity only on V4 is in the kernel")
print("rank(M) =", np.linalg.matrix_rank(M), "-> kernel dimension = 4 - 3 = 1, image = R^3")
