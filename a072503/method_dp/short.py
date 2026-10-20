# A072503 via profile DP (see METHOD.md). Exact Python ints. Prints a(3..15).
# State (a,b,c,s,r,f): a/b/c = # inner rows with no / only-left / only-right
# eyelet used, s = side of last eyelet (0=L,1=R), r = run length (1,2) of that
# side, f = 1 iff the last eyelet's partner (same row) is still unused.
from collections import defaultdict


def D(n):
    cur = {(n - 1, 0, 0, 0, 1, 0): 1}            # p_1 = eyelet 1 (left, top row)
    for _ in range(2 * (n - 1)):                 # place the 2n-2 inner eyelets
        nxt = defaultdict(int)
        for (a, b, c, s, r, f), v in cur.items():
            for t in (0, 1):                     # side of the next eyelet
                if t == s and r == 2:            # rule 3
                    continue
                q = r + 1 if t == s else 1
                if a:                            # fresh row, a choices; partner free
                    key = (a - 1, b + 1, c) if t == 0 else (a - 1, b, c + 1)
                    nxt[key + (t, q, 1)] += a * v
                k = (c if t == 0 else b) - (f if t != s else 0)   # rule 2
                if k > 0:                        # complete a half-used row
                    key = (a, b, c - 1) if t == 0 else (a, b - 1, c)
                    nxt[key + (t, q, 0)] += k * v
        cur = nxt
    # p_2n = eyelet 2n (right, top row): forbidden only after two right eyelets
    return sum(v for (a, b, c, s, r, f), v in cur.items() if not (s == 1 and r == 2))


for n in range(3, 16):
    d = D(n)
    assert d % 2 == 0
    print(n, d // 2)
