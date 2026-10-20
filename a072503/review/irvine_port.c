/* Line-by-line C port of Sean A. Irvine's jOEIS A072503.java (downloaded to
 * review/tmp/dl_java/A072503.java from github.com/archmageirvine/joeis).
 * Only the search() routine is ported; mN, mM, mCount as in the Java code.
 * Usage: irvine_port n      (n = number of eyelet pairs, as in OEIS) */
#include <stdio.h>
#include <stdlib.h>

static int mN, mM;
static long long mCount;

static void search(int currentEyelet, int numUsed, int usedSet, int sides) {
    if (numUsed > mM) {
        if (sides != 3) ++mCount;
        return;
    }
    for (int e = 0, bit = 1; e <= mM; ++e, bit <<= 1) {
        if ((usedSet & bit) == 0 && e != mM - currentEyelet) {
            if (e < mN) {
                if (sides != 0) search(e, numUsed + 1, usedSet | bit, (sides << 1) & 3);
            } else {
                if (sides != 3) search(e, numUsed + 1, usedSet | bit, ((sides << 1) & 3) | 1);
            }
        }
    }
}

int main(int argc, char **argv) {
    int n = atoi(argv[1]);
    mN = n - 1;              /* Java: mN starts at 1 and next() increments it; first term is n = 3 */
    mM = 2 * mN - 1;
    mCount = 0;
    search(-1, 0, 0, 2);     /* 0b10 */
    printf("n=%d count=%lld a=%lld\n", n, mCount, mCount / 2);
    return 0;
}
