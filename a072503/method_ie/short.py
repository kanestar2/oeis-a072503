#!/usr/bin/env python3
# A072503(n), n=3..15, by side words + inclusion-exclusion (exact integers).
# D(n) = (n-1)! * sum_k (-1)^k (n-1-k)! N(k),  a(n) = D(n)/2,  where N(k) counts
# pairs (side word, k pairwise disjoint switch places not touching positions 1, 2n).
# Words = alternating runs L^al R^be (al, be in {1,2}); DP over such blocks.
from math import factorial as f


def a(n):
    F = {(0, 0, 1): {0: 1}}   # (#L, #R, place after last block selected?) -> {k: count}
    N = {}
    for tot in range(2 * n + 1):
        for (i, h, s), P in [kv for kv in F.items() if kv[0][0] + kv[0][1] == tot]:
            for al in (1, 2):
                for be in (1, 2):
                    I, H = i + al, h + be
                    if I > n or H > n:
                        continue
                    for x in (0, 1):                  # inner L->R place selected?
                        if x and al == 1 and s:       # a lone L between two chosen places
                            continue
                        for s2 in (0, 1, 2):          # next R->L place: 0/1; 2 = end (virtual)
                            if x and be == 1 and s2:  # a lone R between two chosen places
                                continue
                            if (s2 == 2) != ((I, H) == (n, n)):
                                continue
                            tgt = N if s2 == 2 else F.setdefault((I, H, s2), {})
                            d = x + (s2 == 1)
                            for k, c in P.items():
                                tgt[k + d] = tgt.get(k + d, 0) + c
    D = f(n - 1) * sum((-1) ** k * f(n - 1 - k) * c for k, c in N.items())
    assert D % 2 == 0
    return D // 2


print(*[a(n) for n in range(3, 16)])
