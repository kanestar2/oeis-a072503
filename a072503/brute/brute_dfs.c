/* Literal enumeration of A072503 lacings (depth-first search, one lacing at a time).
 *
 * Eyelets (Pfoertner numbering): 1..n on the left (top to bottom), n+1..2n on the
 * right (bottom to top).  Horizontal pairs are (k, 2n+1-k); (1, 2n) is the top pair.
 * A lacing is an ordering p_1..p_{2n} of all 2n eyelets with
 *   p_1 = 1, p_{2n} = 2n                         (starts/ends at the top pair)
 *   p_i + p_{i+1} != 2n+1 for all i              (no horizontal connection)
 *   p_i, p_{i+1}, p_{i+2} never all on one side  (no three on the same side)
 * We count these directed lacings D(n); A072503(n) = D(n)/2 (mirror images).
 *
 * Usage: brute_dfs n [print]     ("print" lists every lacing, only for small n)
 * Parallelised over the choice of p_2, p_3 with OpenMP.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <omp.h>

static int n, N, PRINT;

static inline int side(int e) { return e <= n ? 0 : 1; }

/* used: bitmask of used eyelets (bit e), last = p_k, prevside = side(p_{k-1}) or -1,
 * k = number of placed eyelets */
static uint64_t dfs(uint32_t used, int last, int prevside, int k, int *path) {
    if (k == N - 1) {           /* only eyelet N (=2n) is left; it must be last */
        if (last + N == N + 1) return 0;                      /* horizontal (never for n>1) */
        if (prevside == 1 && side(last) == 1) return 0;       /* three on the right */
        if (PRINT) {
            #pragma omp critical
            { for (int i = 0; i < N - 1; i++) printf("%d%s", path[i], N > 9 ? " " : "");
              printf("%d\n", N); }
        }
        return 1;
    }
    uint64_t cnt = 0;
    int ls = side(last);
    for (int e = 2; e < N; e++) {
        if (used >> e & 1) continue;
        if (e + last == N + 1) continue;                      /* horizontal pair */
        if (prevside == ls && side(e) == ls) continue;        /* three on one side */
        path[k] = e;
        cnt += dfs(used | (1u << e), e, ls, k + 1, path);
    }
    return cnt;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s n [print]\n", argv[0]); return 1; }
    n = atoi(argv[1]); N = 2 * n; PRINT = argc > 2;
    if (n < 2 || n > 15) { fprintf(stderr, "n out of range\n"); return 1; }
    double t0 = omp_get_wtime();
    /* jobs = all valid (p_2, p_3) */
    int jobs[1024][2], nj = 0;
    for (int a = 2; a < N; a++) {
        if (a + 1 == N + 1) continue;
        for (int b = 2; b < N; b++) {
            if (b == a || a + b == N + 1) continue;
            if (side(1) == side(a) && side(a) == side(b)) continue;
            jobs[nj][0] = a; jobs[nj][1] = b; nj++;
        }
    }
    uint64_t total = 0; int done = 0;
    #pragma omp parallel for schedule(dynamic, 1) reduction(+:total)
    for (int j = 0; j < nj; j++) {
        int path[64]; path[0] = 1; path[1] = jobs[j][0]; path[2] = jobs[j][1];
        uint32_t used = (1u << 1) | (1u << jobs[j][0]) | (1u << jobs[j][1]);
        uint64_t c = dfs(used, jobs[j][1], side(jobs[j][0]), 3, path);
        total += c;
        #pragma omp critical
        { done++; if (!PRINT && n >= 8)
            fprintf(stderr, "[n=%d] job %d/%d done (p2=%d p3=%d count=%llu) t=%.1fs\n",
                    n, done, nj, jobs[j][0], jobs[j][1], (unsigned long long)c, omp_get_wtime() - t0); }
    }
    if (!PRINT) printf("n=%d directed=%llu a(n)=%llu odd=%d time=%.2fs\n", n,
                       (unsigned long long)total, (unsigned long long)(total / 2),
                       (int)(total & 1), omp_get_wtime() - t0);
    return 0;
}
