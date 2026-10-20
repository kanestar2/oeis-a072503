#!/usr/bin/env python3
"""A072503 by side templates + inclusion-exclusion over forbidden horizontals.

    D(n) = (n-1)! * sum_k (-1)^k (n-1-k)! N_n(k),    a(n) = D(n)/2,

where N_n(k) = sum over admissible side words w of m_k(w), the number of
k-sets of interior switch places of w no two of which share an eyelet
position (see METHOD.md).  N_n(k) is computed by a transfer DP over the
blocks (L-run, R-run) of the word:

  state (i, h, s): i letters L and h letters R used, s = 1 iff the switch
  place after the last block (an R->L place) is selected; the polynomial
  in t (t marks selected places) is stored packed in one Python int with
  B bits per coefficient (all coefficients are non-negative and < 2^B).

  block (alpha, beta, a, s'): L-run of length alpha, R-run of length beta,
  a = 1 iff the inner L->R place is selected, s' = 1 iff the next R->L
  place is selected.  Forbidden: alpha = 1 and s = a = 1; beta = 1 and
  a = s' = 1.  The virtual place before position 1 has s = 1; the virtual
  place after position 2n has s' = 1 and weight 1, hence
  N_n(k) = [t^(k+1)] F[n][n][s=1].

Cells are computed in layers m = max(i, h); layer m needs layers m-1, m-2
only, so the program is incremental in n.  Results are appended to
results.txt ("n D(n) a(n)"), progress to progress.log, and the two last
layers are checkpointed (unpacked) so that a restart continues.

usage: python3 ie_dp.py NMAX [--budget SECONDS] [--dir DIR] [--no-ckpt]
"""
import os
import sys
import time
import pickle
import argparse
from math import factorial


def coef_bits(nmax):
    # every coefficient of a cell (i,h), i,h <= nmax, is at most
    # (#partial words) * (#sets of non-adjacent places) <= 2^(i+h) * Fib(i+h+1)
    # <= 2^(2N) * phi^(2N) < 2^(3.389 N); one spare bit.
    return (3389 * nmax) // 1000 + 2


def pack(coefs, B):
    v = 0
    for c in reversed(coefs):
        v = (v << B) | c
    return v


def unpack(v, B):
    mask = (1 << B) - 1
    out = []
    while v:
        out.append(v & mask)
        v >>= B
    return out


def D_from_N(n, Nk):
    s = 0
    f = factorial
    for k, c in enumerate(Nk):
        if c:
            assert k <= n - 1
            s += (-1) ** k * f(n - 1 - k) * c
    return f(n - 1) * s


class Solver:
    def __init__(self, B):
        self.B = B
        self.layers = {}            # m -> {(i,h): (P0, P1)}

    def cell(self, i, h):
        if i < 0 or h < 0:
            return None
        m = max(i, h)
        L = self.layers.get(m)
        if L is None:
            return None
        return L.get((i, h))

    def init(self):
        # layer 0: only (0,0) with the virtual place before position 1 selected
        self.layers = {0: {(0, 0): (0, 1)}}
        self.done_layer = 0

    def compute_layer(self, m):
        B = self.B
        new = {}
        targets = [(m, h) for h in range(0, m + 1)] + [(i, m) for i in range(0, m)]
        for (i, h) in targets:
            F0 = 0
            F1 = 0
            for al in (1, 2):
                for be in (1, 2):
                    src = self.cell(i - al, h - be)
                    if src is None:
                        continue
                    P0, P1 = src
                    S = P0 + P1
                    # U = sum over a of t^a * (allowed sources): a=1 needs not(al=1 and s=1)
                    U = S + ((S if al == 2 else P0) << B)
                    F0 += U                         # s' = 0: everything allowed
                    F1 += U if be == 2 else S       # s' = 1: be=1 forbids a=1
            if F0 or F1:
                new[(i, h)] = (F0, F1 << B)         # s' = 1 carries one t
        self.layers[m] = new
        self.layers.pop(m - 2, None)
        self.done_layer = m

    def N_of(self, n):
        c = self.layers[n].get((n, n))
        if c is None:
            return []
        co = unpack(c[1], self.B)
        assert co[0] == 0
        return co[1:]

    # checkpoint: unpacked coefficient lists of the last two layers
    def save(self, path):
        m = self.done_layer
        data = {'m': m, 'layers': {}}
        for mm in (m - 1, m):
            if mm in self.layers:
                data['layers'][mm] = {k: (unpack(a, self.B), unpack(b, self.B))
                                      for k, (a, b) in self.layers[mm].items()}
        tmp = path + '.tmp'
        with open(tmp, 'wb') as fh:
            pickle.dump(data, fh, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, path)

    def load(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
        self.layers = {mm: {k: (pack(a, self.B), pack(b, self.B)) for k, (a, b) in L.items()}
                       for mm, L in data['layers'].items()}
        self.done_layer = data['m']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nmax', type=int)
    ap.add_argument('--budget', type=float, default=1400.0,
                    help='stop (with checkpoint) after this many seconds')
    ap.add_argument('--dir', default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--no-ckpt', action='store_true')
    ap.add_argument('--ckpt-every', type=float, default=120.0)
    ap.add_argument('--bits', type=int, default=0, help='override B (testing)')
    args = ap.parse_args()

    res_path = os.path.join(args.dir, 'results.txt')
    log_path = os.path.join(args.dir, 'progress.log')
    ck_path = os.path.join(args.dir, 'tmp', 'ie_dp.ckpt')
    os.makedirs(os.path.join(args.dir, 'tmp'), exist_ok=True)

    def log(msg):
        line = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + msg
        print(line, flush=True)
        with open(log_path, 'a') as fh:
            fh.write(line + '\n')

    known = {}
    if os.path.exists(res_path):
        good = []
        for line in open(res_path):
            p = line.split()
            # accept only complete lines (newline-terminated, D = 2a); a line cut
            # by a kill during the append is dropped and recomputed
            if line.endswith('\n') and len(p) == 3 and int(p[1]) == 2 * int(p[2]):
                known[int(p[0])] = (int(p[1]), int(p[2]))
                good.append(line)
        if ''.join(good) != open(res_path).read():
            with open(res_path, 'w') as fh:
                fh.write(''.join(good))
            log('dropped an incomplete line from results.txt')

    B = args.bits or coef_bits(args.nmax)
    sv = Solver(B)
    start_m = 0
    if not args.no_ckpt and os.path.exists(ck_path):
        sv.load(ck_path)
        start_m = sv.done_layer
        log(f'resumed from checkpoint at layer {start_m} (B={B})')
    else:
        sv.init()
    t0 = time.time()
    last_ck = t0
    log(f'start: nmax={args.nmax} B={B} first layer={start_m + 1} '
        f'known n={min(known) if known else None}..{max(known) if known else None}')
    for m in range(start_m + 1, args.nmax + 1):
        sv.compute_layer(m)
        n = m
        if n < 2:          # the formula needs n >= 2 (for n = 1 the top pair is horizontal)
            continue
        Nk = sv.N_of(n)
        D = D_from_N(n, Nk)
        assert D % 2 == 0, (n, D)
        a = D // 2
        if n in known:
            if known[n] != (D, a):
                log(f'ERROR: n={n} recomputed value differs from results.txt')
                sys.exit(1)
        elif n >= 3:
            with open(res_path, 'a') as fh:
                fh.write(f'{n} {D} {a}\n')
            known[n] = (D, a)
        el = time.time() - t0
        if n <= 12 or n % 10 == 0:
            log(f'n={n} done, elapsed {el:.1f}s, a(n) has {len(str(a))} digits')
        now = time.time()
        if not args.no_ckpt and (now - last_ck > args.ckpt_every or m == args.nmax):
            sv.save(ck_path)
            last_ck = time.time()
            log(f'checkpoint saved at layer {m} ({last_ck - now:.1f}s)')
        if now - t0 > args.budget and m < args.nmax:
            if not args.no_ckpt:
                sv.save(ck_path)
            log(f'budget exhausted after layer {m}; rerun the same command to continue')
            return
    log(f'finished up to n={args.nmax}, total {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
