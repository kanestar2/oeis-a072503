#!/usr/bin/env python3
"""Per-side-word inclusion-exclusion, done naively (small n only).

For a side word w (w_1 = L, w_{2n} = R, n letters of each kind, no three equal
consecutive letters) the number of lacings with that side pattern is

    D_w = (n-1)! * sum_k (-1)^k (n-1-k)! m_k(w)

where m_k(w) is the number of k-sets of *interior* switch places (places i with
w_i != w_{i+1}, not touching position 1 or 2n) no two of which share a position.
Here m_k(w) is obtained by literally enumerating all subsets of the switch
places and applying the general inclusion-exclusion count of each subset
(computed by a separate tiny brute-force-free rule, see count_forced below),
so that the "matching" simplification itself is tested too.

usage:
  python3 ie_per_word.py compare BRUTE_FILE   # compare with brute_perm.py output
  python3 ie_per_word.py nk N_MAX             # print N_n(k) = sum_w m_k(w)
"""
import sys
from itertools import combinations
from math import factorial


def words(n):
    """All admissible side words, generated letter by letter."""
    out = []

    def rec(w, nl, nr):
        if nl == n and nr == n:
            if w[-1] == 'R':
                out.append(''.join(w))
            return
        for c in 'LR':
            if (c == 'L' and nl == n) or (c == 'R' and nr == n):
                continue
            if len(w) >= 2 and w[-1] == c and w[-2] == c:
                continue
            w.append(c)
            rec(w, nl + (c == 'L'), nr + (c == 'R'))
            w.pop()

    rec(['L'], 1, 0)
    return out


def count_forced(w, S, n):
    """Number of pairs of bijections (sigma: L-positions -> rows, tau:
    R-positions -> rows) with sigma(pos 1) = 1, tau(pos 2n) = 1 and
    row(p_i) = row(p_{i+1}) for every switch place i in S.
    Computed from first principles via union-find on positions."""
    m = 2 * n
    parent = list(range(m))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in S:                       # place i joins positions i and i+1 (0-based)
        parent[find(i)] = find(i + 1)
    comps = {}
    for p in range(m):
        comps.setdefault(find(p), []).append(p)
    # each component must get ONE row; it may contain at most one L and one R
    fixed_rows = set()
    nfree_L = nfree_R = 0
    free_pairs = 0
    for c in comps.values():
        nl = sum(1 for p in c if w[p] == 'L')
        nr = len(c) - nl
        if nl > 1 or nr > 1:
            return 0
        has_top = (0 in c) or (m - 1 in c)
        if has_top:
            # the component containing position 1 (or 2n) must have row 1
            if 0 in c and m - 1 in c:
                return 0                          # impossible: different comps unless n=1
            if (0 in c and nr == 1) or (m - 1 in c and nl == 1):
                return 0                          # partner would need row 1 too, but row 1 is used
            continue
        if nl == 1 and nr == 1:
            free_pairs += 1
        elif nl == 1:
            nfree_L += 1
        else:
            nfree_R += 1
    # rows 2..n: pairs take a row on both sides; remaining L-singletons and
    # R-singletons fill the rest.
    k = free_pairs
    if nfree_L != n - 1 - k or nfree_R != n - 1 - k:
        raise AssertionError("bookkeeping")
    # choose an injective row map for pairs and the L-singletons: (n-1)!,
    # then R-singletons get the rows not used by pairs: (n-1-k)!
    return factorial(n - 1) * factorial(n - 1 - k)


def Dw_naive(w, n):
    m = 2 * n
    sw = [i for i in range(m - 1) if w[i] != w[i + 1]]
    tot = 0
    for k in range(len(sw) + 1):
        for S in combinations(sw, k):
            tot += (-1) ** k * count_forced(w, S, n)
    return tot


def mk(w, n):
    """m_k(w): k-matchings among interior switch places."""
    m = 2 * n
    sw = [i for i in range(m - 1) if w[i] != w[i + 1] and i != 0 and i + 1 != m - 1]
    res = [0] * n
    for k in range(len(sw) + 1):
        for S in combinations(sw, k):
            if all(S[j + 1] - S[j] >= 2 for j in range(len(S) - 1)):
                res[k] += 1
    return res


def Dw_formula(w, n):
    return factorial(n - 1) * sum((-1) ** k * factorial(n - 1 - k) * c
                                  for k, c in enumerate(mk(w, n)))


if __name__ == '__main__':
    if sys.argv[1] == 'compare':
        brute = {}
        cur = None
        for line in open(sys.argv[2]):
            if line.startswith('n='):
                cur = int(line.split()[0][2:])
                brute[cur] = {}
            elif line.startswith('  '):
                w, c = line.split()
                brute[cur][w] = int(c)
        allok = True
        for n in sorted(brute):
            ws = words(n)
            ok = True
            tot = 0
            for w in ws:
                a = Dw_naive(w, n)
                b = Dw_formula(w, n)
                c = brute[n].get(w, 0)
                tot += b
                if not (a == b == c):
                    ok = False
                    print("MISMATCH", n, w, a, b, c)
            extra = set(brute[n]) - set(ws)
            if extra:
                ok = False
                print("brute has words not generated:", extra)
            print(f"n={n}: {len(ws)} words, per-word naive-IE == matching-IE == brute: {ok}, D={tot}")
            allok &= ok
        print("ALL OK" if allok else "FAILED")
    elif sys.argv[1] == 'nk':
        for n in range(2, int(sys.argv[2]) + 1):
            tot = [0] * n
            for w in words(n):
                for k, c in enumerate(mk(w, n)):
                    tot[k] += c
            print(n, ' '.join(map(str, tot)))
