#include "stdio.h"

struct X {
    int a;
    int* b;
    struct X* next;
};

typedef struct X X;

int main() {
    printf("Hello\n");
    printf("int: %d\n", sizeof(int));
    printf("int*: %d\n", sizeof(int*));
    printf("X*: %d\n", sizeof(X*));
    printf("Total: %d\n", sizeof(int) + sizeof(int*) + sizeof(X*));
    printf("X: %d\n", sizeof(X));
    int count = 0;
    for (int t1 = 1; t1 < 30; t1 += 2)
        for (int t2 = 4; t2 < 30; t2 += 2)
            for (int t3 = 7; t3 < 30; t3 += 2)
                if (t1 + t2 + t3 == 30) {
                    count++;
                    printf("%d: %d + %d + %d\n", count, t1, t2, t3);
                }
    printf("Total: %d\n", count);
    return 0;
}
