#include <time.h>

#include <array>
#include <iostream>
#include <limits>

using namespace std;

int main() {
    clock_t tStart = clock();
    int* a = new int[(int)3e8];
    for (int i = 0; i < (int)3e8; i++)
        a[i] = rand() % 100;
    cout << "Time taken: " << (double)(clock() - tStart) / CLOCKS_PER_SEC << "s\n ";
    return 0;
}
