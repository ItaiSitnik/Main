#include <limits.h>
#include <locale.h>
#include <stdio.h>

int main()
{
    int record;
    setlocale(LC_NUMERIC, "");

    for (int dest = 1; dest <= 30; dest++) {
        double sum = 0;
        long long count = 1;
        for (unsigned long long i = 1; i < ULLONG_MAX; i++, count++) {
            sum += 1 / (double)i;
            if (sum >= dest) {
                printf("%d: Done - took over %'lld numbers (sum = %.3f)\n", dest, count, sum);
                break;
            }
        }
        record = dest;
    }
    printf("Cannot be done - failed at dest : %d\n", record);
    return 0;
}
