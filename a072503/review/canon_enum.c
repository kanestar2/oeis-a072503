/* Reviewer's independent check (written without reusing any project code).
 *
 * Literal enumeration of CANONICAL lacings.  Any permutation of the inner rows
 * 2..n (applied to both eyelets of a row, sides kept) maps lacings to lacings,
 * and the group S_{n-1} acts freely (a non-identity row permutation moves some
 * eyelet).  Each orbit contains exactly one lacing in which the inner rows are
 * first visited in the order 2, 3, ..., n.  So
 *        D(n) = (n-1)! * C(n),   C(n) = number of canonical lacings.
 * C(n) is enumerated one lacing at a time; all rules are tested literally on
 * Pfoertner eyelet numbers (side: e <= n is left; horizontal: e + f == 2n+1).
 *
 * Usage: canon_enum n [words]
 *   prints  n C(n) D(n)=(n-1)!*C(n) a(n)=D/2  (exact, unsigned __int128)
 *   with "words": also prints, per side word, the number of canonical lacings
 *   (to be multiplied by (n-1)! for the true per-word count).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>

static int n, N, WORDS;

typedef struct {
    int used[40];      /* used[e] = 1 if eyelet e already placed */
    int path[40];
    int next_row;      /* next inner row that may be opened (2..n+1) */
    uint64_t cnt;
    /* per-word counts (only for small n): index = bitmask of sides of p_1..p_2n */
    uint64_t *wc;
} st_t;

static inline int side(int e) { return e <= n ? 0 : 1; }
static inline int rowof(int e) { return e <= n ? e : N + 1 - e; }

static void dfs(st_t *S, int k) {          /* k eyelets placed: path[0..k-1] */
    int last = S->path[k - 1];
    if (k == N - 1) {                        /* only eyelet 2n remains, must be last */
        int e = N;
        if (last + e == N + 1) return;                                     /* rule 2 */
        if (side(S->path[k - 2]) == side(last) && side(last) == side(e)) return; /* rule 3 */
        S->cnt++;
        if (WORDS) {
            uint32_t w = 0;
            for (int i = 0; i < N - 1; i++) w |= (uint32_t)side(S->path[i]) << i;
            w |= 1u << (N - 1);
            S->wc[w]++;
        }
        return;
    }
    for (int e = 2; e <= N - 1; e++) {
        if (S->used[e]) continue;
        int r = rowof(e);
        int partner = N + 1 - e;
        /* canonical: a row may be entered for the first time only if it is next_row */
        int opening = !S->used[partner];
        if (opening && r != S->next_row) continue;
        if (last + e == N + 1) continue;                                       /* rule 2 */
        if (k >= 2 && side(S->path[k - 2]) == side(last) && side(last) == side(e)) continue; /* rule 3 */
        S->used[e] = 1; S->path[k] = e;
        if (opening) S->next_row++;
        dfs(S, k + 1);
        if (opening) S->next_row--;
        S->used[e] = 0;
    }
}

/* enumerate canonical prefixes of a given length for parallel jobs */
typedef struct { int path[12]; int len; } job_t;
static job_t *jobs; static int njobs, capjobs;

static void gen(int *path, int *used, int next_row, int k, int depth) {
    if (k == depth) {
        if (njobs == capjobs) { capjobs = capjobs ? 2 * capjobs : 1024; jobs = realloc(jobs, capjobs * sizeof(job_t)); }
        memcpy(jobs[njobs].path, path, k * sizeof(int)); jobs[njobs].len = k; njobs++;
        return;
    }
    int last = path[k - 1];
    for (int e = 2; e <= N - 1; e++) {
        if (used[e]) continue;
        int opening = !used[N + 1 - e];
        if (opening && rowof(e) != next_row) continue;
        if (last + e == N + 1) continue;
        if (k >= 2 && side(path[k - 2]) == side(last) && side(last) == side(e)) continue;
        used[e] = 1; path[k] = e;
        gen(path, used, next_row + opening, k + 1, depth);
        used[e] = 0;
    }
}

static void print_u128(unsigned __int128 v) {
    char b[64]; int i = 63; b[i] = 0;
    if (!v) b[--i] = '0';
    while (v) { b[--i] = '0' + (int)(v % 10); v /= 10; }
    printf("%s", b + i);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s n [words]\n", argv[0]); return 1; }
    n = atoi(argv[1]); N = 2 * n; WORDS = argc > 2;
    if (n < 3 || n > 16 || (WORDS && n > 10)) { fprintf(stderr, "n out of range\n"); return 1; }
    double t0 = omp_get_wtime();
    int path[40] = {0}, used[40] = {0};
    path[0] = 1; used[1] = 1;
    int depth = N - 1 < 7 ? N - 1 : 7;   /* prefix length for the parallel split */
    gen(path, used, 2, 1, depth);
    uint64_t total = 0;
    size_t wsz = WORDS ? ((size_t)1 << N) : 0;
    uint64_t *wtot = WORDS ? calloc(wsz, sizeof(uint64_t)) : NULL;
    #pragma omp parallel reduction(+:total)
    {
        st_t S; memset(&S, 0, sizeof S);
        S.wc = WORDS ? calloc(wsz, sizeof(uint64_t)) : NULL;
        #pragma omp for schedule(dynamic, 1)
        for (int j = 0; j < njobs; j++) {
            memset(S.used, 0, sizeof S.used);
            int nr = 2;
            for (int i = 0; i < jobs[j].len; i++) {
                int e = jobs[j].path[i];
                S.path[i] = e;
                if (e != 1 && !S.used[N + 1 - e]) nr++;
                S.used[e] = 1;
            }
            S.next_row = nr;
            S.cnt = 0;
            if (jobs[j].len == N - 1) {      /* tiny n: prefix is everything but 2n */
                int k = N - 1, last = S.path[k - 1];
                if (!(side(S.path[k - 2]) == 1 && side(last) == 1)) {
                    S.cnt = 1;
                    if (WORDS) { uint32_t w = 0; for (int i = 0; i < N - 1; i++) w |= (uint32_t)side(S.path[i]) << i; w |= 1u << (N-1); S.wc[w]++; }
                }
            } else dfs(&S, jobs[j].len);
            total += S.cnt;
        }
        if (WORDS) {
            #pragma omp critical
            for (size_t w = 0; w < wsz; w++) wtot[w] += S.wc[w];
            free(S.wc);
        }
    }
    unsigned __int128 f = 1;
    for (int i = 2; i <= n - 1; i++) f *= i;
    unsigned __int128 D = f * total;
    printf("n=%d C=%llu D=", n, (unsigned long long)total); print_u128(D);
    printf(" a="); print_u128(D / 2); printf(" Dodd=%d jobs=%d time=%.2fs\n", (int)(D & 1), njobs, omp_get_wtime() - t0);
    if (WORDS) {
        for (size_t w = 0; w < wsz; w++) if (wtot[w]) {
            for (int i = 0; i < N; i++) putchar((w >> i & 1) ? 'R' : 'L');
            printf(" %llu\n", (unsigned long long)wtot[w]);
        }
    }
    return 0;
}
