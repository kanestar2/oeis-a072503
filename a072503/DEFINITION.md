# A072503 — formal definition used in this project

Eyelets are numbered as in Pfoertner's original program:

* left side: eyelets `1, 2, ..., n` from top to bottom;
* right side: eyelets `n+1, ..., 2n` from bottom to top;
* the horizontal pairs ("rows") are `(k, 2n+1-k)`, `k = 1..n`; `(1, 2n)` is the top pair.

A **lacing** is an ordering `p_1, p_2, ..., p_{2n}` of all 2n eyelets
(every eyelet is used exactly once) such that

1. `p_1 = 1` and `p_{2n} = 2n` (the lace starts and ends at the top pair);
2. no two consecutive eyelets form a horizontal pair: `p_i + p_{i+1} != 2n+1`
   for every `i` (for the top pair this is automatic when n >= 2);
3. no three consecutive eyelets of the lacing lie on the same side: for every
   `i`, the eyelets `p_i, p_{i+1}, p_{i+2}` are not all `<= n` and not all `> n`.

Any other direct connection is allowed (e.g. 1 -> 3 along the same side,
skipping eyelet 2, or any diagonal).

Let `D(n)` be the number of such orderings.  Over/under crossings are not
distinguished (a lacing is just the order of eyelets).  The left-right mirror
image of a lacing (replace every eyelet `e` by `2n+1-e` and read the result
backwards) is again a lacing; it is never equal to the original (see below), so
lacings come in mirror pairs and

    A072503(n) = D(n) / 2.

Why a lacing never equals its mirror image: if `p_{2n+1-i} = 2n+1-p_i` for all
`i`, then for `i = n` we get `p_{n+1} = 2n+1-p_n`, i.e. the two middle eyelets
form a horizontal pair, which rule 2 forbids.

Known values (OEIS, n = 3..9): 3, 45, 1824, 109560, 9520560, 1145057760, 181091917440.
Example n = 3: the 6 orderings are 124536, 135426, 142356, 145326, 153246, 154236, so a(3) = 3.
