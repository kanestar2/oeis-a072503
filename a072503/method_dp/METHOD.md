# method_dp — transfer-matrix / profile DP for A072503

Everything here was derived from `../DEFINITION.md` only.

## 1. Reformulation

Give each eyelet `e` a **side** `σ(e) = L` if `e <= n`, else `R`, and a **row**
`ρ(e) = min(e, 2n+1-e)`. Then `e ↦ (σ(e), ρ(e))` is a bijection from `{1..2n}`
onto `{L,R} × {1..n}`, and the two eyelets of a row are exactly a horizontal pair.

* Rule 2 (`p_i + p_{i+1} ≠ 2n+1`) says that two consecutive eyelets are never in
  the same row (two distinct eyelets in one row are always a horizontal pair).
* Rule 3 depends only on the sides.
* Rule 1 fixes `p_1 = (L,1)` and `p_{2n} = (R,1)`. Rows 2..n are the **inner rows**,
  and positions 2..2n-1 hold exactly their 2(n-1) eyelets.

So the conditions only depend on which side each eyelet is on and which eyelets
share a row. Any permutation π of the inner rows {2..n}, applied to an eyelet as
`(σ,ρ) ↦ (σ,π(ρ))`, therefore maps lacings bijectively onto lacings. This
symmetry is what the DP uses.

## 2. State (profile)

The lace is built one eyelet at a time. After a valid prefix `p_1..p_t`
(`1 <= t <= 2n-1`, where every eyelet except `2n` may already be placed), its
**profile** is `X = (a, b, c, s, r, f)`:

| field | meaning |
|---|---|
| `a` | # inner rows with neither eyelet used |
| `b` | # inner rows with only the left eyelet used |
| `c` | # inner rows with only the right eyelet used |
| `s` | side of `p_t` (L/R) |
| `r` | length (1 or 2) of the run of equal sides ending at `p_t` (r = 2 means `p_{t-1}` is also on side `s`; rule 3 makes r ≤ 2) |
| `f` | 1 iff `p_t` is an inner eyelet whose partner (other eyelet of its row) is still unused |

The number of inner rows with both eyelets used is `d = (n-1) - a - b - c`.
Row 1 has no class: `1` is always `p_1` and `2n` is always the last eyelet.
The initial profile (after `p_1 = 1`) is `(n-1, 0, 0, L, 1, 0)`. Here `f = 0` is
correct because the partner of eyelet 1 is `2n`, which can never be `p_2` when n ≥ 2.

## 3. Transitions and their multiplicities

Take a fixed valid prefix with profile `X = (a,b,c,s,r,f)` and append one inner
eyelet `e` on side `s'`.

* **Rule 3:** allowed iff not (`s' = s` and `r = 2`). The new run length is `r' = r+1` if `s' = s`, else `r' = 1`.
* **Rule 2:** `e` must not be the partner of `p_t`. This only matters when that
  partner is unused, i.e. `f = 1`. It then lies in row `ρ(p_t)` on side `≠ s`, so
  it is a candidate only when `s' ≠ s`. In that case `ρ(p_t)` belongs to the class
  "only side `s` used" (class `b` if `s = L`, class `c` if `s = R`).

The unused eyelets on side `s'` split into two kinds:

| kind of `e` | # candidates (multiplicity) | new profile |
|---|---|---|
| `s'=L`, row untouched | `a` | `(a-1, b+1, c, L, r', 1)` |
| `s'=L`, row had only R used | `c - [f=1 and s=R]` | `(a, b, c-1, L, r', 0)` |
| `s'=R`, row untouched | `a` | `(a-1, b, c+1, R, r', 1)` |
| `s'=R`, row had only L used | `b - [f=1 and s=L]` | `(a, b-1, c, R, r', 0)` |

* An untouched-row candidate is never the forbidden partner, because the partner
  of `p_t` lies in a half-used row (or is eyelet `2n`, which is not a candidate).
  After such an eyelet its partner is unused, so `f' = 1`. After completing a row, `f' = 0`.
* The new `b` and `c` are computed directly. Whether `p_{t+1}` now ends a run of
  1 or 2 needs only `s` and `r`.

**Last step.** After all `2n-2` inner eyelets are placed (`a = b = c = 0`), the
eyelet `2n` (side R) is appended.

* Rule 2 holds automatically: the partner of `2n` is `1 = p_1 ≠ p_{2n-1}`.
* Rule 3 forbids it exactly when `s = R` and `r = 2`.

So `D(n) = Σ N(0,0,0,s,r,f) · [not (s=R and r=2)]`, where `N(X)` is the number
of valid prefixes of length `2n-1` with profile `X`.

## 4. Why the counts are exact

**Lemma (lumping).** For two valid prefixes `P` and `P'` of the same length with
the same profile `X`, the number of valid completions is the same.

*Proof.* Choose a permutation π of the inner rows that maps:

* the untouched rows of `P` to the untouched rows of `P'`;
* the only-L rows of `P` to the only-L rows of `P'`;
* the only-R rows of `P` to the only-R rows of `P'`;
* the both-used rows of `P` to the both-used rows of `P'`.

The class sizes are equal, so such a π exists. If `f = 1`, also require
`π(ρ(p_t)) = ρ(p'_t)`. Both rows lie in the same class (fixed by `s`), so this
can be arranged.

Applying π to the rows of a completion of `P` (sides kept) gives a sequence of
exactly the unused eyelets of `P'`. Consecutive rows stay different because π is
a bijection, and sides are unchanged, so rules 2 and 3 inside the completion are
preserved. At the junction:

* the side pattern of `p_{t-1}, p_t` is the same for `P` and `P'` (both have `s, r`);
* if `f = 1`, then `p_{t+1}` is the partner of `p_t` iff its image is the partner of `p'_t`;
* if `f = 0`, the row of `p_t` has no unused eyelet left (or `p_t = 1`, whose
  partner `2n` only comes last), so rule 2 at the junction holds automatically.

The map is invertible (use π⁻¹), hence a bijection between the completion sets. ∎

The same argument shows that the number of single eyelets taking a prefix with
profile `X` to a prefix with profile `Y` depends only on `(X, Y)`. That number is
the multiplicity in the table, counted directly in §3. Grouping the valid
prefixes of length `t+1` by their last eyelet gives

    N_{t+1}(Y) = Σ_X N_t(X) · mult(X → Y),

with no over- or under-counting: each prefix arises from exactly one shorter
prefix and one eyelet. This is `dp_forward.py` and `short.py`.

**Backward form (`dp_main.py`).** Let `F(X)` be the number of completions of a
prefix with profile `X`, which is well defined by the lemma. Then

    F(X) = Σ_Y mult(X → Y) F(Y),
    F(0,0,0,s,r,f) = [not (s=R and r=2)].

Neither the transitions nor the terminal values involve `n`, so a single table
serves every `n`:

    D(n) = F(n-1, 0, 0, L, 1, 0).

The states are grouped into layers by `k = 2a + b + c`, the number of inner
eyelets still to place. Each transition lowers `k` by exactly 1, so layer `k` is
computed from layer `k-1` alone, and `D(n)` is read off layer `2(n-1)`. The
whole layer is computed, including states that no `n` reaches. Their values are
never read for a reachable state, so they cannot affect `D(n)`.

In code, with `P = F` on layer `k-1`:

    GL2   = a·P(a-1,b+1,c,L,2,1) + c·P(a,b,c-1,L,2,0)       (append L after an L-run of 1)
    HL1_f = a·P(a-1,b+1,c,L,1,1) + (c-f)·P(a,b,c-1,L,1,0)   (append L after an R)
    GR2   = a·P(a-1,b,c+1,R,2,1) + b·P(a,b-1,c,R,2,0)
    HR1_f = a·P(a-1,b,c+1,R,1,1) + (b-f)·P(a,b-1,c,R,1,0)
    F(L,1,f) = GL2 + HR1_f     F(L,2,f) = HR1_f
    F(R,1,f) = GR2 + HL1_f     F(R,2,f) = HL1_f

A term whose target has a negative coordinate is 0. Its multiplicity is 0 anyway,
except in profiles that cannot occur.

**Evenness.** By the mirror argument in DEFINITION.md, `D(n)` is even. The
program asserts this, and it holds for every computed `n`. Note that `n = 1` is
excluded: the formula would give 1, because "2n is never p_2" fails there. All
computed values are for `n >= 3`, and `D(2) = 0` comes out correctly.

## 5. Complexity

* Layer `k` has `Σ_{a ≤ k/2} (k-2a+1) ≈ k²/4` triples `(a,b,c)`, times 8 for `(s,r,f)`.
  * Up to `n = N`: about `2N³/3` triples in total, or `16N³/3` stored values.
    For N = 400 that is 4.27·10⁷ triples (3.4·10⁸ values). For N = 300 it is 1.80·10⁷ triples.
  * Each value takes O(1) big-integer additions and small-integer multiplications
    (about 16 per triple).
  * The numbers have `O(N log N)` bits. That gives `O(N⁴ log N)` bit operations
    and `O(N³ log N)` bits of memory for one layer.
  * Only two layers are kept at a time, as numpy object arrays of Python ints.
    All arithmetic is exact integer arithmetic: no floats and no modular reduction.
* The forward per-`n` DP (`dp_forward.py`) has `O(n³)` states per `n`. It is
  slower in total (dict based) and is used only as a cross-check.

## 6. Files and commands

All commands are run from `method_dp/`:

    python3 dp_main.py 400        # main run: results.txt (n=3..400) + progress.log
                                  # resumable: tmp/checkpoint.pkl every 5 min and at exit;
                                  # optional 2nd arg = time budget in minutes (default 20)
    python3 dp_forward.py 3 150   # independent per-n forward DP (same transitions, separate code)
    python3 short.py              # < 40 lines, prints a(3..15)
    python3 brute_check.py 6      # literal permutation enumeration, n = 3..6
    mkdir -p tmp && gcc -O2 -o tmp/bitmask_check bitmask_check.c && tmp/bitmask_check 12
                                  # subset DP over eyelets, NO symmetry used, n = 3..12

How `dp_main.py` handles `results.txt`:

* It appends a line `n D(n) a(n)` as soon as that `n` is done (with flush and fsync).
* On a restart it resumes from the checkpoint if one exists.
* For an `n` already in the file it does not write again. It checks that the
  recomputed value equals the stored one, so running it from scratch with the
  file present re-verifies the whole file.
* The program keeps its checkpoint, which is large (about 0.56 GB at k = 798).
  I deleted it by hand after the final run so it would not be committed.
  `python3 dp_main.py 400` therefore starts from scratch: it re-verifies all of
  `results.txt` in about 4 minutes. A larger NMAX then continues past n = 400.

## 7. Checks performed (all passed)

* `dp_main.py`, `dp_forward.py`, `short.py` and `bitmask_check` all reproduce the
  known values a(3..9) = 3, 45, 1824, 109560, 9520560, 1145057760, 181091917440.
* `brute_check.py` (literal enumeration of all orderings with p_1=1, p_2n=2n,
  rules 2 and 3 tested on eyelet numbers) gives D(3..6) = 6, 90, 3648, 219120.
  This equals the DP. It also checks that every mirror image is a lacing different from the original.
* `bitmask_check.c` uses no symmetry and no profile. It agrees with the DP for
  n = 3..12, including a(10), a(11) and a(12).
* `dp_forward.py` agrees with `results.txt` line by line for n = 3..150.
* `short.py` agrees with `results.txt` for n = 3..15.
* The `results.txt` integrity checks found:
  * n = 3..400 contiguous, no duplicates;
  * D = 2a on every line;
  * a full rerun from scratch re-verified every stored value (§8).

New values:

    a(10) = 36441019601280
    a(11) = 9101014585689600
    a(12) = 2761334311015526400
    a(13) = 1000447433001080064000
    a(14) = 426648783674324552140800
    a(15) = 211548372228734725081497600

## 8. Measured wall-clock times

Machine: 4 cores, single-threaded Python 3.13.

| run | wall time | peak RSS |
|---|---|---|
| `dp_main.py 300`, fresh start, n = 3..300 | 67.5 s | 716 MB |
| `dp_main.py 400`, resumed from the k = 598 checkpoint, n = 301..400 | 164.9 s | 1241 MB |
| `dp_main.py 400`, from scratch, re-verifying all 398 stored lines | 253.2 s (cumulative: n=40 at 0.1 s, n=100 at 1.6 s, n=200 at 13.8 s, n=300 at 68.2 s, n=400 at 245.6 s) | 1265 MB |
| `dp_main.py 40` (n = 3..40) | ≈ 0.1 s | |
| `dp_main.py 120` | ≈ 2.6 s | |
| `dp_forward.py 3 12` | 0.05 s | |
| `dp_forward.py 3 150` | 264 s | |
| `short.py` | 0.04 s | |
| `brute_check.py 6` | 14.4 s | |
| `bitmask_check 11` (n = 3..11) | 4.9 s | |
| `bitmask_check 12` (n = 3..12) | 20.6 s | 1.5 GB |

The resumed n = 301..400 run had `dp_forward.py` competing on another core.
