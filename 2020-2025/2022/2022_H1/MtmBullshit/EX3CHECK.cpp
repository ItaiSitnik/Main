#include <iostream>
#include <string>
using namespace std;

struct x {
    string s;
    int* p;
};

int main()
{
    cout << "Hello\n";
    x A;
    int n = 5;
    A.s = "ABC";
    A.p = &n;

    cout << "A: " << A.s << ", " << A.p << "\n\n";

    x B = A;

    cout << "A == B: " << (A.s == B.s && A.p == B.p) << "\n\n";

    B.p++;
    B.p--;

    cout << "A == B: " << (A.s == B.s && A.p == B.p) << "\n\n";

    B.s += " DEF";
    B.p++;

    cout << "A: " << A.s << ", " << A.p << "\n";
    cout << "B: " << B.s << ", " << B.p << "\n\n";

    cout << "A == B: " << (A.s == B.s && A.p == B.p) << "\n\n";

    return 0;
}
