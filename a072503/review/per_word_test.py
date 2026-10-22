#!/usr/bin/env python3
"""Per-side-word test of method_ie's formula D_w = (n-1)! sum_k (-1)^k (n-1-k)! m_k(w)
against the reviewer's literal canonical enumeration (canon_enum, per-word counts
times (n-1)!).  Imports ../method_ie/ie_per_word.py (no file of method_ie is written).

Usage (from a072503/review/): python3 -B per_word_test.py NMIN NMAX [CANON_ENUM]

CANON_ENUM is the path of a binary built from review/canon_enum.c.  Without it,
review/tmp/bin/canon_enum is used; if that file does not exist, it is first built
there with "gcc -O2 -fopenmp" (review/tmp/ is git-ignored).
"per_word_test.py 3 9" takes a few seconds.

Editor's note (2026-10-22): the reviewer ran this script on a copy of
ie_per_word.py in review/tmp/ie_copy and a binary in review/tmp/bin, neither of
which is in the repository.  The import path now points to ../method_ie and the
binary is built on first use (or given as CANON_ENUM), so that the script runs
from a clone; the test itself is unchanged.
"""
import os
import subprocess
import sys
from math import factorial

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "method_ie"))
sys.dont_write_bytecode = True   # write no __pycache__ into method_ie
import ie_per_word  # noqa: E402  (the project file)

if len(sys.argv) not in (3, 4):
    sys.exit(__doc__)
lo, hi = int(sys.argv[1]), int(sys.argv[2])
if len(sys.argv) == 4:
    CANON = os.path.abspath(sys.argv[3])
else:
    CANON = os.path.join(HERE, "tmp", "bin", "canon_enum")
    if not os.path.exists(CANON):
        os.makedirs(os.path.dirname(CANON), exist_ok=True)
        print("building", CANON, "from canon_enum.c", flush=True)
        subprocess.run(["gcc", "-O2", "-fopenmp", "-o", CANON,
                        os.path.join(HERE, "canon_enum.c")], check=True)
allok = True
for n in range(lo, hi + 1):
    out = subprocess.run([CANON, str(n), "words"],
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
