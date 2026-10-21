"""S3_12 - Numerical errors and floating-point representation.

Why Asset-Inventory checks the condition number instead of comparing the
determinant to zero, and why it uses solve instead of the inverse.
"""
import math
import numpy as np

print("=== 1. 0.1 + 0.2 ===")
print("0.1 + 0.2 =", repr(0.1 + 0.2))
print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)
print("math.isclose(0.1 + 0.2, 0.3):", math.isclose(0.1 + 0.2, 0.3))

print("\n=== 2. det close to zero does not mean singular ===")
small = 0.1 * np.eye(10)              # perfectly fine matrix, just small numbers
print("0.1 * I (10 x 10): det =", np.linalg.det(small), "| cond =", np.linalg.cond(small))

print("\n=== 3. A singular matrix whose det does not come out as zero ===")
almost = np.array([[0.1, 0.3],
                   [0.7, 2.1]])          # row 2 = 7 * row 1, so det should be 0
print("by hand: 0.1 * 2.1 - 0.3 * 0.7 = 0.21 - 0.21 = 0")
print("in Python: 0.1 * 2.1 =", repr(0.1 * 2.1), "and 0.3 * 0.7 =", repr(0.3 * 0.7))
print("det =", np.linalg.det(almost), "| det == 0:", np.linalg.det(almost) == 0)
print("cond = %.1e -> huge, so the matrix is singular" % np.linalg.cond(almost))

print("\n=== 4. solve versus inverse ===")
n = 12
hilbert = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
x_true = np.ones(n)
b = hilbert @ x_true
x_solve = np.linalg.solve(hilbert, b)
x_inv = np.linalg.inv(hilbert) @ b
print("cond(Hilbert 12 x 12) = %.1e" % np.linalg.cond(hilbert))
print("residual |Hx - b| with solve: %.1e" % np.linalg.norm(hilbert @ x_solve - b))
print("residual |Hx - b| with inv:   %.1e" % np.linalg.norm(hilbert @ x_inv - b))

print("\n=== 5. The check used in Asset-Inventory ===")
MAX_CONDITION_NUMBER = 1e12
for name, matrix in [("I - A of S3_10", np.array([[1, -0.1, 0], [0, 1, 0], [-0.5, -0.2, 1]])),
                     ("singular 2 x 2", almost)]:
    cond = np.linalg.cond(matrix)
    ok = np.isfinite(cond) and cond <= MAX_CONDITION_NUMBER
    print(f"{name}: cond = {cond:.3g} -> {'solve' if ok else 'refuse'}")
