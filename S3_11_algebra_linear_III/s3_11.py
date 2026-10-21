"""S3_11 - Linear Algebra III: determinants and invertibility.

Shows a dependency matrix A that makes I - A singular, and checks the rule
used in Asset-Inventory: if every row of A sums to less than 1, I - A is
invertible.
"""
import numpy as np

print("=== 1. Determinant of I - A in the S3_10 scenario ===")
A = np.array([[0.0, 0.1, 0.0],
              [0.0, 0.0, 0.0],
              [0.5, 0.2, 0.0]])
system = np.eye(3) - A
print("I - A =\n", system)
print("det(I - A) =", round(np.linalg.det(system), 6), "-> not zero, so there is one solution")

print("\n=== 2. A dependency matrix that breaks the model ===")
# E1 inherits 100% of E2 and E2 inherits 100% of E1
A_bad = np.array([[0.0, 1.0],
                  [1.0, 0.0]])
system_bad = np.eye(2) - A_bad
print("I - A =\n", system_bad)
print("det(I - A) =", np.linalg.det(system_bad), "-> zero, so I - A has no inverse")
try:
    np.linalg.solve(system_bad, np.array([5.0, 3.0]))
except np.linalg.LinAlgError as error:
    print("np.linalg.solve refuses:", error)
print("row sums of A:", A_bad.sum(axis=1), "-> 1, so Asset-Inventory would reject it")

print("\n=== 3. The rule: every row of A sums to less than 1 ===")
# Heavy dependencies, but each row still sums to 0.9
A_heavy = np.array([[0.0,  0.4,  0.5],
                    [0.3,  0.0,  0.6],
                    [0.45, 0.45, 0.0]])
system_heavy = np.eye(3) - A_heavy
print("row sums of A:", A_heavy.sum(axis=1))
print("I - A =\n", system_heavy)
print("on every row, the diagonal (1) is bigger than the sum of the others (0.9)")
print("det(I - A) =", round(np.linalg.det(system_heavy), 4), "-> not zero, so I - A is invertible")
