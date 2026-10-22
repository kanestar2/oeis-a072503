#!/usr/bin/env python3
"""Compare the saved results of the two independent methods (method_dp,
method_ie) with each other, with the known OEIS terms, with the direct subset
DP (brute/subset_dp.c, values taken from logs/subset_dp_*.log) and with the
b-file oeis/b072503.txt.  Nothing is recomputed: only saved files are read.
If all checks pass, writes the accepted terms (n where BOTH methods agree) to
accepted_terms.txt in the OEIS b-file format "n a(n)" and reports whether its
content changed.  Exits with status 1 if any check fails.

Usage (from the a072503/ folder): python3 compare.py
"""
import os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))   # paths below are relative to a072503/

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

# subset DP values from the logs; lines that are not result lines (e.g. stderr) are skipped
sub = {}
for path, pat in (("logs/subset_dp_exact_n3-12.log", r"n=(\d+) mode=0 D=(\d+) a=(\d+)"),
                  ("logs/subset_dp_crt_n12-13.log", r"n=(\d+) CRT: D=(\d+) a=(\d+)")):
    for line in open(path):
        m = re.search(pat, line)
        if m:
            n, D, a = map(int, m.groups())
            assert D == 2 * a, f"{path}: D != 2a at n={n}"
            assert sub.get(n, a) == a, f"{path}: n={n} differs from the other log"
            sub[n] = a
assert sorted(sub) == list(range(3, 14)), f"subset_dp logs cover n = {sorted(sub)}, expected 3..13"

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
acc = [f"{n} {dp[n]}\n" for n in common]

# b-file: must be exactly the accepted terms from n = 3 on, as long as a line has <= 1000 chars
k = 0
while k < len(acc) and len(acc[k]) - 1 <= 1000:
    k += 1
assert k < len(acc), "accepted terms end before a line exceeds 1000 chars"
bf = open("oeis/b072503.txt", newline="").read()      # byte-exact: no newline translation
if bf != "".join(acc[:k]):
    print(f"FAIL: oeis/b072503.txt differs from the accepted terms n = 3..{common[k - 1]}")
    sys.exit(1)
print(f"oeis/b072503.txt: n = 3..{common[k - 1]} ({k} lines), equal to the accepted terms, "
      f"longest line {max(len(s) - 1 for s in acc[:k])} chars "
      f"(the line for n = {common[k]} would have {len(acc[k]) - 1})")

new = "".join(acc)
old = open("accepted_terms.txt", newline="").read() if os.path.exists("accepted_terms.txt") else None
with open("accepted_terms.txt", "w") as f:
    f.write(new)
print(f"accepted_terms.txt written: n = 3..{common[-1]}, "
      + ("content unchanged" if old == new else
         "NEW FILE" if old is None else
         f"CONTENT CHANGED (previous file had {len(old.splitlines())} lines)"))
