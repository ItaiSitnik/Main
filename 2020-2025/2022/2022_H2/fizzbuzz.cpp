#include <iostream>
#include <string>
using namespace std;

#define N 105

int main() {
    for (int x = 1; x <= N; x++) {
        string out = "";

        if (x % 3 == 0)
            out += "Fizz";

        if (x % 5 == 0)
            out += "Buzz";

        if (out == "")
            out = to_string(x);

        cout << out << endl;
    }
}
