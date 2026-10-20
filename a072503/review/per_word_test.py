#!/usr/bin/env python3
"""Per-side-word test of method_ie's formula D_w = (n-1)! sum_k (-1)^k (n-1-k)! m_k(w)
against the reviewer's literal canonical enumeration (canon_enum, per-word counts
times (n-1)!).  Uses a COPY of method_ie/ie_per_word.py (review/tmp/ie_copy).

Usage: python3 -B per_word_test.py NMIN NMAX
"""
import os
import subprocess
import sys
from math import factorial

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tmp", "ie_copy"))
import ie_per_word  # noqa: E402  (copy of the project file)

lo, hi = int(sys.argv[1]), int(sys.argv[2])
allok = True
for n in range(lo, hi + 1):
    out = subprocess.run([os.path.join(HERE, "tmp", "bin", "canon_enum"), str(n), "words"],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    head, rows = out[0], out[1:]
    enum = {w: int(c) * factorial(n - 1) for w, c in (r.split() for r in rows)}
    words = ie_per_word.words(n)
    bad = 0
    for w in words:
        f = ie_per_word.Dw_formula(w, n)
        if f != enum.get(w, 0):
            bad += 1
            if bad <= 5:
                print("MISMATCH", n, w, f, enum.get(w, 0))
    extra = set(enum) - set(words)
    nz = sum(1 for w in words if enum.get(w, 0))
    ok = bad == 0 and not extra
    allok &= ok
    print(f"n={n}: {len(words)} admissible words ({nz} with lacings), "
          f"enumerated words not admissible: {len(extra)}, mismatches: {bad}, "
          f"sum = {sum(enum.values())}  [{head}]", flush=True)
print("ALL OK" if allok else "FAILED")
