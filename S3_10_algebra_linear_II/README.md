# S3_10 — Linear Algebra II: linear systems

Card: *Álgebra Linear II: Sistemas Lineares* (Sprint 3).
This card was done in a reduced version focused on Assignment 2: exercises 4 to 6 (the effective-risk system) are solved below. Exercises 1 to 3 (generic 2×2 and 3×3 systems, classification and geometric interpretation) were covered as reading only.

```bash
python3 s3_10.py
```

## 4. The effective-risk equations as (I − A)x = b

Scenario: three equipments (all with exposure factor 1.0). Own risks b = [7.5, 14.8, 0]. E1 inherits 10% of the risk of E2; E3 inherits 50% of E1 and 20% of E2.

Effective risk = own risk + inherited risk:

- x₁ = 7.5 + 0.1·x₂
- x₂ = 14.8
- x₃ = 0 + 0.5·x₁ + 0.2·x₂

In matrix form this is **x = b + A·x**, with

```
A = [ 0    0.1  0 ]      A[i][j] = fraction of the risk of j that i inherits
    [ 0    0    0 ]
    [ 0.5  0.2  0 ]
```

Moving the x terms to the left: x − A·x = b, and since x = I·x, **(I − A)·x = b**.

## 5. Solving by hand (Gauss elimination)

Augmented matrix [I − A | b]:

```
[  1   -0.1  0 |  7.5 ]
[  0    1    0 | 14.8 ]
[ -0.5 -0.2  1 |  0   ]
```

Goal: zeros below the diagonal. Only row 3 needs work.

1. **L3 ← L3 + 0.5·L1** removes the −0.5: [−0.5 + 0.5, −0.2 − 0.05, 1 + 0 | 0 + 3.75] = [0, −0.25, 1 | 3.75]
2. **L3 ← L3 + 0.25·L2** removes the −0.25: [0, −0.25 + 0.25, 1 | 3.75 + 3.7] = [0, 0, 1 | 7.45]

```
[ 1  -0.1  0 |  7.5  ]
[ 0   1    0 | 14.8  ]
[ 0   0    1 |  7.45 ]
```

Back substitution, from the bottom up:

- x₃ = 7.45
- x₂ = 14.8
- x₁ − 0.1·x₂ = 7.5 → x₁ = 7.5 + 1.48 = 8.98

**x = [8.98, 14.8, 7.45]**. The system has exactly one solution (possible and determined), because I − A is invertible (see S3_11).

## 6. Check with NumPy

`np.linalg.solve(I - A, b)` gives the same x, and x = b + A·x holds. This is the same scenario used to validate `asset_inventory/risk.py`.

```
=== 4. The equations as (I - A) x = b ===
I - A =
 [[ 1.  -0.1  0. ]
 [ 0.   1.   0. ]
 [-0.5 -0.2  1. ]]
b = [ 7.5 14.8  0. ]

=== 5. Gauss elimination by hand ===
start:
 [[ 1.  -0.1  0.   7.5]
 [ 0.   1.   0.  14.8]
 [-0.5 -0.2  1.   0. ]]
L3 <- L3 + 0.5 L1:
 [[ 1.   -0.1   0.    7.5 ]
 [ 0.    1.    0.   14.8 ]
 [ 0.   -0.25  1.    3.75]]
L3 <- L3 + 0.25 L2:
 [[ 1.   -0.1   0.    7.5 ]
 [ 0.    1.    0.   14.8 ]
 [ 0.    0.    1.    7.45]]
back substitution: x = [ 8.98 14.8   7.45]

=== 6. Check with NumPy ===
np.linalg.solve:   x = [ 8.98 14.8   7.45]
same result: True
x = b + A x holds: True
```

## Applied in the main project

`asset_inventory/risk.py` in [Asset-Inventory](https://github.com/larasoaresm2/Asset-Inventory) builds A from the registered dependencies and solves `np.linalg.solve(np.eye(n) - A, b)`.
