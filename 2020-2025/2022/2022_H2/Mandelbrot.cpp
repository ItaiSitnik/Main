#include <cmath>
#include <complex>
#include <iostream>
using namespace std;

#define N 41
#define INTERS 100
#define THRESHOLD 2

bool getMandelbrot(double x, double y) {
    x -= (N - 1) / 2 + N / 4.0;  // translate
    y += (N - 1) / 2;
    x /= 0.45 * N;  // scale
    y /= 0.45 * N;

    complex<double> c{x, y}, z{};
    for (int i = 0; i < INTERS; i++) {
        z = z * z + c;
        if (abs(z) > THRESHOLD)
            return false;
    }
    return true;
}

int main() {
    bool grid[N][N];

    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            grid[i][j] = getMandelbrot(j, -i);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (j != 0)
                cout << ' ';
            cout << (grid[i][j] ? 'X' : ' ');
        }
        cout << "\n";
    }
}
