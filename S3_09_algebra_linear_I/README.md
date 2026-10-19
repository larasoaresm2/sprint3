# S3_09 — Linear Algebra I: matrices and linear transformations

Card: *Álgebra Linear I: Matrizes e Transformações Lineares* (Sprint 3).
Each exercise is solved by hand below and checked with NumPy in `s3_09.py`.

```bash
python3 s3_09.py
```

## 1. Is it a linear transformation?

A function T is linear when **T(u + w) = T(u) + T(w)** and **T(k·u) = k·T(u)**. A quick consequence: a linear T always sends the zero vector to zero.

- **T(x, y) = (2x, x + y)** is linear. With u = (x₁, y₁) and w = (x₂, y₂):
  T(u + w) = (2(x₁ + x₂), (x₁ + x₂) + (y₁ + y₂)) = (2x₁, x₁ + y₁) + (2x₂, x₂ + y₂) = T(u) + T(w), and
  T(k·u) = (2kx₁, kx₁ + ky₁) = k·(2x₁, x₁ + y₁) = k·T(u).
- **S(x, y) = (x + 1, y)** is **not** linear: S(0, 0) = (1, 0) ≠ (0, 0).

## 2. Matrix of a transformation and its dimensions

The columns of the matrix are the images of the basis vectors: T(1, 0) = (2, 1) and T(0, 1) = (0, 1).

```
T = [ 2  0 ]      2 × 2: takes R² to R²
    [ 1  1 ]
```

An n × m matrix takes vectors with **m** entries to vectors with **n** entries. The incidence matrix M of exercise 5 is 3 × 4: it takes the space of the 4 vulnerabilities (R⁴) to the space of the 3 equipments (R³).

## 3. Kernel and image

- **Kernel** (núcleo): the vectors that T sends to zero.
- **Image** (imagem): every vector T can produce.

For T: 2x = 0 and x + y = 0 only when x = y = 0, so the **kernel is {(0, 0)}**. Its determinant is 2·1 − 0·1 = 2 ≠ 0, so T is invertible and its **image is all of R²**.

## 4. Geometric transformations of the plane

| Transformation | Matrix | Example |
| --- | --- | --- |
| Rotation by 90° | `[[0, -1], [1, 0]]` | (1, 0) → (0, 1) |
| Reflection on the x axis | `[[1, 0], [0, -1]]` | (2, 3) → (2, −3) |
| Scale by 2 | `[[2, 0], [0, 2]]` | (1, 2) → (2, 4) |

The scale matrix is **diagonal**: each coordinate is multiplied by its own number. The exposure-factor matrix F of the risk model works the same way.

## 5. Own risk b = M·v (3 equipments, 4 vulnerabilities)

Scenario: E1 is a `Server`, E2 a `WebApplication`, E3 a `Database`. CVSS: V1 = 9.8, V2 = 7.5, V3 = 5.0, V4 = 3.1. E1 has V1 and V3; E2 has V1 and V2; E3 has V3; no equipment has V4.

```
         V1  V2  V3  V4
M = E1 [  1   0   1   0 ]        v = [9.8, 7.5, 5.0, 3.1]
    E2 [  1   1   0   0 ]
    E3 [  0   0   1   0 ]
```

Each entry of b is one row of M times v:

- E1: 1·9.8 + 0·7.5 + 1·5.0 + 0·3.1 = **14.8**
- E2: 1·9.8 + 1·7.5 + 0·5.0 + 0·3.1 = **17.3**
- E3: 0·9.8 + 0·7.5 + 1·5.0 + 0·3.1 = **5.0**

**b = M·v = [14.8, 17.3, 5.0]**. M·v is a combination of the columns of M weighted by the severities: it carries the severity vector from the vulnerability space to the equipment space.

## 6. Composition with the exposure factors: F(M·v) = (F·M)·v

F = diag(1.2, 1.5, 0.8) (Server, WebApplication, Database).

- **F(M·v)**: first b = [14.8, 17.3, 5.0], then each entry times its factor: [1.2·14.8, 1.5·17.3, 0.8·5.0] = **[17.76, 25.95, 4.0]**.
- **(F·M)·v**: F·M multiplies each row of M by the factor of its equipment, `[[1.2, 0, 1.2, 0], [1.5, 1.5, 0, 0], [0, 0, 0.8, 0]]`; times v gives 1.2·9.8 + 1.2·5.0 = 17.76, 1.5·9.8 + 1.5·7.5 = 25.95 and 0.8·5.0 = 4.0 → **[17.76, 25.95, 4.0]**.

Both orders give the same result because matrix multiplication is associative: applying M and then F is the same as applying the composed transformation F·M. This is the own risk `b = F·M·v` used in Asset-Inventory.

## 7. Interpretation in the risk model

- **A null column in M** (V4 here) is a vulnerability that affects no equipment: whatever its CVSS, it adds nothing to any risk.
- **Kernel of M**: the severity vectors with M·v = 0. Solving gives V1 = V2 = V3 = 0 with V4 free, so the kernel is every vector of the form (0, 0, 0, t): severity placed only on vulnerabilities no equipment has. rank(M) = 3, so the kernel has dimension 4 − 3 = 1.
- **Image of M**: rank 3 = number of equipments, so the image is all of R³: any combination of own risks can be produced by some severity vector.

## 8. NumPy

`s3_09.py` repeats every exercise with NumPy (`@` for matrix products, `np.diag`, `np.linalg.det`, `np.linalg.matrix_rank`). Output:

```
=== 1. Is it a linear transformation? ===
T(u + w) == T(u) + T(w): True
T(k u)   == k T(u):      True
S(0) = [1. 0.] -> not (0, 0), so S is not linear

=== 2. Matrix of T and its dimensions ===
[[2. 0.]
 [1. 1.]] shape (2, 2) -> takes R^2 to R^2
T_matrix @ u = [2. 3.] | T(u) = [2. 3.]

=== 3. Kernel and image of T ===
det(T) = 2.0 -> not zero, so kernel = {0} and image = R^2
rank(T) = 2

=== 4. Geometric transformations of the plane ===
rotate (1, 0) by 90 degrees: [0. 1.]
reflect (2, 3) on the x axis: [ 2. -3.]
scale (1, 2) by 2:           [2. 4.]

=== 5. Own risk b = M v (3 equipments, 4 vulnerabilities) ===
M shape (3, 4) -> takes R^4 (vulnerabilities) to R^3 (equipments)
b = M v = [14.8 17.3  5. ]

=== 6. Composition with F: F(Mv) == (FM)v ===
F (M v) = [17.76 25.95  4.  ]
(F M) v = [17.76 25.95  4.  ]
equal: True

=== 7. Null column and kernel of M ===
column V4 = [0. 0. 0.] -> no equipment has V4
M @ [0, 0, 0, 3.1] = [0. 0. 0.] -> a severity only on V4 is in the kernel
rank(M) = 3 -> kernel dimension = 4 - 3 = 1, image = R^3
```

## Applied in the main project

`asset_inventory/risk.py` in [Asset-Inventory](https://github.com/larasoaresm2/Asset-Inventory) builds M, v and F from the inventory and computes `b = F @ M @ v`.
