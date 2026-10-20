/* Independent check that does NOT use the row symmetry: DP over subsets of the
 * 2n-2 inner eyelets 2..2n-1.  State = (set of used inner eyelets, last eyelet,
 * length of the current same-side run).  Rules 1-3 of DEFINITION.md are applied
 * literally on eyelet numbers.  Only additions are used, so arithmetic mod 2^64
 * (uint64 wraparound) gives D(n) exactly whenever D(n) < 2^64 (true for n <= 12;
 * D(12) = 5.52e18).  Memory: 2^(2n-2) * (2n-2) * 2 * 8 bytes (1.5 GB at n = 12).
 * Build: gcc -O2 -o tmp/bitmask_check bitmask_check.c ; run: tmp/bitmask_check nmax
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv) {
    int nmax = argc > 1 ? atoi(argv[1]) : 11;
    for (int n = 3; n <= nmax; n++) {
        int K = 2 * n - 2;                       /* inner eyelets e = 2..2n-1 -> bit e-2 */
        size_t nm = (size_t)1 << K;
        uint64_t *dp = calloc(nm * K * 2, sizeof(uint64_t));
        if (!dp) { fprintf(stderr, "out of memory\n"); return 1; }
#define IDX(mask, j, run) (((size_t)(mask) * K + (j)) * 2 + ((run) - 1))
#define SIDE(e) ((e) <= n ? 0 : 1)
        /* p_1 = 1 (left).  p_2 = e: rule 2 needs 1 + e != 2n+1, i.e. e != 2n: automatic. */
        for (int j = 0; j < K; j++) {
            int e = j + 2;
            dp[IDX((size_t)1 << j, j, SIDE(e) == 0 ? 2 : 1)] += 1;
        }
        for (size_t mask = 1; mask < nm; mask++) {
            for (int j = 0; j < K; j++) {
                if (!(mask >> j & 1)) continue;
                int e = j + 2, s = SIDE(e);
                for (int run = 1; run <= 2; run++) {
                    uint64_t v = dp[IDX(mask, j, run)];
                    if (!v) continue;
                    for (int j2 = 0; j2 < K; j2++) {
                        if (mask >> j2 & 1) continue;
                        int e2 = j2 + 2, s2 = SIDE(e2);
                        if (e + e2 == 2 * n + 1) continue;          /* rule 2 */
                        if (s2 == s && run == 2) continue;          /* rule 3 */
                        dp[IDX(mask | ((size_t)1 << j2), j2, s2 == s ? run + 1 : 1)] += v;
                    }
                }
            }
        }
        uint64_t D = 0;                       /* p_{2n} = 2n (right side) */
        size_t full = nm - 1;
        for (int j = 0; j < K; j++) {
            int e = j + 2;                    /* rule 2: e + 2n != 2n+1 since e != 1 */
            for (int run = 1; run <= 2; run++) {
                if (SIDE(e) == 1 && run == 2) continue;   /* rule 3: R,R,R */
                D += dp[IDX(full, j, run)];
            }
        }
        printf("%d %llu %llu\n", n, (unsigned long long)D, (unsigned long long)(D / 2));
        fflush(stdout);
        free(dp);
    }
    return 0;
}
