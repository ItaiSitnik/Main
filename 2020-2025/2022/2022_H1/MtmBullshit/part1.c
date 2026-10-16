#include <stdio.h>
#include <stdlib.h>

int get2PowerExponent(int n)
{
    if (!n || n & (n - 1)) {
        return -1;
    }
    int exponent = 0;
    while (n /= 2) {
        exponent++;
    }
    return exponent;
}

int main()
{
    int size = 0;
    printf("Enter size of input:\n");
    scanf("%d", &size);

    if (size <= 0) {
        printf("Invalid size\n");
        return 0;
    }

    int* input = (int*)malloc(size * sizeof(int));

    printf("Enter numbers:\n");
    for (int scanned, i = 0; i < size; i++) {
        scanned = scanf("%d", &input[i]);
        if (!scanned || scanned == EOF) {
            printf("Invalid number\n");
            return 0;
        }
    }

    int sum = 0;
    for (int exponent, i = 0; i < size; i++) {
        exponent = get2PowerExponent(input[i]);
        if (exponent != -1) {
            printf("The number %d is a power of 2: %d = 2^%d\n", input[i], input[i], exponent);
            sum += exponent;
        }
    }

    printf("Total exponent sum is %d\n", sum);
    free(input);
    return 0;
}
