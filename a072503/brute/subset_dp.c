/* Direct check of A072503 by dynamic programming over subsets (Held-Karp style).
 *
 * This is the definition from DEFINITION.md translated literally, without any
 * symmetry argument: a partial lacing 1 = p_1, p_2, ..., p_k is summarised by
 *   (set of inner eyelets used, last eyelet p_k, flag "p_{k-1} is on the same side as p_k").
 * That is all the rules need: rule 2 looks at the last eyelet only, rule 3 at the
 * sides of the last two.  The table therefore counts every lacing exactly once.
 *
 * Inner eyelets are 2..2n-1 (eyelet 1 is the fixed start, 2n the fixed end);
 * bit i of the mask stands for eyelet i+2.  Table size: 2^(2n-2) * (2n-2) * 2.
 *
 * Arithmetic (compile-time):  -DMODE=0  exact unsigned __int128
 *                             -DMODE=1  modulo 2^64
 *                             -DMODE=2  modulo p = 2^61-1
 * For large n, MODE=1 and MODE=2 are combined by the Chinese remainder theorem
 * (brute/crt.py); this is exact as long as D(n) < 2^125.
 *
 * Usage: subset_dp n        prints  "n=<n> mode=<m> D=<D mod ...>"
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>

#ifndef MODE
#define MODE 0
#endif

#if MODE == 0
typedef unsigned __int128 val;
static inline val ADD(val a, val b) { return a + b; }
#elif MODE == 1
typedef uint64_t val;
static inline val ADD(val a, val b) { return a + b; }
#else
typedef uint64_t val;
static const uint64_t P = (1ULL << 61) - 1;
static inline val ADD(val a, val b) { val s = a + b; return s >= P ? s - P : s; }
#endif

static void print_val(val v) {
    char buf[64]; int i = 63; buf[i] = 0;
    if (v == 0) buf[--i] = '0';
    while (v > 0) { buf[--i] = (char)('0' + (int)(v % 10)); v /= 10; }
    printf("%s", buf + i);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s n\n", argv[0]); return 1; }
    int n = atoi(argv[1]);
    int N = 2 * n, M = N - 2;                 /* M inner eyelets */
    if (n < 2 || M > 24) { fprintf(stderr, "n out of range\n"); return 1; }
    int eye[32], sd[32], partner[32];         /* index -> eyelet, side, partner index */
    for (int i = 0; i < M; i++) { eye[i] = i + 2; sd[i] = (eye[i] <= n) ? 0 : 1; }
    for (int i = 0; i < M; i++) partner[i] = (N + 1 - eye[i]) - 2;   /* in 0..M-1 */
    uint64_t nmask = 1ULL << M;
    size_t entries = (size_t)nmask * M * 2;
    fprintf(stderr, "[subset_dp n=%d mode=%d] table %zu entries, %.2f GB\n",
            n, MODE, entries, entries * sizeof(val) / 1e9);
    val *T = calloc(entries, sizeof(val));
    if (!T) { fprintf(stderr, "out of memory\n"); return 2; }
#define IDX(mask, e, s) ((((size_t)(mask)) * M + (e)) * 2 + (s))
    double t0 = omp_get_wtime();
    /* first step 1 -> p_2 (eyelet 1 is on the left; its partner 2n is not inner) */
    for (int e = 0; e < M; e++) T[IDX(1ULL << e, e, sd[e] == 0)] = 1;
    /* layers by popcount: pull from layer k-1 */
    for (int k = 2; k <= M; k++) {
        #pragma omp parallel for schedule(dynamic, 4096)
        for (uint64_t mask = 0; mask < nmask; mask++) {
            if (__builtin_popcountll(mask) != k) continue;
            for (int f = 0; f < M; f++) {            /* new last eyelet */
                if (!(mask >> f & 1)) continue;
                uint64_t pm = mask ^ (1ULL << f);
                val same = 0, diff = 0;
                for (int e = 0; e < M; e++) {        /* previous last eyelet */
                    if (!(pm >> e & 1)) continue;
                    if (e == partner[f]) continue;   /* rule 2: horizontal pair */
                    if (sd[e] == sd[f]) {
                        /* rule 3: allowed only if the eyelet before e was on the other side */
                        same = ADD(same, T[IDX(pm, e, 0)]);
                    } else {
                        diff = ADD(diff, T[IDX(pm, e, 0)]);
                        diff = ADD(diff, T[IDX(pm, e, 1)]);
                    }
                }
                T[IDX(mask, f, 1)] = same;
                T[IDX(mask, f, 0)] = diff;
            }
        }
        fprintf(stderr, "[subset_dp n=%d mode=%d] layer %d/%d done, t=%.1fs\n",
                n, MODE, k, M, omp_get_wtime() - t0);
    }
    /* last step p_{2n-1} -> 2n (right side; never a horizontal pair since p_{2n-1} >= 2) */
    val D = 0;
    uint64_t full = nmask - 1;
    for (int e = 0; e < M; e++) {
        D = ADD(D, T[IDX(full, e, 0)]);
        if (sd[e] == 0) D = ADD(D, T[IDX(full, e, 1)]);
    }
    printf("n=%d mode=%d D=", n, MODE); print_val(D);
#if MODE == 0
    printf(" a=");  print_val(D / 2); printf(" odd=%d", (int)(D & 1));
#endif
    printf(" time=%.2fs\n", omp_get_wtime() - t0);
    free(T);
    return 0;
}
