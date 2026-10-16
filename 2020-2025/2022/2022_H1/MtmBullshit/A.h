#include <exception>
#include <iostream>
#include <string>
using namespace std;

class A {
   public:
    A(string name) : name(name) {
        cout << "Hello\n";
    }
    void f() {
        cout << "f called for " << name << "\n";
    }

   private:
    string name;
};
