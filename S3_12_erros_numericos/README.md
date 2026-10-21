# S3_12 — Numerical errors and floating-point representation

Card: *Erros Numéricos e Representação Computacional* (Sprint 3).
This card was done in a reduced version focused on Assignment 2: why comparing floats with `==` fails, why Asset-Inventory checks the condition number instead of comparing the determinant to zero, and why it uses `solve` instead of the inverse. The remaining exercises were covered as reading only.

```bash
python3 s3_12.py
```

## 1. 0.1 + 0.2 is not 0.3

Computers store real numbers in binary (IEEE 754). 0.1 has no exact binary representation, just as 1/3 has none in decimal, so a tiny rounding error remains: `0.1 + 0.2 = 0.30000000000000004`.

Rule: never compare floats with `==`. Use a tolerance: `math.isclose`, `np.isclose` / `np.allclose`, or `pytest.approx` in tests.

## 2. A small determinant does not mean "no inverse"

0.1·I (10 × 10) has det = 0.1¹⁰ = 1e−10, which looks like zero. But the matrix is perfect: its condition number is 1, the best possible value. The determinant shrinks just because the numbers are small; it does not measure how close a matrix is to having no inverse.

## 3. A singular matrix whose determinant does not come out as zero

```
[ 0.1  0.3 ]     row 2 = 7 × row 1, so det = 0.1·2.1 − 0.3·0.7 = 0.21 − 0.21 = 0
[ 0.7  2.1 ]
```

In floating point 0.1·2.1 = 0.21000000000000002, so NumPy returns det ≈ 3.9e−17 and `det == 0` is False. The condition number (≈ 1e16) shows the problem.

Sections 2 and 3 together: **the determinant fails in both directions; the condition number gets both right.**

## 4. solve versus inverse

The condition number says how much errors in the data can grow in the solution: cond ≈ 1 is safe, cond ≈ 1e16 means the answer can be meaningless in double precision.

On the 12 × 12 Hilbert matrix (a classic ill-conditioned example), with b built from a known x:

- `np.linalg.solve`: residual |Hx − b| ≈ 6e−16
- `np.linalg.inv(H) @ b`: residual ≈ 1e−1

Computing the inverse does more operations and accumulates more error; `solve` uses elimination (LU, the method of S3_10) directly.

## 5. The check used in Asset-Inventory

`risk.py` refuses to solve when `cond(I − A)` is not finite or is above `MAX_CONDITION_NUMBER = 1e12`, and then calls `np.linalg.solve`:

- I − A of the S3_10 scenario: cond ≈ 1.73 → solve
- the singular 2 × 2 of section 3: cond ≈ 1e16 → refuse

```
=== 1. 0.1 + 0.2 ===
0.1 + 0.2 = 0.30000000000000004
0.1 + 0.2 == 0.3: False
math.isclose(0.1 + 0.2, 0.3): True

=== 2. det close to zero does not mean singular ===
0.1 * I (10 x 10): det = 9.999999999999996e-11 | cond = 1.0

=== 3. A singular matrix whose det does not come out as zero ===
by hand: 0.1 * 2.1 - 0.3 * 0.7 = 0.21 - 0.21 = 0
in Python: 0.1 * 2.1 = 0.21000000000000002 and 0.3 * 0.7 = 0.21
det = 3.885780586188033e-17 | det == 0: False
cond = 1.1e+16 -> huge, so the matrix is singular

=== 4. solve versus inverse ===
cond(Hilbert 12 x 12) = 1.6e+16
residual |Hx - b| with solve: 6.0e-16
residual |Hx - b| with inv:   1.4e-01

=== 5. The check used in Asset-Inventory ===
I - A of S3_10: cond = 1.73 -> solve
singular 2 x 2: cond = 1.14e+16 -> refuse
```

## Applied in the main project

`asset_inventory/risk.py` in [Asset-Inventory](https://github.com/larasoaresm2/Asset-Inventory): `np.linalg.cond` before solving, `np.linalg.solve` instead of the inverse; the report shows the condition number and the determinant.
