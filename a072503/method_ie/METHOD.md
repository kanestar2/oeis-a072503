# A072503 — method "side templates + inclusion–exclusion over forbidden horizontals"

All counting is exact (Python `int`); no floating point anywhere.
The only project input is `../DEFINITION.md` (rules 1–3, `D(n)`, `a(n) = D(n)/2`).

## 1. Side words

Write *row* `k` for the horizontal pair `{k, 2n+1-k}`: the left eyelet of row `k` is `k`,
the right eyelet of row `k` is `2n+1-k`. An eyelet is fixed by its side and its row.

For a lacing `p_1..p_{2n}` let `w = w_1..w_{2n}` be its **side word**
(`w_i = L` iff `p_i <= n`). Then:

* `w_1 = L` and `w_{2n} = R` (rule 1), and `w` has `n` letters of each kind;
* rule 3 says exactly that `w` contains no `LLL` and no `RRR`.

Call such words **admissible**. Conversely, a fixed admissible `w` together with
a bijection `σ` from the L‑positions of `w` to the rows and a bijection `τ` from the
R‑positions to the rows gives an ordering of all eyelets. Rule 1 means `σ(1) = 1`
and `τ(2n) = 1`. Rule 3 then holds automatically, so only rule 2 remains.

Call a place `i` (between positions `i` and `i+1`) a **switch place** if `w_i ≠ w_{i+1}`.
At a non‑switch place rule 2 holds automatically: two left eyelets add up to at most `2n-1`,
and two right eyelets to at least `2n+3`. At a switch place, rule 2 says the two eyelets are
in different rows. So

    D(n) = Σ_{w admissible} D_w,
    D_w  = #{(σ,τ) : σ(1)=1, τ(2n)=1, row(p_i) ≠ row(p_{i+1}) at every switch place i}.

## 2. Inclusion–exclusion for a fixed word

For a switch place `i`, let `E_i` be the "bad" event `row(p_i) = row(p_{i+1})`. Then
`D_w = Σ_S (-1)^{|S|} |∩_{i∈S} E_i|`, summed over all sets `S` of switch places.

**Lemma.** Let `S` be a set of switch places and `k = |S|`.
* If two places of `S` share a position, or a place of `S` touches position 1 or position `2n`,
  then `|∩_S E_i| = 0`.
* Otherwise `|∩_S E_i| = (n-1)! (n-1-k)!`.

*Proof.*
* *Two places share a position.* If places `j-1` and `j` are both switches, positions
  `j-1` and `j+1` are on the same side and both must have the row of position `j`. But a
  bijection on one side gives distinct positions distinct rows, so this is impossible.
* *A place touches position 1.* If place 1 is in `S`, position 2 is on the right with row
  `σ(1) = 1`. But `τ(2n) = 1` and `2 ≠ 2n` for `n ≥ 2`, so this is impossible. Place `2n-1`
  is symmetric. (This is the special role of the top row.)
* *Otherwise* `S` pairs `k` distinct L‑positions `≠ 1` with `k` distinct R‑positions `≠ 2n`.
  Choose `σ` freely with `σ(1) = 1`: `(n-1)!` ways. All `σ`‑values at those L‑positions are
  in `{2..n}` and distinct. `τ` is then forced on the `k` paired R‑positions, `τ(2n) = 1`,
  and the remaining `n-1-k` R‑positions take the remaining `n-1-k` rows in any order:
  `(n-1-k)!` ways. ∎

So, with `m_k(w)` = the number of `k`‑sets of **interior** switch places (not touching
position 1 or `2n`) no two of which share a position (`k`‑matchings),

    D_w = (n-1)! Σ_k (-1)^k (n-1-k)! m_k(w)
    D(n) = (n-1)! Σ_{k=0}^{n-1} (-1)^k (n-1-k)! N_n(k),     N_n(k) = Σ_w m_k(w).      (★)

Here `k ≤ n-1` because every chosen place uses its own L‑position `≠ 1`.
Example, `n = 3`: the 5 admissible words give `D_w = 0, 2, 2, 0, 2`, so `D(3) = 6`.

## 3. Words by run structure

An admissible word has `2r` runs, alternating and starting with L:
`w = L^{α_1} R^{β_1} L^{α_2} R^{β_2} ... L^{α_r} R^{β_r}`, with `α_i, β_i ∈ {1,2}`,
`Σα_i = Σβ_i = n`. Call `L^{α_i}R^{β_i}` *block* `i`. Its switch places are the *inner*
place `x_i` (L→R inside block `i`, `i = 1..r`) and the *outer* places `y_i` (R→L after
block `i`, `i = 1..r-1`). Add **virtual** places `y_0` (before position 1) and `y_r`
(after position `2n`), and treat them as always chosen. Two consecutive switch places
share a position iff the run between them has length 1. Place `x_1` touches position 1
iff `α_1 = 1`, which is the same as "`y_0` and `x_1` share a position". Likewise, `x_r`
touches position `2n` iff `β_r = 1`, i.e. iff it shares a position with `y_r`. The places
`y_1..y_{r-1}` never touch the ends. Hence a choice of places, written as 0/1‑values,
`x_i, y_i` with `y_0 = y_r = 1`, is a matching of interior places iff for all `i`

    α_i = 1  ⇒  not (y_{i-1} = 1 and x_i = 1),
    β_i = 1  ⇒  not (x_i = 1 and y_i = 1).                                         (C)

So `N_n(k)` is the number of tuples `(r, α, β, x, y_1..y_{r-1})` satisfying (C), with
`Σα = Σβ = n` and `Σx_i + Σ_{i=1}^{r-1} y_i = k`.

## 4. The DP (main program `ie_dp.py`)

Let `F(i, h, s)` be the generating polynomial in `t` (one `t` per chosen real place) of
all tuples for a *prefix* of complete blocks using `i` L's and `h` R's, whose last outer
place has value `s`. Start: `F(0,0,1) = 1` (the virtual `y_0`). A block
`(α, β, x, s')` goes from `(i,h,s)` to `(i+α, h+β, s')` with weight `t^{x+s'}` when (C)
allows it. If this block is the last one, `s' = y_r = 1` is virtual and carries no `t`.
The step into `(n,n,1)` has the same validity rule as the virtual end, plus one factor `t`.
Hence

    N_n(k) = [t^{k+1}] F(n, n, 1).

Pulling sources into a target cell, with `P_s = F(i-α, h-β, s)` and `S = P_0 + P_1`:

    U_α = S + t·(α = 2 ? S : P_0)                 (x = 0, or x = 1 allowed)
    F(i,h,0) = Σ_{α,β} U_α
    F(i,h,1) = t · Σ_{α,β} (β = 2 ? U_α : S)

Cells are computed in layers `m = max(i,h)`. Layer `m` only needs layers `m-1` and `m-2`,
so `n = m` is finished when layer `m` is, and the program runs incrementally in `n`.
Each polynomial is stored **packed** in one Python integer with `B` bits per coefficient.
All coefficients are non‑negative counts. For a cell, a coefficient is at most
(number of words of length `M = i+h ≤ 2N`) × (number of sets of non‑adjacent places)
`≤ 2^{2N}·Fib(2N+2) ≤ 2^{2N}φ^{2N+1} < 2^{3.3885N+0.7}`, so `B = ⌊3.389N⌋+2` bits never
carry. As an extra check, a run with a much larger `B` (1700 instead of 680, `N = 200`) gave
byte‑identical output.

**Complexity.** For all `n ≤ N` together there are `O(N²)` cells with `O(N)` coefficients
and 16 transitions each: `O(N³)` additions of `O(N)`‑bit numbers, i.e. `O(N⁴)` bit
operations. With packing, that is only `O(N²)` big‑integer additions. The final sum (★)
costs `O(n)` multiplications per `n`. Memory is `O(N³)` bits (two layers): 281 MB at
`N = 500`.

## 5. An explicit finite sum (checked in `formula.py`)

Fix `r` and the outer string `y_0..y_r` (`y_0 = y_r = 1`). Given `y`, each block can be
summed over `x_i, α_i, β_i` independently. Using `u` for each L beyond one per run, `v` for
each R beyond one per run, and `t` for chosen places, block `i` contributes
`g(y_{i-1}, y_i)` with

    g(0,0) = (1+t)(1+u)(1+v)          g(1,0) = (1+v)(1+(1+t)u)
    g(0,1) = (1+u)(1+(1+t)v)          g(1,1) = (1+u)(1+v) + t u v

(if `x_i = 1` and the outer place on that side is 1, the run on that side must have length
2; that is the factor `u` resp. `v` instead of `1+u` resp. `1+v`).

Suppose `y_1..y_{r-1}` has `Z` zeros in `q` maximal blocks. There are
`C(Z-1,q-1)·C(r-Z,q)` such strings (convention `C(-1,-1) = 1`). They have `Z-q` steps
(0,0), `q` steps (1,0), `q` steps (0,1), `r-q-Z` steps (1,1), and `r-1-Z` chosen outer
places. Expand
`(1+(1+t)u)^q`, `(1+(1+t)v)^q` and `((1+u)(1+v)+tuv)^{r-q-Z}`, then extract
`[u^{n-r} v^{n-r} t^k]`:

    N_n(k) = Σ_{r,q,Z,e,a,c} C(Z-1,q-1) C(r-Z,q) C(q,a) C(q,c) C(r-q-Z,e)
              · C(r-q-e, n-r-a-e) · C(r-q-e, n-r-c-e) · C(Z-q+a+c, k-r+1+Z-e)

Inserting this into (★) and summing over `k`:

    a(n) = (n-1)!/2 · Σ_{r,q,Z,e,a,c} (-1)^{r-1-Z+e} C(Z-1,q-1) C(r-Z,q) C(q,a) C(q,c) C(r-q-Z,e)
              · C(r-q-e, n-r-a-e) · C(r-q-e, n-r-c-e) · Δ(n-r+Z-e, Z-q+a+c),

    Δ(M, b) = Σ_j (-1)^j C(b,j) (M-j)!   (permutations of M points fixing none of b given points),

with `1 ≤ r ≤ n`, `0 ≤ q ≤ Z ≤ r-1`, `q+Z ≤ r`, `0 ≤ e ≤ r-q-Z`, `0 ≤ a, c ≤ q`.
This is a 6‑fold finite sum, `O(n^6)`. It is only used as an independent check; the DP is
much faster.

## 6. Verification performed (all passed)

| check | script | result |
|---|---|---|
| literal permutation enumeration n = 3..6 (from DEFINITION.md only) | `brute_perm.py 3 6` | D = 6, 90, 3648, 219120 |
| per side word: brute force = general IE over *all* subsets of switch places (union‑find, no matching shortcut) = matching formula `D_w` | `ie_per_word.py compare tmp/brute_3_6.txt` | equal for all 5 + 11 + 26 + 63 words |
| `N_n(k)`: DP = summing `m_k(w)` over enumerated words (n ≤ 11) = explicit 6‑fold sum (n ≤ 16); `D(n)`: DP = Δ‑sum | `formula.py 16` | all equal |
| known terms a(3..9) = 3, 45, 1824, 109560, 9520560, 1145057760, 181091917440 | `ie_dp.py`, `short.py` | reproduced |
| `D(n)` even | asserted for every n | ok, n = 2..500 |
| packing width (B = 680 vs 1700), resume after budget stop, truncated last line, recompute from scratch | `ie_dp.py` in `tmp/` | byte‑identical |
| `short.py` vs `ie_dp.py`, a(3..15) | | equal |

New values: a(10) = 36441019601280, a(11) = 9101014585689600,
a(12) = 2761334311015526400 (more in `results.txt`). Under this definition a(2) = 0; it is
not written to `results.txt`, which starts at n = 3.

## 7. Reproduce

    cd method_ie
    python3 brute_perm.py 3 6 > tmp/brute_3_6.txt        # ~7 s
    python3 ie_per_word.py compare tmp/brute_3_6.txt      # ~0.2 s
    python3 formula.py 16                                  # ~92 s
    python3 short.py                                       # a(3..15), ~0.05 s
    python3 ie_dp.py 500                                   # results.txt, progress.log

`ie_dp.py NMAX [--budget SECONDS]` appends `n D(n) a(n)` lines to `results.txt` and logs to
`progress.log`. Every 120 s it checkpoints the last two layers (unpacked) to
`tmp/ie_dp.ckpt`. It stops cleanly once the budget is used up (default 1400 s); rerunning
the same command continues from the checkpoint. Without a checkpoint it recomputes from
`n = 2` and *verifies* every n already in `results.txt` instead of writing it again.
`sha256(results.txt)` for n = 3..500:
`8298788ed18463c0f5c2f0a44f45b39e3ddc8f499586e61bb91a7f84f7fd448f`.

## 8. Measured wall‑clock times (this machine, Python 3.13, one core)

* `ie_dp.py 200`: 1.3 s
* `ie_dp.py 500`: 49 s without checkpoints; 58.3 s for the official run (45.8 s to reach
  n = 500 plus a 12.5 s final checkpoint); peak RSS 281 MB.
* `ie_dp.py 1000` (exploratory, `B` sized for 1000): reached n = 300 at 19 s, 500 at 88 s,
  700 at 252 s, 800 at 383 s. It was then killed silently, most likely by a memory cap
  (about 2 GB at that point). That is why the official range stops at n = 500. Going further
  would need a smaller memory footprint (e.g. a per-layer coefficient width, or C/GMP);
  that was not attempted.
* `formula.py 16`: 92 s. `brute_perm.py 3 6`: 6.8 s. `short.py`: 0.05 s.

Note: the final checkpoint (`tmp/ie_dp.ckpt`, 81 MB at n = 500) was deleted so that it is not
committed. Rerunning `python3 ie_dp.py 500` recomputes everything in about 1 minute and checks
it against `results.txt`. This was done once more at the end: all 498 lines verified, the file
unchanged.
