# A072503: how the new terms were computed — an explanation for non-specialists

## 0. In brief

The sequence A072503 counts the ways to lace a shoe with `n` pairs of
eyelets so that the lace never runs “straight across” the shoe between the two
eyelets of one row. OEIS knows the terms up to `n = 9`. We obtained

| n | a(n) |
|---|---|
| 10 | 36441019601280 |
| 11 | 9101014585689600 |
| 12 | 2761334311015526400 |
| 13 | 1000447433001080064000 |
| 14 | 426648783674324552140800 |
| 15 | 211548372228734725081497600 |
| 16 | 120678246106857751226923008000 |
| 17 | 78477648409428536071705853952000 |

and so on up to `n = 400` (file `accepted_terms.txt`).

Every number was obtained by **two different counting methods**, written by
two different implementers who were instructed not to read each other's work
(section 8). The numbers agree for every `n` from 3 to 400. Both methods
reproduce all seven previously known terms. For `n ≤ 13` there is a third,
“direct” method, and it agrees too. For `n ≤ 8` all lacings were, in addition,
enumerated one by one.

Where this text says “proved”, a written proof exists in the section or file
cited. The proofs were written by AI agents and checked by the reviewer agent,
not yet by an independent human expert.

Below, step by step: what exactly is counted, using `n = 3` as an example; how
both methods work; and why they can be trusted.

---

## 1. What we count

### 1.1. The shoe and the numbering

The shoe has `n` rows of eyelets; each row has a left and a right eyelet. The
numbering is the same as that of the sequence's author (Hugo Pfoertner): on the
left from top to bottom `1, 2, …, n`, on the right from bottom to top
`n+1, …, 2n`. For `n = 3`:

```
              left side      right side
row 1 (top)      1 ●             ● 6      ← top pair: the lace starts and ends here
row 2            2 ●             ● 5
row 3 (bottom)   3 ●             ● 4
```

The eyelets of one row are the pairs `(1,6)`, `(2,5)`, `(3,4)`. In general,
the pair of row `k` is `(k, 2n+1−k)`: the two numbers always add up to `2n+1`.

### 1.2. What a lacing is

A lacing is an order in which the eyelets are visited: the lace passes through
the eyelets `p1, p2, …, p2n` in turn. Only the order matters, not whether the
lace passes over or under (“over/under” is not distinguished). The rules are as
follows.

1. **Start and end in the top pair.** The lacing starts at eyelet 1 and
   ends at eyelet `2n` (the ends of the lace stick out at the top, where they
   are tied).
2. **Each eyelet is used exactly once.**
3. **No “horizontals”.** The lace cannot go directly from one eyelet of a row
   to the other eyelet of the same row (the transitions 2↔5, 3↔4 are forbidden
   for `n = 3`). In terms of numbers: two numbers that are adjacent in the
   lacing never add up to `2n+1`.
4. **At most two consecutive eyelets on the same side.** No three consecutive
   eyelets of the lacing lie on the same side. Without this rule the lace could
   run along one edge for a long time and would not hold the shoe together.

All other transitions are allowed: diagonally across the whole shoe, along an
edge skipping an eyelet (for example, 1 → 3), and so on.

Finally, a lacing and its **mirror image** (left and right sides swapped) are
counted as the same lacing. So the answer is the number of orders satisfying
rules 1–4, divided by 2 (why it divides exactly in half is explained in
section 2.3).

Note on numbering: `DEFINITION.md` and the other project files number the rules
differently: their rule 1 is our rule 1, their rule 2 is our rule 3 (no
horizontals), their rule 3 is our rule 4 (at most two consecutive on one side),
and our rule 2 (each eyelet exactly once) is stated in their preamble.

### 1.3. Why exactly this reading

The text in OEIS allows different readings of rule 4. We checked three:

* “three consecutive on one side”: any three (the rule above);
* “three consecutive on one side, with the middle one lying between the outer
  two” (the lace runs in a straight line);
* “three adjacent eyelets of one edge in succession” (as in the related
  A078602).

For `n = 3` all three readings give the same 6 lacings as in the OEIS example.
But for `n = 4` and `n = 5` they give 45 and 1824, 76 and 3738, and 89 and 5554,
respectively. OEIS has 45 and 1824, so the first reading is the correct one. It
is also the reading implemented by the Java program of Sean A. Irvine, who found
a(9). As a check: the third reading, with the ban on horizontals lifted, gives
exactly the terms of A078602 (21, 601, 34278). So the model itself (the
numbering, “lacing = visiting order”) is set up correctly. An even stronger
argument was found by the reviewer: **our** reading, with the ban on
horizontals lifted, gives exactly A078698 (20, 396, 14976, 907200, …). This is a
sequence by the same author, Pfoertner: “every eyelet has a direct connection
to the opposite side”. For the inner eyelets this is the same as our rule 4.
Details are in `DECISIONS.md`.

---

## 2. Example: n = 3

### 2.1. Enumerating by hand

A lacing has the form `1 _ _ _ _ 6`, where the middle holds the eyelets 2, 3,
4, 5 in some order. There are `4! = 24` such orders in total.

**Rule 3 (no horizontals)** forbids 2 and 5 from being adjacent, and likewise 3
and 4. The transition 1↔6 is impossible anyway: 1 comes first and 6 comes last.
That leaves 8 orders. In them there is exactly one eyelet between 2 and 5, and
likewise between 3 and 4:

```
1 2 3 5 4 6     1 2 4 5 3 6     1 5 3 2 4 6     1 5 4 2 3 6
1 3 2 4 5 6     1 3 5 4 2 6     1 4 2 3 5 6     1 4 5 3 2 6
```

**Rule 4 (at most two consecutive on one side).** Eyelets 1, 2, 3 are on the
left, 4, 5, 6 on the right. The order `1 2 3 5 4 6` begins with three left ones
(1, 2, 3). The order `1 3 2 4 5 6` ends with three right ones (4, 5, 6). We
cross out both. Exactly the six lacings from the OEIS example remain:

```
124536, 135426, 142356, 145326, 153246, 154236
```

### 2.2. Mirror pairs

Reflection swaps the sides: eyelet `e` goes to `7 − e` (1↔6, 2↔5, 3↔4). To
start from 1 again, we read the reflected lacing backwards. For example,
`124536` → (6,5,3,2,4,1) → read backwards `142356`. The six lacings split into
three pairs:

* `124536` ↔ `142356`
* `135426` ↔ `153246`
* `145326` ↔ `154236`

Therefore **a(3) = 3**.

### 2.3. Why everything always divides in half

The reflection of a lacing is again a lacing: the rules do not distinguish
between the left and right sides. But can a lacing coincide with its own
reflection? Then the reflection would map the middle of the lacing to itself.
The two middle eyelets `pn` and `pn+1` would swap places, that is, they would be
mirror images of each other: two eyelets of the same row, connected directly.
That is a horizontal, and it is forbidden. Hence there are no symmetric
lacings, all lacings split into pairs, and the division by 2 is exact. All
programs additionally check that the count before division is even.

---

## 3. Why we cannot simply enumerate everything for n = 10

There are `(2n−2)!` orders of the eyelets between the first and the last. For
`n = 10` this is `18! ≈ 6.4·10^15`. Even if bad variants are discarded
immediately, the valid lacings alone number about `7.3·10^13` for `n = 10`
(twice the answer). At a billion lacings per second that is almost a full day
for a single number, and the next number is about 250 times larger. This is
exactly how Irvine obtained a(9) in 2024: that is `3.6·10^11` lacings. By
brute-force enumeration (the program `brute/brute_dfs.c`) we repeated
`n = 3…8`. For `n = 8` that is 2.3 billion lacings in about 59 seconds on 4 cores.
Beyond that, a smarter method is needed.

---

## 4. The key observation: rows are interchangeable

Each eyelet can be described by two attributes: its **side** (left/right) and
its **row** (1…n). Let us see which attributes the rules use.

* Rule 4 looks only at sides.
* Rule 3 forbids two eyelets of the same row from being adjacent. All that
  matters to it is *whether* the neighbours' rows are *the same*, not which
  rows they are.
* Row 1 is special: the lacing starts and ends in it.

So if in a finished lacing we **relabel rows 2…n** (for example, swap rows 2
and 3 everywhere, on both sides at once), we again get a valid lacing. There
are `(n−1)!` relabelings, and different relabelings give different lacings.
Therefore all lacings split into groups of exactly `(n−1)!` each. Consequence
(proved): **2·a(n) is divisible by (n−1)!**. The quotient is the number of
lacings in which the inner rows first appear in the order 2, 3, …, n. For
`n = 3…11` these are 3, 15, 152, 1826, 26446, 454388, 8982734,
200843362, 5015991284. For `n ≤ 6` this was checked by brute-force enumeration
(`brute/canonical_check.py`). The reviewer, with a separate program,
enumerated such “canonical” lacings up to `n = 11`. So a(10) and a(11) were
also obtained by direct brute-force enumeration (`review/canon_enum.c`).

Both fast methods rely on this interchangeability, but use it in completely
different ways.

---

## 5. Method 1: “row bookkeeping” (folder `method_dp/`)

### 5.1. The idea

We build the lacing step by step, eyelet by eyelet. To continue, we do not
need to remember *which exactly* eyelets are already used. It is enough to know
the following:

* `u`: how many inner rows are still **untouched** (both eyelets free);
* `l`: in how many rows **only the left** eyelet is used;
* `r`: in how many rows **only the right** eyelet is used;
* which **side** we are on now and how many **consecutive** eyelets we have
  visited on it (1 or 2);
* whether the **pair** of the current eyelet, that is, the other eyelet of the
  same row, is free. That is exactly where we cannot go now: it would be a
  horizontal.

It is like a cashier who, to give change, needs to know how many banknotes of
each denomination they have, not their serial numbers. Why this is enough: two
partial lacings with the same “bookkeeping” data may differ (even in their
left/right pattern), but what remains to be done is the same for both up to a
relabeling of rows: a suitable relabeling of rows 2…n (section 4) turns every
completion of one into a completion of the other, and back. Hence they have
equally many ways to be completed. This is proved in `method_dp/METHOD.md`
(section 4, the lumping lemma).

### 5.2. A step

From the current eyelet we can go:

* to an **untouched row**, on either side: `u` ways. After this, the new
  eyelet's pair is free;
* to a **half-used row**, to take its second eyelet. On the left side, the
  suitable rows are those where only the right eyelet is used (`r` of them); on
  the right side, those where only the left one is used (`l` of them). If the
  pair of the current eyelet is still free and we move to the other side, one
  of these options is exactly the horizontal: we subtract it;
* **to the same side**: only if so far we have visited one consecutive eyelet
  on it, not two (rule 4).

The number of ways is multiplied by these counts. Eyelet `2n` (top right) is
placed last. This is allowed if the two previous eyelets are not both on the
right.

### 5.3. Example n = 3 step by step

We write a state as `(u, l, r, side, consecutive, pair free?)`. At the start we
are at eyelet 1: `(2, 0, 0, L, 1, no)`, one way.

| after | states and the number of ways to reach them |
|---|---|
| p2 | `(1,1,0, L,2, yes)`: 2 [p2 = 2 or 3] · `(1,0,1, R,1, yes)`: 2 [p2 = 4 or 5] |
| p3 | `(0,1,1, R,1, yes)`: 2 · `(0,1,1, L,1, yes)`: 2 · `(0,0,2, R,2, yes)`: 2 |
| p4 | `(0,0,1, R,2, no)`: 2 · `(0,1,0, L,2, no)`: 2 · `(0,0,1, L,1, no)`: 2 |
| p5 | `(0,0,0, L,1, no)`: 2 · `(0,0,0, R,1, no)`: 2 · `(0,0,0, L,2, no)`: 2 |

An example of one transition. From `(1,1,0, L,2, yes)` (we are on the left, and
this is already the second consecutive left eyelet) we cannot go left. We can go
right, into the only untouched row. There is also exactly one row with “only
the left used”, but it is the row of the current eyelet: going into it would be
a horizontal. In total `1·2 = 2` ways, state `(0,1,1, R,1, yes)`.

At the end, all three states allow the last step to eyelet 6 (none of them has
“two consecutive rights”). In total `2 + 2 + 2 = 6` lacings, `a(3) = 6/2 = 3`.
This matches the enumeration by hand.

### 5.4. What it costs

There are on the order of `n³` states, not `(2n)!`. For `n = 10` the
computation takes thousandths of a second. The Python program computes all `n`
up to 400 in 4 minutes, with exact integers and no rounding.

### 5.5. How this is written in the program of the OEIS draft

The program `oeis/a072503_oeis.py` (the same code is in the draft's `%o`
lines) is exactly method 1. Its state is the tuple `(u, l, r, s, k, f)`: `s` is
the side (0 = left, 1 = right), `k` is how many consecutive eyelets are on that
side, and `f = 1` if the partner of the current eyelet is free. Line by line:

| program line | what it does |
|---|---|
| `cur = {(n-1, 0, 0, 0, 1, 0): 1}` | start at eyelet 1: all `n−1` inner rows are untouched, the side is left, one consecutive eyelet. The partner of eyelet 1 is `2n`, which is placed last anyway, so `f = 0`. One way |
| `for _ in range(2*n-2):` | place the `2n−2` inner eyelets one after another |
| `for t in (0, 1):` | choose the side of the next eyelet |
| `if t == s and k == 2: continue` | rule 4: a third consecutive eyelet on the same side is not allowed |
| `kk = k+1 if t == s else 1` | the new run length on that side |
| `if u:` … `nxt[key] = nxt.get(key, 0) + u*v` | go to an untouched row: `u` ways. The row becomes "only left used" (or "only right used"), and the partner of the new eyelet is free (`f = 1`) |
| `m = (r if t == 0 else l) - (f if t != s else 0)` | how many half-used rows can be "closed" on side `t`. If we switch sides while the partner of the current eyelet is free, one of these options is a horizontal, so it is subtracted (rule 3) |
| `if m > 0:` … `nxt[key] = nxt.get(key, 0) + m*v` | close a half-used row: `m` ways; the partner of the new eyelet is already used (`f = 0`) |
| `return sum(` … `if not (s == 1 and k == 2))//2` | the last step to eyelet `2n` (a right eyelet): not allowed if the two previous eyelets are also on the right. Divide by 2 because of mirror pairs |

Limits of the program: it is exact (Python integers are never rounded), but it
has about `n³` states and recomputes them for every `n`. One value a(n) takes
0.14 s for `n = 50`, 1.7 s for `n = 100` and 16 s for `n = 200`. The b-file was
computed with the faster programs of methods 1 and 2.

---

## 6. Method 2: “side pattern + inclusion–exclusion” (folder `method_ie/`)

### 6.1. Sides first, then rows

Let us write down which side each eyelet of the lacing lies on: we get a word
of length `2n` in the letters L and R. For example, `124536` → `LLRRLR`. Rule 4
says precisely that the word has no three consecutive equal letters. In
addition, the word starts with L, ends with R, and contains `n` letters of each
kind. For `n = 3` there are five such words:

```
LLRRLR   LRLLRR   LRRLLR   LLRLRR   LRLRLR
```

Once the word is chosen, it remains to decide *which row* goes in each
position. The left positions get the rows 1…n (the first position must be
row 1), and so do the right positions (the last one must be row 1). That is
`(n−1)!·(n−1)!` options. Rule 4 already holds for them. What remains is rule 3:
at every **change of side** (L next to R), the neighbours' rows must be
different.

### 6.2. Inclusion–exclusion on an example

Take the word `LLRRLR` for `n = 3`. Positions 1–6: L L R R L R. Positions 1
and 6 hold the eyelets of row 1 (1 and 6). The remaining left positions 2 and 5
get the rows {2, 3} in some order, and the right positions 3 and 4 also get
{2, 3}. In total `2·2 = 4` options. There are two changes of side where a
horizontal can occur: between positions 2|3 and 4|5. The change 5|6 is safe:
position 6 holds row 1, and that row is already taken by position 1.

The inclusion–exclusion method works like this: from all options we subtract
the bad ones, but options that are bad in two places at once have then been
subtracted twice, so we add them back.

* Total: 4.
* Horizontal at 2|3 (equal rows in positions 2 and 3): 2 options.
* Horizontal at 4|5: 2 options.
* Horizontals at both 2|3 and 4|5: 2 options.

Good ones: `4 − 2 − 2 + 2 = 2`. These are the lacings `124536` and `135426`,
as in the enumeration.

### 6.3. The general rule

Suppose we require a horizontal at `k` chosen changes of side. How many options
allow this?

* If two chosen changes touch **the same position** (for example, R|L|R with a
  single L in the middle), we get 0. The single L would have to have the same
  row as both neighbouring Rs, and two right eyelets of the same row do not
  exist.
* If a chosen change touches **the first or the last position**, we also get 0:
  row 1 is already taken by the start and the end.
* Otherwise, the chosen changes split `k` left positions and `k` right
  positions into pairs of “the same row”. We arrange the left rows arbitrarily:
  `(n−1)!` ways. This also determines the rows in the `k` right positions. The
  remaining `n−1−k` right positions are filled arbitrarily: `(n−1−k)!` ways.

This gives the formula (it is derived, not guessed; the proof is in
`method_ie/METHOD.md`):

```
2·a(n) = (n−1)! · Σ_k (−1)^k · (n−1−k)! · N(n,k)
```

Here `N(n,k)` is the number of pairs “admissible word + `k` chosen changes of
side, no two of which touch the same position and none of which touches the
first or the last position”. There are very many words, but there is no need to
enumerate them. A word is an alternation of “blocks” L or LL and R or RR, and
`N(n,k)` is computed by a small dynamic program over these blocks. For `n = 3`
the words give 2, 2, 2, 0 and 0 lacings, 6 in total — again in agreement with
the enumeration.

The same implementer also derived from this an explicit finite sum of binomial
coefficients (the formula is in `method_ie/METHOD.md`, checked up to `n = 16`).

---

## 7. A third, “direct” method: dynamic programming over subsets (`brute/subset_dp.c`)

This method makes no assumptions about symmetry at all. It remembers **which
exactly** eyelets are already used, where we are now, and whether the previous
eyelet was on the same side. It is a direct restatement of the rules: from each
such “snapshot” we can step to any free eyelet if the rules allow it. There are
`2^(2n−2)·(2n−2)·2` possible snapshots. For `n = 13` that is 800 million, about
6 GB of memory and about 24 s + 15 s (one run for each of two moduli, see
section 8). Beyond that, memory runs out. This method
confirmed `n = 3…13`, including a(10), a(11), a(12), a(13).

---

## 8. How the verification is organized

1. **Definition.** Three readings of the rules were checked by enumerating all
   orders. The only one that gives the known a(4) and a(5) was chosen. Then
   enumerating the lacings one by one confirmed a(3)…a(8).
2. **Independence.** Methods 1 and 2 were written by two different implementers
   (separate AI agents). Each was given only the text of the definition
   (`DEFINITION.md`) and the known terms. They were forbidden to read each
   other's folder, the brute-force enumerations and our intermediate numbers,
   and they did not know the new numbers in advance. The methods are
   fundamentally different: one goes through the lacing step by step, the other
   first chooses the sides and then counts the exclusions.
3. **Mandatory test.** Each method had to reproduce, on its own, all seven
   known terms a(3)…a(9). Each implementer also checked against their own
   brute-force enumeration.
4. **Comparison.** `compare.py` (run as `python3 compare.py` from `a072503/`)
   recomputes nothing. It compares the saved results of methods 1 and 2 with
   each other, with the logs of the “direct” method and with the b-file
   `oeis/b072503.txt`, and rewrites `accepted_terms.txt` with identical
   content. Methods 1 and 2 agreed for all `n = 3…400`, and the “direct” method
   for `n = 3…13`. A new term is accepted only if two independent methods
   agree.
5. **Exact arithmetic.** There is no rounding anywhere: Python integers (of any
   length) or 128-bit integers in C. For `n = 13` the C computation is done
   with two moduli and combined by the Chinese remainder theorem, with a
   check at `n = 12`.
6. **The reviewer.** A separate reviewer agent tried to find an error in the
   reading, in the code and in the results, and found none. Here is what it
   did:
   * recomputed everything from scratch;
   * checked eight other readings of the rules: none of them fits (two more
     variants turned out to be equivalent to ours);
   * obtained a(3..11) with its own enumeration of canonical lacings;
   * wrote a third fast method, which agreed up to `n = 500`;
   * checked the key lemma of method 1 on 882 thousand real partial lacings.

   Its report is `review/REVIEW.md`.

---

## 9. What is proved and what is only checked

“Proved” below means that a written proof exists in the section or file cited.
The proofs were written by AI agents and checked by the reviewer agent, not yet
by an independent human expert.

| statement | status |
|---|---|
| Lacings split into mirror pairs, there are no symmetric ones, the division by 2 is exact | proved (section 2.3) |
| 2·a(n) is divisible by (n−1)!, the quotient = the number of lacings with the rows in order of first appearance | proved (section 4), checked by enumeration up to n = 11 |
| The formula of method 2 (inclusion–exclusion) | proved (section 6, in detail in `method_ie/METHOD.md`) |
| Exactness of method 1 (“lumping” of states) | proved (`method_dp/METHOD.md`, lemma) |
| Values a(10)…a(400) | computed by two independent methods, both with written proofs; 100% agreement |
| Reading of the rules | not “provable”: it is a choice of how to read the OEIS text. Justification: it is the only reading that reproduces all known terms, and it coincides with Irvine's program |
| Linear recurrence of order 18 with polynomial coefficients of degree 18 for 2·a(n)/(n−1)! | **conjecture only**: found by fitting modulo primes, fitted on n ≤ 420 and holds for all further terms up to n = 500. The coefficients have not been written out; there is no proof (`recurrence/README.md`) |

---

## 10. If an OEIS editor asks “how did you compute this?”

> Rows 2…n are interchangeable: the rules look only at the side of an eyelet
> and at whether neighbouring eyelets are in the same row. Therefore, when
> building a lacing step by step, it is enough to remember how many rows are
> untouched, how many have only the left eyelet used and how many have only the
> right eyelet used. One also needs the side of the current eyelet, how many
> consecutive eyelets have been visited on that side, and whether its pair is
> free. This is a dynamic program with ~n³ states. Independently of it: a sum
> over words in L/R with no three consecutive equal letters, where horizontals
> at changes of side are handled by inclusion–exclusion, gives
> `2a(n) = (n−1)! Σ_k (−1)^k (n−1−k)! N(n,k)`. Both methods give the same
> numbers for n ≤ 400 and the known a(3..9). A direct dynamic program over
> subsets of eyelets confirms n ≤ 13, and full brute-force enumeration confirms
> n ≤ 8.

---

## Glossary

* **Lacing**: the order in which the lace passes through the eyelets.
* **Horizontal**: a direct transition between the two eyelets of one row.
* **Mirror image**: the same lacing with the left and right sides swapped.
* **Brute-force enumeration**: checking all options one by one.
* **Dynamic programming (DP)**: counting step by step, where at each step one
  remembers not the options themselves but only how many of them there are in
  each “state”.
* **Inclusion–exclusion**: a way to count the good options: subtract the bad
  ones from all of them, add back those subtracted twice, and so on.
* **Modulo a prime**: a computation in which only the remainders after
  division by a large prime number are kept. This is fast and convenient for
  finding patterns, but it does not give the numbers themselves.
