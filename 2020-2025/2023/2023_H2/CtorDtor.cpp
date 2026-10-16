#include <iostream>
using namespace std;

class A {
   protected:
    A() {
        cout << "A C'tor\n";
    }
    ~A() {
        cout << "A D'tor\n";
    }
};

class C {
   public:
    C() {
        cout << "C C'tor\n";
    }
    ~C() {
        cout << "C D'tor\n";
    }
};

class B : public A {
    C c;

   public:
    B() {
        cout << "B C'tor\n";
    }
    ~B() {
        cout << "B D'tor\n";
    }
};

int main() {
    B b;
    cout << "==========\n";
    return 0;
}
