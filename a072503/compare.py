#!/usr/bin/env python3
"""Compare the two independent methods (method_dp, method_ie) with each other,
with the known OEIS terms and with the direct subset DP (brute/subset_dp.c).
Writes the accepted terms (n where BOTH methods agree) to accepted_terms.txt
in the OEIS b-file format "n a(n)".

Usage: python3 compare.py
"""
import re, sys

def load(path):
    d = {}
    for line in open(path):
        n, D, a = map(int, line.split())
        assert D == 2 * a, f"{path}: D != 2a at n={n}"
        assert n not in d, f"{path}: duplicate n={n}"
        d[n] = a
    return d

dp, ie = load("method_dp/results.txt"), load("method_ie/results.txt")
known = {3: 3, 4: 45, 5: 1824, 6: 109560, 7: 9520560, 8: 1145057760, 9: 181091917440}
sub = {}
for line in open("logs/subset_dp_exact_n3-12.log"):
    m = re.search(r"n=(\d+) mode=0 D=(\d+) a=(\d+)", line); sub[int(m[1])] = int(m[3])
for line in open("logs/subset_dp_crt_n12-13.log"):
    m = re.search(r"n=(\d+) CRT: D=\d+ a=(\d+)", line)
    if m: sub[int(m[1])] = int(m[2])

ok = True
for name, d in (("method_dp", dp), ("method_ie", ie), ("subset_dp", sub)):
    for n, v in known.items():
        if d.get(n) != v:
            print(f"FAIL: {name} a({n}) = {d.get(n)} != known {v}"); ok = False
    print(f"{name}: n = {min(d)}..{max(d)} ({len(d)} values), reproduces a(3..9): "
          f"{all(d.get(n) == v for n, v in known.items())}")
common = sorted(set(dp) & set(ie))
assert common == list(range(3, max(common) + 1)), "gap in common range"
mism = [n for n in common if dp[n] != ie[n]]
print(f"method_dp vs method_ie: common n = 3..{common[-1]}, mismatches: {mism}")
smism = [n for n in sub if not (sub[n] == dp[n] == ie[n])]
print(f"subset_dp vs both methods, n = {min(sub)}..{max(sub)}: mismatches: {smism}")
if mism or smism or not ok:
    sys.exit(1)
with open("accepted_terms.txt", "w") as f:
    for n in common:
        f.write(f"{n} {dp[n]}\n")
print(f"accepted_terms.txt written: n = 3..{common[-1]}")
