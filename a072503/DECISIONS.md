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
