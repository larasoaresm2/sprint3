"""S3_10 - Linear Algebra II: linear systems.

Solves the effective-risk system (I - A)x = b of a 3-equipment scenario
by Gauss elimination, step by step, and checks it with np.linalg.solve.
"""
import numpy as np

print("=== 4. The equations as (I - A) x = b ===")
# x1 = 7.5  + 0.1 x2           (E1 inherits 10% of E2)
# x2 = 14.8                    (E2 depends on nobody)
# x3 = 0    + 0.5 x1 + 0.2 x2  (E3 inherits 50% of E1 and 20% of E2)
b = np.array([7.5, 14.8, 0.0])
A = np.array([[0.0, 0.1, 0.0],
              [0.0, 0.0, 0.0],
              [0.5, 0.2, 0.0]])
system = np.eye(3) - A
print("I - A =\n", system)
print("b =", b)

print("\n=== 5. Gauss elimination by hand ===")
augmented = np.column_stack([system, b])   # [I - A | b]
print("start:\n", augmented)

augmented[2] = augmented[2] + 0.5 * augmented[0]    # L3 <- L3 + 0.5 L1
print("L3 <- L3 + 0.5 L1:\n", augmented)

augmented[2] = augmented[2] + 0.25 * augmented[1]   # L3 <- L3 + 0.25 L2
print("L3 <- L3 + 0.25 L2:\n", augmented)

# back substitution: from the last row up
x3 = augmented[2, 3]
x2 = augmented[1, 3]
x1 = augmented[0, 3] + 0.1 * x2
x_by_hand = np.array([x1, x2, x3])
print("back substitution: x =", x_by_hand.round(2))

print("\n=== 6. Check with NumPy ===")
x_numpy = np.linalg.solve(system, b)
print("np.linalg.solve:   x =", x_numpy.round(2))
print("same result:", np.allclose(x_by_hand, x_numpy))
print("x = b + A x holds:", np.allclose(x_numpy, b + A @ x_numpy))
