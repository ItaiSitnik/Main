#include <iostream>
#include <string>

#define N 40

using namespace std;

struct Pair {
    int n;
    bool marked;
};

void printUnmarked(Pair a[])
{
    cout << "[ ";
    for (int i = 0; i < N; i++)
        if (!a[i].marked)
            cout << a[i].n << ((i != N - 1) ? ", " : " ]\n");
}

int main()
{
    Pair numbers[N];
    for (int i = 0; i < N; i++)
        numbers[i] = { i + 1, false };

    cout << "All Numbers:\n\t";
    printUnmarked(numbers);

    for (int i = 1; i < N; i++) {
        if (numbers[i].marked)
            continue;
        for (int j = numbers[i].n; j < N; j++)
            numbers[j].marked = numbers[j].n % numbers[i].n;
    }

    cout << "Primes:\n\t";
    printUnmarked(numbers);

    return 0;
}
