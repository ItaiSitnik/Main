#include "A.h"

static class A x("x");
static A y("y");
A z("z");

void convert(double d) {
    static int i = (int)d;
}

void inc(int i) {
    cout << "  (i: " << i << ")\n";

    static int count;
    cout << "  [old count: " << count << "]\n";
    count = i;
    count++;
    cout << "count: " << count << "\n\n";
}

int main() {
    // for (int i = 0; i < 5; i++)
    //     inc(rand());
    x.f();
    y.f();
    z.f();
    return 0;
}
