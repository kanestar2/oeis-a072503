def a(n):
    # Build the lacing eyelet by eyelet.  Rows 2..n are interchangeable, so
    # only counts matter. State (u, l, r, s, k, f): u, l, r = number of inner
    # rows with no eyelet / only the left one / only the right one used so far,
    # s = side of the current eyelet (0 = left, 1 = right), k = 1 or 2 eyelets
    # in a row on that side, f = 1 if the other eyelet of the current row is unused.
    cur = {(n-1, 0, 0, 0, 1, 0): 1}           # start at eyelet 1 (left, top)
    for _ in range(2*n-2):
        nxt = {}
        for (u, l, r, s, k, f), v in cur.items():
            for t in (0, 1):                  # side of the next eyelet
                if t == s and k == 2: continue    # no three on one side
                kk = k+1 if t == s else 1
                if u:                         # eyelet of an untouched row
                    key = (u-1, l+1, r, t, kk, 1) if t == 0 else (u-1, l, r+1, t, kk, 1)
                    nxt[key] = nxt.get(key, 0) + u*v
                m = (r if t == 0 else l) - (f if t != s else 0)  # no horizontal
                if m > 0:                     # second eyelet of a half-used row
                    key = (u, l, r-1, t, kk, 0) if t == 0 else (u, l-1, r, t, kk, 0)
                    nxt[key] = nxt.get(key, 0) + m*v
        cur = nxt
    # finish at eyelet 2n (right, top); halve for mirror images
    return sum(v for (u, l, r, s, k, f), v in cur.items() if not (s == 1 and k == 2))//2
print([a(n) for n in range(3, 18)])
