# OEIS A072503 — new terms

**A072503**: number of ways to lace a shoe with n eyelet pairs such that there
is no direct "horizontal" connection between any adjacent eyelet pair.
The OEIS (oeisdata snapshot of 2026-10-20) knows a(3..9). This work obtains
**a(10) … a(400)**.

## Final terms

| n | a(n) | confirmed by |
|---|---|---|
| 3 | 3 | OEIS; brute-force enumeration; direct DP; method 1; method 2 |
| 4 | 45 | same |
| 5 | 1824 | same |
| 6 | 109560 | same |
| 7 | 9520560 | same |
| 8 | 1145057760 | same |
| 9 | 181091917440 | OEIS (Irvine 2024); direct DP; method 1; method 2 |
| **10** | **36441019601280** | **direct DP; method 1; method 2 — new** |
| 11 | 9101014585689600 | direct DP; method 1; method 2 — new |
| 12 | 2761334311015526400 | direct DP; method 1; method 2 — new |
| 13 | 1000447433001080064000 | direct DP (2 moduli + CRT); method 1; method 2 — new |
| 14 | 426648783674324552140800 | method 1; method 2 — new |
| 15 | 211548372228734725081497600 | method 1; method 2 — new |
| 16 | 120678246106857751226923008000 | method 1; method 2 — new |
| 17 | 78477648409428536071705853952000 | method 1; method 2 — new |
| 18…400 | `accepted_terms.txt` | method 1; method 2 — new |

* `accepted_terms.txt` — all accepted terms n = 3..400 in b-file format
  (`n a(n)`). A term is accepted only if both independent methods gave the
  same number. There is not a single discrepancy.
* `oeis/b072503.txt` — the b-file for OEIS, n = 3..233. Beyond that the
  b-file lines would be longer than 1000 characters (an OEIS guideline), and
  from n = 235 the numbers themselves have more than 1000 digits.
* Method 2 also computed n = 401..500 (`method_ie/results.txt`), but the other
  method did not check them, so they are **not** accepted.

## Definition (in brief)

Eyelets 1..n are on the left from top to bottom, n+1..2n on the right from
bottom to top; the pairs are (k, 2n+1−k). A lacing is an order of visiting all
2n eyelets, from 1 to 2n, in which (a) there is no step within a single pair
and (b) no three consecutive eyelets lie on the same side.
a(n) = (number of such orders)/2: they come in mirror pairs, and none is
symmetric. The exact statement is in `DEFINITION.md`, and why this particular
interpretation was chosen is in `DECISIONS.md` (D2). It is the only one that
gives a(4) = 45 and a(5) = 1824, and it agrees with Irvine's program.
Moreover, the same rules without the ban on horizontal connections give
exactly A078698, a related sequence by the same author, Pfoertner.

## How to reproduce each number

Everything is run from the `a072503/` folder. You need gcc with OpenMP and
Python 3.8+ (method 1 uses numpy).

| what | command | time (4 cores, 16 GB) |
|---|---|---|
| choosing the interpretation, n = 3..5 | `python3 brute/interpretations.py 5` | 0.5 s |
| full brute-force enumeration, a(3..8) | `gcc -O3 -march=native -fopenmp -o brute/brute_dfs brute/brute_dfs.c && for n in 3 4 5 6 7 8; do brute/brute_dfs $n; done` | n = 8: 54 s |
| direct subset DP, a(3..12) exactly | `gcc -O3 -march=native -fopenmp -DMODE=0 -o brute/subset_dp_m0 brute/subset_dp.c && for n in $(seq 3 12); do brute/subset_dp_m0 $n; done` | n = 12: 13 s, 3 GB |
| direct DP, a(13) | `gcc ... -DMODE=1 -o brute/subset_dp_m1 ...`, `-DMODE=2 -o brute/subset_dp_m2 ...`; `brute/subset_dp_m1 13`, `brute/subset_dp_m2 13`; `python3 brute/crt.py 13 <D1> <D2>` | 23 s + 14 s, 6.4 GB |
| **method 1**, a(3..400) | `cd method_dp && python3 dp_main.py 400` | 253 s, 1.3 GB (n ≤ 100: 1.6 s) |
| **method 2**, a(3..500) | `cd method_ie && python3 ie_dp.py 500` | 58 s, 0.3 GB (n ≤ 200: 1.3 s) |
| comparison and `accepted_terms.txt` | `python3 compare.py` | < 1 s |
| short programs, a(3..15) / a(3..17) | `python3 method_dp/short.py`, `python3 method_ie/short.py`, `python3 oeis/a072503_oeis.py` | < 0.1 s |
| D(n)/(n−1)! = "canonical" lacings | `python3 brute/canonical_check.py 6` | 8 s |
| recurrence search | `cd recurrence && python3 guess_np.py T 40 ../method_ie/results.txt; python3 holdout.py 18 18 420 2147483629` | 2 min + 1 min |

The programs `dp_main.py` and `ie_dp.py` are resumable. They append one line
per n, write a log (`progress.log`), save checkpoints to `tmp/` (not tracked
by git) and stop at a time limit (20 and 23 minutes by default). If
`results.txt` already exists, a rerun recomputes and **checks** each line
instead of overwriting it. But this holds only for a run **without a
checkpoint**: a checkpoint is saved at the end of every run, and the next run
resumes from it without checking anything. So to re-verify, first delete
`method_dp/tmp/checkpoint.pkl` and `method_ie/tmp/ie_dp.ckpt` (or run
`python3 ie_dp.py 500 --no-ckpt`).

## How the numbers were established

1. **Priority check**: `seq/A072/A072503.seq` from github.com/oeis/oeisdata
   (sparse checkout, commit f72d165 of 2026-10-20, copy
   `A072503_oeisdata_snapshot.seq`). There is no a(10) there, and the keyword
   is `more`.
2. **The definition** was reconstructed by brute-force enumeration and matched
   the known a(3..8) (`brute/`, `logs/`).
3. **Two independent fast methods** were written by two different agents that
   saw only `DEFINITION.md` and the known terms. They did not know our
   intermediate numbers.
   * `method_dp/` — dynamic programming over states: how many rows are
     untouched, how many have only the left eyelet used and how many have only
     the right eyelet used, plus a few bits of local information. About n³
     states.
   * `method_ie/` — a sum over side patterns (words over L/R without LLL and
     RRR), with horizontals accounted for by inclusion–exclusion. Formula:
     `2a(n) = (n−1)! Σ_k (−1)^k (n−1−k)! N(n,k)`.
   Both reproduce a(3..9) and were checked against their own brute-force
   enumerations.
4. **A third check**, using no symmetry at all — a direct subset DP
   (`brute/subset_dp.c`), n = 3..13.
5. **Comparison** (`compare.py`, `logs/compare.log`): methods 1 and 2 agree for
   n = 3..400, and the direct DP agrees with them for n = 3..13.
6. **The reviewer agent** (`review/REVIEW.md`) looked for an error and **found
   none**, whether in the interpretation, the code or the numbers. It did the
   following:
   * rebuilt both `results.txt` files from scratch; they matched byte for byte;
   * wrote its own enumeration of "canonical" lacings, which gives a(3..11)
     directly, including a(10) (`review/canon_enum.c`);
   * wrote a third fast method (`review/glue_ie.py`); it agreed for n = 3..500;
   * checked the key lemma of method 1 on 882 thousand real lacing prefixes;
   * checked the formula of method 2 for every side word for n = 3..9;
   * found one more confirmation of the interpretation: the same rules without
     the ban on horizontal connections give the neighbouring A078698 by
     Pfoertner.

   Verdict: a(10) and all of a(3..400) are established. Its remarks concerned
   only the documentation; what was done about them is in `DECISIONS.md`, D5.

## Formulas: what is proved and what is not

* **Proved:** the inclusion–exclusion formula (`method_ie/METHOD.md`, which
  also gives an explicit 6-fold binomial sum) and the exactness of method 1
  (`method_dp/METHOD.md`). It is also proved that 2a(n) is divisible by
  (n−1)!: the quotient is the number of lacings in which the inner pairs first
  appear in the order 2..n (`explanation.md`, section 4). This was checked by
  brute-force enumeration up to n = 6, and by the reviewer up to n = 11.
* **Only a conjecture:** 2a(n)/(n−1)! satisfies a linear recurrence of order 18
  with polynomial coefficients of degree 18. It was found modulo primes,
  fitted on n ≤ 420, and holds for all subsequent terms up to n = 500. The
  coefficients are not written out (`recurrence/README.md`).

## Time spent

* The whole work took about 1 h 25 min (18:56–20:20 UTC, 2026-10-20). The
  agents for methods 1 and 2 worked in parallel for ~18 and ~28 minutes, the
  reviewer for ~39 minutes.
* Net machine time for the new numbers is a few minutes (table above). The
  longest runs are the full brute-force enumeration for n = 8 (54 s) and
  method 1 up to n = 400 (4 min). No run came close to the 25-minute limit.

## Files

| file / folder | contents |
|---|---|
| `README.md` | this file (Russian version: `README_ru.md`) |
| `explanation.md` | detailed explanation for a non-specialist, with a worked example for n = 3 (Russian original: `explanation_ru.md`) |
| `oeis_draft.txt` | draft of the OEIS edit (new terms, formula, Python program, Extensions line). Nothing has been submitted. **Read its header first: the OEIS rules on AI** (Russian: `oeis_draft_ru.txt`) |
| `oeis/` | the b-file and the program from the draft |
| `DEFINITION.md` | the exact definition given to the agents |
| `DECISIONS.md` | log of the decisions made, with their justifications |
| `accepted_terms.txt`, `compare.py` | accepted terms and the comparison |
| `brute/` | brute-force enumeration, direct subset DP, checks of the interpretations |
| `method_dp/`, `method_ie/` | the two independent methods (code, METHOD.md, results.txt, logs) |
| `recurrence/` | recurrence search (empirical) |
| `review/` | the reviewer's report (`REVIEW.md`) and its own checks |
| `logs/` | logs of all runs |
