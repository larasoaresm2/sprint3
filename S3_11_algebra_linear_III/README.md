# S3_11 — Linear Algebra III: determinants and invertibility

Card: *Álgebra Linear III: Determinantes e Invertibilidade* (Sprint 3).
This card was done in a reduced version focused on Assignment 2: when I − A has an inverse, an example where it does not, and why the row-sum rule guarantees it. Determinant drills (Sarrus, cofactors on generic matrices) were covered as reading only.

```bash
python3 s3_11.py
```

## 1. Determinant of I − A in the S3_10 scenario

```
I − A = [  1   -0.1  0 ]
        [  0    1    0 ]
        [ -0.5 -0.2  1 ]
```

Expanding along row 2 (only one non-zero entry): det = 1 · det([[1, 0], [−0.5, 1]]) = 1 · (1·1 − 0·(−0.5)) = **1**. Not zero, so the system has exactly one solution.

## 2. A dependency matrix that breaks the model

E1 inherits 100% of the risk of E2 and E2 inherits 100% of E1:

```
A = [ 0  1 ]      I − A = [  1  -1 ]      det = 1·1 − (−1)·(−1) = 0
    [ 1  0 ]              [ -1   1 ]
```

The equations are x₁ = b₁ + x₂ and x₂ = b₂ + x₁. Substituting: x₁ = b₁ + b₂ + x₁, so b₁ + b₂ = 0. With positive own risks this never holds: **there is no solution**, the risk would loop between the two equipments forever. `np.linalg.solve` refuses with *Singular matrix*.

Asset-Inventory would reject this A: each row sums to 1, and `add_dependency` only accepts rows that sum to less than 1.

## 3. The rule: every row of A sums to less than 1

```
A = [ 0     0.4   0.5 ]   row sums: 0.9, 0.9, 0.9
    [ 0.3   0     0.6 ]
    [ 0.45  0.45  0   ]
```

By cofactors along row 1 of I − A:
det = 1·(1·1 − (−0.6)(−0.45)) − (−0.4)·((−0.3)·1 − (−0.6)(−0.45)) + (−0.5)·((−0.3)(−0.45) − 1·(−0.45))
= 0.73 − 0.228 − 0.2925 = **0.2095** ≠ 0.

**Why the rule always works.** On every row of I − A the diagonal is 1 and the other entries add up (in absolute value) to the row sum of A, which is less than 1: the matrix is *strictly diagonally dominant*. Proof that it is invertible:

1. Suppose some x ≠ 0 has (I − A)x = 0, that is, x = A·x.
2. Take the entry xᵢ with the largest absolute value. Row i says xᵢ = Σⱼ Aᵢⱼ·xⱼ.
3. Every |xⱼ| ≤ |xᵢ|, so |xᵢ| ≤ (Σⱼ Aᵢⱼ)·|xᵢ| < |xᵢ|, because the row sum is less than 1.
4. A number cannot be smaller than itself, so no such x exists: the only solution of (I − A)x = 0 is x = 0, and I − A is invertible.

```
=== 1. Determinant of I - A in the S3_10 scenario ===
I - A =
 [[ 1.  -0.1  0. ]
 [ 0.   1.   0. ]
 [-0.5 -0.2  1. ]]
det(I - A) = 1.0 -> not zero, so there is one solution

=== 2. A dependency matrix that breaks the model ===
I - A =
 [[ 1. -1.]
 [-1.  1.]]
det(I - A) = 0.0 -> zero, so I - A has no inverse
np.linalg.solve refuses: Singular matrix
row sums of A: [1. 1.] -> 1, so Asset-Inventory would reject it

=== 3. The rule: every row of A sums to less than 1 ===
row sums of A: [0.9 0.9 0.9]
I - A =
 [[ 1.   -0.4  -0.5 ]
 [-0.3   1.   -0.6 ]
 [-0.45 -0.45  1.  ]]
on every row, the diagonal (1) is bigger than the sum of the others (0.9)
det(I - A) = 0.2095 -> not zero, so I - A is invertible
```

## Applied in the main project

`Inventory.add_dependency` in [Asset-Inventory](https://github.com/larasoaresm2/Asset-Inventory) rejects a dependency that would make the row sum of A reach 1, so `risk.py` always receives an invertible I − A.
