# Independent adversarial review — A072503 new terms

Reviewer: independent review agent, 2026-10-20 (UTC 19:33–20:10). Machine: 4 cores, 16 GB, gcc 13.3, Python 3.13.
No existing file was modified. Everything I wrote is in `review/` (scratch and run outputs in `review/tmp/`). No git commands were run.

## 0. Summary

I tried to break the definition, the code and the results. **I found no error in the definition, in any program, or in any accepted term.**
The weaknesses I found are in how the checks are documented (one of them is real: a "re-run verifies results.txt" claim is only true when no checkpoint is present). None of them affects a number.

New evidence from this review, independent of all project code:

* a literal enumeration of canonical lacings (`canon_enum.c`). It gives **a(10) = 36441019601280** and **a(11) = 9101014585689600** exactly, for D(n) = (n-1)!·C(n).
* a third fast method, written from scratch (`glue_ie.py`). It uses inclusion–exclusion over glued rows, with a letter-by-letter DP over side words. It agrees with **all 398 accepted terms** and with all 498 terms of method_ie (n = 3..500).
* Irvine's Java program, ported line by line to C, gives exactly D(3..8). Reading the code confirms that it implements DEFINITION.md exactly.
* The same rules without the horizontal ban reproduce Pfoertner's sister sequence **A078698**, which has a proven closed form. The mirror-symmetric counts reproduce **A078700 = 2·A078702 − A078698**. So the model and the mirror convention are Pfoertner's own.
* Asymptotics: D(n)/A078698(n) → e^{−(1+1/√5)} = 0.2352248073 (Poisson heuristic). The accepted terms, Richardson-extrapolated from n = 50..400, give 0.2352248021.

**Verdict: a(10) = 36441019601280 and all accepted terms a(3..400) should be considered established** (details in §6).

---

## 1. Definition

### 1.1 Is DEFINITION.md the right reading?
* **OEIS text** (snapshot `%I #18`): it starts and ends at the top pair, uses every eyelet, does not distinguish over from under, forbids "three consecutive eyelets on the same side", forbids horizontal connections and divides by 2. DEFINITION.md is a faithful formalisation.
* **Irvine's program** is the source of a(9). I downloaded it to `tmp/dl_java/A072503.java` from github.com/archmageirvine/joeis.
  * It numbers the inner eyelets 0..2m−1 (m = n−1). Left is `e < m`, which is eyelets 2..n.
  * The partner test is `e != 2m−1−current`, the same as `p_i + p_{i+1} ≠ 2n+1`.
  * `sides` holds the last two sides, starting as "R,L". L is forbidden after L,L and R after R,R. The exit to the other top eyelet (on the right) is forbidden after R,R.
  * This is exactly rules 1–3 of DEFINITION.md, with no extra or missing condition. `int`/`long` ranges are irrelevant for n ≤ 9.
  * My line-by-line C port (`irvine_port.c`) gives D = 6, 90, 3648, 219120, 19041120, 2290115520 for n = 3..8. That equals the project's D(n).
* **Sister sequences** (downloaded from oeisdata to `tmp/dl_oeis/`):
  * A078698 is "each eyelet has at least one direct connection to the opposite side", directed, starting and ending at the extreme pair. For an inner eyelet, its rule is logically identical to rule 3: the two neighbours of p_i are not both on p_i's side. For the end eyelets, the top connection 1–2n supplies the opposite side.
  * **Reading C without the horizontal ban** gives D' = 20, 396, 14976, 907200 by literal enumeration (n = 3..6). This is A078698 and its closed form (n−1)!²·Σ_k C(n−k,k)² (`family_check.py`).
  * Method_dp's own transition table with the rule-2 term removed reproduces the A078698 data for n = 3..17 and the closed form for n ≤ 60.
  * The number of lacings fixed by the mirror map μ(p)_i = 2n+1−p_{2n+1−i} (no ban) is 6, 30, 192, 1560. That is 2·A078702 − A078698 = A078700, the "symmetric" lacings.
  * So Pfoertner's mirror convention is μ, the one in DEFINITION.md. A072503 is the A078702-style count (lacings up to mirror image) of A078698 lacings with no inner horizontal.
* **Alternative readings** (`alt_readings.py`, n = 3..6, compared with 2·a(n) = 6, 90, 3648, 219120):

| reading | D(3..6) | matches? |
|---|---|---|
| C (DEFINITION.md) | 6, 90, 3648, 219120 | **yes** |
| C, but start at either top eyelet (both directions) | 12, 180, 7296, 438240 | only as D/4, which is the same count |
| strict zigzag (no same-side step) | 0, 6, 72, 1920 | no |
| C + no vertical-neighbour step | 0, 18, 882, 58300 | no |
| C, but the bottom horizontal (n, n+1) is allowed | 9, 146, 5028, 285984 | no (odd) |
| reading A ("in line", middle eyelet between) | 6, 152, 7476, 577116 | no |
| runs ≤ 3 (no 4 on a side) | 8, 216, 9792, 754800 | no |
| C without the horizontal ban | 20, 396, 14976, 907200 | no (= A078698) |
| no 3-rule at all | 8, 240, 13824, 1263360 | no |

  * Reading B ("adjacent in a line") gives 3, 89, 5554, as in `logs/interpretations_n3-5.log`. I re-ran it and the output is identical.
  * A cyclic reading of rule 3 (wrapping through the top connection) is equivalent: the triples (p_{2n−1}, 2n, 1) and (2n, 1, p_2) are never all on one side.
  * Connecting the top pair is impossible because 1 and 2n are the end points.
  * **Only reading C fits.**
* **a(n) = D(n)/2.**
  * μ is an involution.
  * μ maps lacings to lacings: sides swap, the triple order reverses, and p_i+p_{i+1}=2n+1 ⇔ μ-sum = 2n+1.
  * A fixed point would force p_n + p_{n+1} = 2n+1, which rule 2 forbids. So the proof in DEFINITION.md is correct.
  * Checked by enumeration: there are 0 μ-fixed lacings and the set is μ-closed (n = 3..6). The 6 lacings of the OEIS n=3 example are three μ-pairs.
* **Not checked:** Pfoertner's FORTRAN program (randomwalk.de does not resolve here, and web.archive.org is blocked by the proxy). Its values a(3..8) are reproduced, and so is Irvine's program, so this is a small residual risk only.

### 1.2 Row-relabelling claim (used in the draft comment)
* A permutation of the inner rows 2..n, applied to both eyelets of each row, preserves rules 1–3.
* A non-identity permutation moves some eyelet, so the action is free.
* Each orbit contains exactly one lacing whose inner rows are first visited in the order 2, 3, ..., n. So D(n) = (n−1)!·C(n).
* My literal enumeration of canonical lacings gives C(3..11) = 3, 15, 152, 1826, 26446, 454388, 8982734, 200843362, 5015991284. That is exactly the list in `oeis_draft.txt` and README; the project checked it only for n ≤ 6.

## 2. Code review (line by line)

| program | checked | result |
|---|---|---|
| `brute/interpretations.py` | rules A/B/C, side/row formulas, permutations of 2..2n−1 | correct |
| `brute/brute_dfs.c` | job generation (horizontal 1–a impossible; a,b partner test; triple (1,a,b)), DFS rules, termination at k = 2n−1 with the R,R,R test, `uint32` mask (n ≤ 15), `jobs[1024]` ≥ 784, OpenMP `reduction(+)` plus `critical` for the counter and printing, `path` is thread-local | correct, no race |
| `brute/subset_dp.c` | flag semantics (1 = previous eyelet on the same side), rule 3 (same side only from flag 0), rule 2 (`partner[f]`), first step (flag = left), last step (right: flag 0 only), layers by popcount (writes popcount k, reads k−1 → no race), MODE 2 addition < 2^62 (no overflow), __int128 range (D(12) ≈ 2^62.3; partial counts ≤ 22! < 2^70) | correct |
| `brute/crt.py` | CRT algebra | correct; `assert D < 2**125` is vacuous (always true by construction). The real justification is D(13) < 24! < 2^80 |
| `method_dp/dp_main.py` | slicing for each of the 4 transitions (`[1:]`, `[:-1]`, concat with zero), `cvec` = reversed `bvec`, the subtraction of f only on a side change with partner class b (s=L) / c (s=R), run rules, terminal layer, `D = layer[n−1][ix(L,1,0)][0]`, object arrays (exact ints) | correct |
| `method_dp/short.py`, `dp_forward.py` | same transitions in dict form | correct (same derivation as dp_main, so not an independent method) |
| `method_dp/bitmask_check.c` | uint64 wrap-around exact since D(12) < 2^64, forward order over masks | correct |
| `method_ie/ie_dp.py` | sources always in layers m−1, m−2 (checked); `pop(m−2)` after use; virtual y_0 = (0,1); (C) constraints; `F1 << B`; `N_of` = [t^{k+1}]; packing bound B = ⌊3.389N⌋+2 ≥ log2(2^{2N}·Fib(2N+2)); no subtraction in packed arithmetic; checkpoint re-packs with the new B (safe, since the bound depends only on the layer) | correct |
| `method_ie/formula.py` | matches METHOD.md §5 term by term (k = r−1−Z+e+j, M = r−q−e, Δ index n−r+Z−e) | implements the stated formula |
| `method_ie/ie_per_word.py`, `brute_perm.py` | union-find naive inclusion–exclusion, words generator | correct |
| `compare.py` | load/assert, common range, mismatch test, writes `accepted_terms.txt` | correct (weaknesses W2) |
| `oeis/a072503_oeis.py` (draft program) | same DP as method_dp/short.py | correct; prints a(3..17) = accepted |

* **Hard-coded values:** `grep` for the known terms finds them only in `compare.py` (the comparison table) and `interpretations.py` (a printing aid). No fast method contains a known value or a fudge factor.
* **Hidden dependence:** method_dp imports only numpy/stdlib; method_ie imports only its own files. No shared code, and the formulas are structurally different (a profile DP vs. matching polynomials of side words). I cannot verify agent isolation from the files, but nothing points to copying.

## 3. Re-runs (I did not trust the logs)

Binaries were compiled into `review/tmp/bin` (`gcc -O2 [-fopenmp] [-DMODE=k]`, the project binaries were not used) and deleted afterwards. Python was run with `-B`. Programs that write next to themselves were run on copies.

| command | time | result |
|---|---|---|
| `brute_dfs n`, n = 3..7 | < 1 s | D = 6, 90, 3648, 219120, 19041120 |
| `brute_dfs 8` (4 threads) | 74.2 s | D = 2290115520 (a = 1145057760) |
| `subset_dp_m0 n`, n = 3..12 | n=12: 9.8 s | identical to `logs/subset_dp_exact_n3-12.log` |
| `subset_dp_m1 13`, `subset_dp_m2 13`, `crt.py` | 26.7 + 18.9 s | a(13) = 1000447433001080064000; n = 12 by CRT = exact |
| `bitmask_check 12` (method_dp) | 12 s | n = 3..12 equal |
| `python3 brute/interpretations.py 5` | 0.55 s | byte-identical to `logs/interpretations_n3-5.log` |
| `dp_main.py 150` on a copy containing results.txt (verifying) | 6.4 s | no assertion; file unchanged |
| `dp_main.py 400` **from scratch in an empty dir** | 239 s | new results.txt **byte-identical** (sha256 add30bce…) |
| `ie_dp.py 200` on a copy (verifying) | 1.9 s | no error; file unchanged |
| `ie_dp.py 500 --no-ckpt` **from scratch** | 45 s | new results.txt **byte-identical** (sha256 8298788e…, as in METHOD.md) |
| `short.py` (both) | 0.05 s | a(3..15) equal |
| `formula.py 16` (copy) | 90 s | ALL OK |
| `brute_perm.py 3 6` + `ie_per_word.py compare` | 7 s | ALL OK |
| `brute_check.py 6` | 12 s | D(3..6) |
| `dp_forward.py 3 60` | 5 s | 58 lines equal to results.txt |
| `compare.py` on a copy (with the two results files and the two subset logs) | 0.1 s | output identical to `logs/compare.log`; `accepted_terms.txt` **byte-identical** |

## 4. My own checks (independent code)

| script | method | time | result |
|---|---|---|---|
| `canon_enum.c` (OpenMP) | literal DFS over canonical lacings, rules tested on eyelet numbers; D = (n−1)!·C(n) | n=10: 8.8 s, n=11: 208 s | **a(3..11) exact**, including a(10) = 36441019601280 and a(11) = 9101014585689600 |
| `glue_ie.py 500` | (my own derivation) global inclusion–exclusion over glued inner rows: D = Σ_j (−1)^j C(n−1,j) j! (n−1−j)!² N_n(j), N_n(j) by a letter-by-letter DP with a domino flag (not method_ie's block DP), packed ints, B = 4N+8 | 44 s | equals **all 398 accepted terms** and **all 498** method_ie terms (n = 3..500) |
| `prefix_test.py` | method_dp's lumping lemma, tested on its production code: completions of real prefixes by my memoized search vs F(profile) from `dp_main.next_layer` | 46 s | **882,321 prefixes, 0 mismatches** (all prefixes n = 4..6, 300 random each for n = 8..11) |
| `per_word_test.py 3 9` | method_ie per-word formula D_w vs per-word counts from `canon_enum` (×(n−1)!) | 2 s | all 5+11+26+63+153+376+931 words equal (method_ie only had n ≤ 6) |
| `closed_form.py 70` | METHOD.md §5 sum, implemented from the text (Δ by recurrence, not formula.py) | 147 s | equals accepted, n = 3..70 |
| `alt_readings.py 6`, `family_check.py`, `irvine_port.c` | see §1 | | as stated |
| `sanity.py` | accepted = common part (format, contiguity, newline); D divisible by (n−1)! for all n ≤ 400; growth | s | all OK (below) |
| `asymptotic_check.py` | rho(n) = D(n)/A078698(n) vs e^{−(1+1/√5)} | < 1 s | 0.2352248021 (extrapolated) vs 0.2352248073 |

**Growth.**
* a(n+1)/(a(n)·n²) rises smoothly: 2.497 (n=10), 2.605 (100), 2.6148 (399). It tends to φ² = 2.618, the side-word growth rate.
* log(a(n)/(n−1)!²) has strictly positive second differences for all n ≥ 11 (centred at n = 11..399), with no sign change.
* rho(n) decreases monotonically from n = 5 on.

**Divisibility.**
* D(n) is divisible by (n−1)! for all n ≤ 400, as it must be.
* C(n) = D(n)/(n−1)! is odd only for n = 3, 4. So a(n) is divisible by (n−1)! for 5 ≤ n ≤ 400 (an observation, not needed).
* No other forced factor was predicted, and none was tested.

**Draft files.**
* The `%S` line of `oeis_draft.txt` (a(3..17), 240 characters; a(18) would make 276) equals the accepted terms.
* `oeis/b072503.txt` is n = 3..234: contiguous, equal to accepted, largest term 1000 digits (a(235) has 1005), LF endings.
* The `%F` wording (places 2 ≤ i ≤ 2n−2, w(i) ≠ w(i+1), no two consecutive) is the formula I re-derived independently.

## 5. Findings, ranked by severity

**Definition problems:** none found.

**Code bugs:** none found that affect any result.

**Result problems:** none. Every accepted term was reproduced by at least three independent implementations: method_dp, method_ie and my glue_ie.py. In addition:
* n ≤ 13: the symmetry-free subset DP;
* n ≤ 11: my literal canonical enumeration;
* n ≤ 8: full literal DFS and Irvine's program;
* n ≤ 70: the closed form.

**Weaknesses in the checks / documentation:**

1. **W1 (medium; a check weaker than claimed).** README ("a rerun recomputes and checks each line") and the method docs say that re-running `dp_main.py`/`ie_dp.py` re-verifies results.txt. That is true only when no checkpoint exists.
   * Both programs save a checkpoint at the end of every run (`tmp/checkpoint.pkl`, `tmp/ie_dp.ckpt`).
   * A second identical run then resumes past every n, verifies nothing, and logs "finished" (demonstrated: `dp_main.py 150` → "resumed from checkpoint at layer k=298 … total 0.2s"; `ie_dp.py 200` → "first layer=201 … total 0.0s").
   * The official re-verifications were valid because the checkpoints had been deleted by hand.
   * Fix: document "delete tmp/ first" (or use `ie_dp.py --no-ckpt`; dp_main has no such switch).
2. **W2 (low).** `compare.py` takes the subset-DP values from logs, not from a run. The logs are partly hand-assembled: "(4 threads)" and "n=12 CRT:" are not program output. I re-ran everything and the numbers are identical.
3. **W3 (low).** Several "checks" are re-implementations of the same derivation, not independent methods. METHOD.md is honest about this, but summaries sometimes count them as checks.
   * `dp_forward.py` and `short.py` re-implement dp_main's transitions.
   * `formula.py` checks the same identity (★) as ie_dp.
   * The real independence is: method_dp vs method_ie vs subset DP (and now `canon_enum`, `glue_ie`).
4. **W4 (low).** `crt.py`'s `assert D < 2**125` cannot fail. The justification for exactness is the a-priori bound D(13) ≤ 24! < 2^80, which DECISIONS.md should state.
5. **W5 (low).** `ie_dp.py` silently rewrites results.txt when it finds a malformed line, and re-appends the recomputed value at the end, out of order. It should rather flag a corrupted line during a "verify" run. No such event occurred (progress.log has no "dropped" line).
6. **W6 (low, documentation).**
   * DECISIONS.md D2 supports the model only through A078602 under reading B. The stronger evidence is that **reading C itself** without the ban gives **A078698**, Pfoertner's sister sequence with a proven formula, and that the mirror-fixed counts give A078700.
   * The related .seq files said to have been read are not in the repository; I put copies in `review/tmp/dl_oeis/`.
   * The canonical-count statement is "checked to n = 6" in README/explanation; it is now checked by literal enumeration to n = 11.
   * Suggest adding these to DECISIONS/README and to the editor note.
7. **W7 (info).** Pfoertner's FORTRAN program could not be retrieved, so it was not compared.
8. **W8 (info).** Method_ie's terms n = 401..500 (not accepted) agree with my independent `glue_ie.py`. If wanted, they now have two independent confirmations. This is irrelevant for the b-file, which stops at n = 234 because of the 1000-digit limit.
9. **W9 (info).** Small timing differences from the docs (brute n=8: 74 s here vs 54 s) and an ordering difference in explanation.md ("2, 2, 2, 0 and 0" vs METHOD.md "0, 2, 2, 0, 2", the same multiset). These are harmless.
10. Not reviewed in depth: `recurrence/` (marked as a conjecture and not part of the draft). Its hold-out uses n = 401..500, which `glue_ie.py` has now confirmed.

## 6. Verdict

* **a(10) = 36441019601280 is established.** It is obtained by:
  * five independent computations: the symmetry-free subset DP (re-run), my literal canonical enumeration, method_dp, method_ie and my glue_ie;
  * the closed form;
  * under a definition that is exactly Irvine's program (the source of a(9)) and matches Pfoertner's sister sequences A078698/A078702.
* **a(11) = 9101014585689600, a(12) = 2761334311015526400 and a(13) = 1000447433001080064000** are equally established.
* **All accepted terms a(3..400)** should be considered established. There are three independent exact polynomial-time implementations that agree on every term, and two of them have written proofs that I checked. The lumping lemma and the per-word formula were also tested directly on the production code. Growth and asymptotics are fully consistent.
* The only recommended changes before submission are documentation fixes W1, W4 and W6. No number needs to change.

## 7. Files in review/

* `REVIEW.md`: this report.
* `canon_enum.c`: literal canonical enumeration. Build with `gcc -O2 -fopenmp -o tmp/bin/canon_enum canon_enum.c`; `per_word_test.py` expects that binary.
* `glue_ie.py`: third fast method.
* `prefix_test.py`, `per_word_test.py`: tests of each method's key lemma.
* `closed_form.py`, `alt_readings.py`, `family_check.py`, `irvine_port.c`, `sanity.py`, `asymptotic_check.py`.
* `tmp/runs/*`: outputs of every run listed above (`sha256_before.txt`, `sha256_regenerated.txt`).
* `tmp/dl_java`, `tmp/dl_oeis`: downloaded sources (data only).
* `tmp/dp_copy`, `tmp/ie_copy`, `tmp/compare_copy`, `tmp/oeis_copy`: script copies used for runs. Bulky checkpoints and copies of the results files were deleted after hashing.
* `review/tmp/` is not covered by `.gitignore`; it is about 1.5 MB.
