#include <deque>
#include <iostream>
#include <memory>
using namespace std;

class A {
   public:
    int n;
    A(int n) : n(n) {}
};

int fibCache[47];

int fib(int n) {
    if (fibCache[n] != -1)
        return fibCache[n];
    if (n < 2) {
        fibCache[n] = n;
        return n;
    }
    fibCache[n] = fib(n - 1) + fib(n - 2);
    return fibCache[n];
}

int main() {
    for (int& n : fibCache)
        n = -1;
    cout << fib(46) << "\n";

    unique_ptr<A> a(new A(1));
    unique_ptr<A> b(new A(2));
    unique_ptr<A> c(new A(3));

    deque<unique_ptr<A>> deque1, deque2;
    deque1.push_back(move(a));
    deque1.push_back(move(b));
    deque1.push_back(move(c));

    cout << "first: ";
    for (auto& p : deque1)
        cout << p->n << ", ";
    cout << "\n";
    cout << "second: ";
    for (auto& p : deque2)
        cout << p->n << ", ";
    cout << "\n\n";

    deque2.push_back(move(b));

    cout << "first: ";
    for (auto& p : deque1)
        cout << p->n << ", ";
    cout << "\n";
    cout << "second: ";
    for (auto& p : deque2)
        cout << p->n << ", ";
    cout << "\n\n";

    return 0;
}
