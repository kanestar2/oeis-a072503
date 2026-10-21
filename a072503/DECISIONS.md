# Decision log

Decisions taken without the user (as instructed), with the evidence for each.

## D1. Has a(10) already been published?  (stage 1, 2026-10-20)
* `seq/A072/A072503.seq` taken from github.com/oeis/oeisdata by sparse checkout
  (oeisdata commit `f72d165f5ec0c8ad0efbe3c8a3cdb2543ef6272b`, dated 2026-10-20).
  The file (copy: `A072503_oeisdata_snapshot.seq`, `%I #18 Oct 07 2024`) still
  ends at a(9) = 181091917440 and carries the keyword `more`.  So a(10) is not in
  OEIS yet; work continues.
* The related files A078602, A078629, A078676, A078698, A078702, A002866 were
  also read for context (A002866: lacings with *all* horizontals present).

## D2. Reading of the rules  (stage 2)
The OEIS text allows several readings of "three consecutive eyelets on the
same side are not permitted".  Three readings were tested by literal
enumeration of all permutations (`brute/interpretations.py`, log
`logs/interpretations_n3-5.log`):

| reading | n=3 | n=4 | n=5 |
|---|---|---|---|
| A: three lace-consecutive eyelets in one column, the middle one between the others | 3 | 76 | 3738 |
| B: same, but the three eyelets are neighbours in the column (the "in a line" rule of A078602) | 3 | 89 | 5554 |
| **C: any three lace-consecutive eyelets on the same side** | **3** | **45** | **1824** |
| OEIS | 3 | 45 | 1824 |

* All three readings give exactly the six lacings of the OEIS example for n=3,
  but only **C** reproduces a(4) and a(5).  Reading C is also exactly what
  Sean Irvine's Java program (jOEIS `A072503.java`, read from
  github.com/archmageirvine/joeis) implements.
* Cross-check of the model: reading B *without* the horizontal ban gives
  21, 601, 34278 = A078602(3..5), so the numbering and the path model are right.
* Stronger cross-check found by the reviewer (`review/REVIEW.md` §1): reading C
  *without* the horizontal ban gives 20, 396, 14976, 907200 = A078698(3..6)
  (Pfoertner's sister sequence "each eyelet has a direct connection to the
  opposite side", which for inner eyelets is the same condition as rule 3), and
  the mirror-fixed lacings then give A078700 = 2*A078702 - A078698.  So reading C
  and the mirror convention are Pfoertner's own.  Nine other readings tested by
  the reviewer do not fit the known terms.
* **Decision: reading C** (see `DEFINITION.md` for the final wording).
* Direction/mirrors: we count orderings that start at 1 and end at 2n and divide
  by 2.  This is the same as counting undirected lacings up to left-right mirror
  image; the proof that no lacing is its own mirror image is in `DEFINITION.md`.
* Under reading C the lace may go from one eyelet to *any* other eyelet
  (including skipping eyelets on the same side, e.g. 1 -> 3); the only
  forbidden direct connections are the horizontal ones.  This matches the
  n = 3 example (135426 uses 1 -> 3).

## D3. Brute force results  (stage 2)
`brute/brute_dfs.c` enumerates the lacings one by one (DFS, OpenMP):
n = 3..8 give 3, 45, 1824, 109560, 9520560, 1145057760 — all equal to OEIS
(logs in `logs/brute_dfs_*.log`, n = 8 took 54 s on 4 threads).

## D4. Third, "direct" check: dynamic programming over subsets  (stage 3)
Independent of the two fast methods (which are written by separate agents that
see only `DEFINITION.md`), `brute/subset_dp.c` counts lacings by a Held-Karp
table indexed by (set of used eyelets, last eyelet, "previous eyelet on the same
side?").  It is the definition translated literally, with no symmetry argument,
so it serves as an exact semi-brute-force reference beyond the reach of
enumeration.  Exponential: table 2^(2n-2)*(2n-2)*2 entries.
* n = 3..12 exact with unsigned __int128 (`logs/subset_dp_exact_n3-12.log`):
  reproduces all seven known terms a(3..9), and gives
  a(10) = 36441019601280, a(11) = 9101014585689600, a(12) = 2761334311015526400.
* n = 13 needs 6.4 GB with 64-bit cells, so it is run twice (mod 2^64 and mod
  2^61-1) and combined by CRT (`brute/crt.py`; checked on n = 12 against the exact
  run): a(13) = 1000447433001080064000 (`logs/subset_dp_crt_n12-13.log`).
  The CRT value is exact because 0 <= D(n) <= (2n-2)! and 24! < 2^80 is far
  below 2^64*(2^61-1); `crt.py` now asserts (2n-2)! < 2^64*(2^61-1) (true for n <= 17).
* Decision: these values are NOT given to the method agents (independence);
  they are compared with the agents' results afterwards.
* n = 14 would need ~28 GB in this layout (or a layered table with ranking);
  not done.

## D5. Independent review  (stage 7)
A separate reviewer agent (`review/REVIEW.md`) re-ran every program (two
from-scratch rebuilds of both `results.txt` were byte-identical), wrote its own
checks — a literal enumeration of "canonical" lacings giving a(3..11)
directly (`review/canon_enum.c`), a third fast method (`review/glue_ie.py`,
agrees for n = 3..500), a test of method 1's key lemma on 882 321 real
prefixes, and a per-side-word test of method 2 for n = 3..9 — and found **no
error in the definition, the code or the numbers**.  Verdict: a(10) and all
accepted terms a(3..400) are established.  Its documentation remarks and what
was done about them:
1. *Re-verification of `results.txt` only happens without a checkpoint.*  Both
   programs save a checkpoint at the end; a second run then checks nothing.
   -> README now says: delete `method_dp/tmp/checkpoint.pkl` /
   `method_ie/tmp/ie_dp.ckpt` first, or use `ie_dp.py --no-ckpt`.
2. *`compare.py` reads the subset-DP values from logs, and two log lines had
   been written by hand.*  -> `logs/brute_dfs_n8.log` and
   `logs/subset_dp_crt_n12-13.log` were regenerated by re-running the programs
   (same numbers).  `compare.py` still reads the logs (the subset DP for n = 13
   takes 40 s and 6.4 GB, so it is not re-run on every comparison); this is
   documented here.
3. *`dp_forward.py`, `short.py`, `formula.py` are implementation checks, not
   independent methods.*  Agreed; they are not counted as such.  The two
   independent methods are method_dp and method_ie (plus the subset DP and the
   reviewer's own `glue_ie.py`).
4. *The CRT assertion `D < 2^125` could never fail.*  -> replaced by the real
   argument (see D4).
5. *`ie_dp.py` silently repairs a malformed last line.*  Never happened (the
   file was rebuilt byte-identically twice); left as is, documented here.
6. *Mention the A078698/A078700 evidence and that the canonical counts
   2a(n)/(n-1)! are now checked to n = 11.*  -> added to D2, README,
   explanation.md and the editor note in oeis_draft.txt.
7. Pfoertner's FORTRAN program could not be fetched (host does not resolve,
   web archive blocked).  Residual risk is small: its values a(3..8) and
   Irvine's a(9) are reproduced.
Observation by the reviewer (not needed, not proved): 2a(n)/(n-1)! is odd only
for n = 3, 4, so a(n) is divisible by (n-1)! for 5 <= n <= 400.
