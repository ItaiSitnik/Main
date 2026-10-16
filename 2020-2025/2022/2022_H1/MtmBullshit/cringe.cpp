#include <iostream>
using namespace std;

class A {
protected:
    virtual void print() = 0;
};

void A::print()
{
    cout << "1\n";
}

class B : public A {
public:
    void print() override
    {
        A::print();
        cout << "2\n";
    }
};

int main()
{
    B b;
    b.print();
    return 0;
}
