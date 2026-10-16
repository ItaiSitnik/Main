#include <iostream>
using namespace std;

int n;

class A {
   private:
    int id;

   public:
    A() : id(n++) {
        cout << "A ctor " << id << "\n";
    }
    ~A() {
        cout << "A dtor " << id << "\n";
    }
};

class B : public A {
   private:
    int id;

   public:
    B() : id(n++) {
        cout << "B ctor " << id << "\n";
    }
    ~B() {
        cout << "B dtor " << id << "\n";
    }
};

class C : public B {
   private:
    int id;
    A a1;
    A a2;
    B b;

   public:
    C() : id(n++) {
        cout << "C ctor " << id << "\n";
    }
    ~C() {
        cout << "C dtor " << id << "\n";
    }
};

int main() {
    C c;
    cout << "-------------\n";
    return 0;
}
