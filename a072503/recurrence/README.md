# Search for a recurrence (empirical, NOT proven)

Sequence tested: `T(n) = D(n)/(n-1)! = 2*a(n)/(n-1)!` (always an integer — this
part *is* proved, see the inclusion-exclusion formula in `../method_ie/METHOD.md`:
`D(n) = (n-1)! * sum_k (-1)^k (n-1-k)! N_n(k)`).
T(3..11) = 3, 15, 152, 1826, 26446, 454388, 8982734, 200843362, 5015991284.

Terms used: `../method_ie/results.txt` (n = 3..500; n = 3..400 are confirmed by
both methods).

Method: look for `sum_{i=0..R} P_i(n) T(n+i) = 0` with polynomials `deg P_i <= d`,
by computing the rank of the linear system modulo a prime (`guess_np.py`,
`mindeg.py`), then a hold-out test (`holdout.py`).

Findings:
* No recurrence of order R <= 17 with degree <= d_max(R) (d_max = 232 for R = 1,
  ..., 24 for R = 17) — `guess_np_T.log`.  Lower orders with higher degree cannot
  be excluded with 500 terms.
* **Order 18, degree 18**: the solution space modulo p is exactly one-dimensional
  (361 unknowns, 480 equations).  Fitted on n <= 420 only, the recurrence holds
  for all 80 remaining equations (terms up to a(500)), modulo p = 2^31-19 and
  p = 10^9+7 — `holdout.log`.  Smaller degree is possible at higher order
  (order 22 / degree 10, order 26 / degree 8, ...) — `mindeg.log`.
* Status: **conjecture**, supported by 80 held-out terms.  Not proved; the exact
  rational coefficients were not computed (they are expected to be huge).
  That some P-recurrence exists is expected in theory (the formula is a finite
  sum of hypergeometric terms, hence holonomic), but its order was not derived.

Reproduce (from this folder): `python3 guess_np.py T 40 ../method_ie/results.txt`,
`python3 mindeg.py 18 26`, `python3 holdout.py 18 18 420 2147483629`,
`python3 holdout.py 18 18 420 1000000007` (the two hold-out runs take about 25 s together;
their output, which names each prime p, is `holdout.log`).
