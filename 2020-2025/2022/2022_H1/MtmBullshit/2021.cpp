#include <iostream>
using namespace std;

class A {
};

static class A a();

void convert(double d) {
    static int i = (int)d;
    cout << "Converted: " << d;
}

int main() {
    convert(1.0);
    return 0;
}
