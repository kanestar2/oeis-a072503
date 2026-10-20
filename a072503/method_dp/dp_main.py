#!/usr/bin/env python3
"""Main program: backward profile DP for A072503, all n in one pass, resumable.

F(a, b, c, s, r, f) = number of ways to COMPLETE a lacing from a state in which
  a inner rows are untouched, b inner rows have only the left eyelet used,
  c inner rows have only the right eyelet used, the last placed eyelet is on
  side s (0=L, 1=R), ends a run of r (1 or 2) equal sides, and f = 1 iff its
  partner eyelet is still unused.  (Full derivation: METHOD.md.)
F does not depend on n, so one table serves every n:
    D(n) = F(n-1, 0, 0, L, 1, 0)      (state right after p_1 = eyelet 1).
Layer k = set of states with k = 2a+b+c inner eyelets still to place; layer k
depends only on layer k-1.  D(n) is read off layer 2(n-1).

Usage: python3 dp_main.py NMAX [time_budget_minutes=20]
  * appends "n D(n) a(n)" to results.txt (skips n already there, but checks
    that a recomputed value equals the stored one),
  * logs to progress.log, checkpoints the current layer to tmp/checkpoint.pkl
    (every 5 min and on exit) and resumes from it on restart.
"""
import os
import sys
import time
import pickle
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.txt")
LOG = os.path.join(HERE, "progress.log")
CKPT = os.path.join(HERE, "tmp", "checkpoint.pkl")
L, R = 0, 1


def ix(s, r, f):
    return 4 * s + 2 * (r - 1) + f


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S") + "  " + msg
    with open(LOG, "a") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def objvec(values):
    v = np.empty(len(values), dtype=object)
    v[:] = list(values)
    return v


def layer0():
    # all inner eyelets placed; only p_{2n} = 2n (right side) remains.
    # It is forbidden iff the last two eyelets were both on the right (rule 3).
    return [[objvec([0 if (s == R and r == 2) else 1])
             for s in (L, R) for r in (1, 2) for f in (0, 1)]]


def next_layer(P, k):
    """Layer k (list over a = 0..k//2 of 8 object arrays indexed by b) from P = layer k-1."""
    out = []
    for a in range(k // 2 + 1):
        nb = k - 2 * a + 1                      # b = 0..k-2a, c = k-2a-b
        bvec = objvec(range(nb))
        cvec = bvec[::-1].copy()
        zero = objvec([0] * nb)
        if a >= 1:                              # take an eyelet of an untouched row (a choices)
            A = P[a - 1]                        # layer k-1 entry a-1 has length nb+1
            nL2 = a * A[ix(L, 2, 1)][1:]        # -> state (a-1, b+1, c), side L, f=1
            nL1 = a * A[ix(L, 1, 1)][1:]
            nR2 = a * A[ix(R, 2, 1)][:-1]       # -> state (a-1, b, c+1), side R, f=1
            nR1 = a * A[ix(R, 1, 1)][:-1]
        else:
            nL2 = nL1 = nR2 = nR1 = zero
        if nb >= 2:                             # take the 2nd eyelet of a half-used row
            B = P[a]                            # layer k-1 entry a has length nb-1
            z = objvec([0])
            oL2 = np.concatenate((B[ix(L, 2, 0)], z))   # -> (a, b, c-1), side L, f=0
            oL1 = np.concatenate((B[ix(L, 1, 0)], z))
            oR2 = np.concatenate((z, B[ix(R, 2, 0)]))   # -> (a, b-1, c), side R, f=0
            oR1 = np.concatenate((z, B[ix(R, 1, 0)]))
        else:
            oL2 = oL1 = oR2 = oR1 = zero
        GL2 = nL2 + cvec * oL2        # next eyelet left, same side as a left run of 1
        HL10 = nL1 + cvec * oL1       # next eyelet left after a right eyelet, f=0
        HL11 = HL10 - oL1             #   ... f=1: the partner (one of the c rows) is forbidden
        GR2 = nR2 + bvec * oR2
        HR10 = nR1 + bvec * oR1
        HR11 = HR10 - oR1
        e = [None] * 8
        e[ix(L, 1, 0)] = GL2 + HR10
        e[ix(L, 1, 1)] = GL2 + HR11
        e[ix(L, 2, 0)] = HR10         # run of 2 on the left: must switch to the right
        e[ix(L, 2, 1)] = HR11
        e[ix(R, 1, 0)] = GR2 + HL10
        e[ix(R, 1, 1)] = GR2 + HL11
        e[ix(R, 2, 0)] = HL10
        e[ix(R, 2, 1)] = HL11
        out.append(e)
    return out


def read_results():
    have = {}
    if os.path.exists(RESULTS):
        with open(RESULTS) as fh:
            for line in fh:
                if line.strip():
                    n, D, a = line.split()
                    have[int(n)] = (int(D), int(a))
    return have


def save_ckpt(k, layer):
    tmpf = CKPT + ".tmp"
    with open(tmpf, "wb") as fh:
        pickle.dump((k, layer), fh, protocol=pickle.HIGHEST_PROTOCOL)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmpf, CKPT)


def main():
    nmax = int(sys.argv[1])
    budget = 60.0 * (float(sys.argv[2]) if len(sys.argv) > 2 else 20.0)
    os.makedirs(os.path.dirname(CKPT), exist_ok=True)
    t0 = time.time()
    have = read_results()
    if os.path.exists(CKPT):
        with open(CKPT, "rb") as fh:
            k, layer = pickle.load(fh)
        log(f"start nmax={nmax}: resumed from checkpoint at layer k={k}; "
            f"{len(have)} n already in results.txt")
    else:
        k, layer = 0, layer0()
        log(f"start nmax={nmax}: fresh start; {len(have)} n already in results.txt")
    last_ckpt = time.time()
    kmax = 2 * (nmax - 1)
    while k < kmax:
        k += 1
        layer = next_layer(layer, k)
        if k % 2 == 0 and k // 2 + 1 >= 3:
            n = k // 2 + 1
            D = int(layer[n - 1][ix(L, 1, 0)][0])
            assert D % 2 == 0, (n, D)
            if n in have:
                assert have[n] == (D, D // 2), f"mismatch with stored value at n={n}"
            else:
                with open(RESULTS, "a") as fh:
                    fh.write(f"{n} {D} {D // 2}\n")
                    fh.flush()
                    os.fsync(fh.fileno())
                have[n] = (D, D // 2)
            log(f"n={n} done ({len(str(D // 2))} digits), elapsed {time.time() - t0:.1f}s")
        now = time.time()
        if k < kmax and (now - last_ckpt > 300 or now - t0 > budget):
            save_ckpt(k, layer)
            last_ckpt = now
            log(f"checkpoint saved at layer k={k}")
            if now - t0 > budget:
                log("time budget reached; rerun the same command to continue")
                return
    save_ckpt(k, layer)
    log(f"finished up to nmax={nmax} (checkpoint at k={k}), total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
