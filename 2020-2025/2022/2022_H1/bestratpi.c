#include <stdio.h>

#define pi 3.1415926535897932384626433

double f(double x)
{
    return x < 0 ? -x : x;
}

int main()
{
    int besti = -1, bestj = -1;
    double bestdiff = 1000;

    for (int i = 1; i < 10000; i++)
        for (int j = 1; j < 10000; j++)
            if (f(i / (double)j - pi) < bestdiff) {
                besti = i;
                bestj = j;
                bestdiff = f(i / (double)j - pi);
            }
    printf("BEST 3 DIG: %d / %d AT DIFF %f", besti, bestj, bestdiff);
}
