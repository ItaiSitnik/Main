#include <iostream>

class A {
   public:
    int x;
    A(int x) : x(x) {}
    A operator+(const A& a) { return A(x + a.x); }
};

int main() {
    A a(1), b(2), c(3);
    A d = a + (b + c);
    // std::cout << d.x;
}
