#include <chrono>
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

template <typename S>
ostream& operator<<(ostream& os, const vector<S>& vector)
{
    for (auto element : vector)
        os << element << " ";
    return os;
}

int gcd(int a, int b)
{
    return b == 0 ? a : gcd(b, a % b);
}

int gcd(const vector<int>& v)
{
    int n = v[0];
    for (int i = 1; i < v.size(); ++i) {
        n = gcd(v[i], n);
        if (n == 1)
            return 1;
    }
    return n;
}

int lcm(int a, int b)
{
    return a * b / gcd(a, b);
}

int lcm(const vector<int>& v)
{
    int n = v[0];
    for (int i = 1; i < v.size(); ++i)
        n = lcm(v[i], n);
    return n;
}

bool isPrime(int n)
{
    if (n <= 1)
        return false;

    for (int i = 2; i <= sqrt(n); i++)
        if (n % i == 0)
            return false;

    return true;
}

template <
    class result_t = chrono::milliseconds,
    class clock_t = chrono::steady_clock,
    class duration_t = chrono::milliseconds>
auto since(chrono::time_point<clock_t, duration_t> const& start)
{
    return chrono::duration_cast<result_t>(clock_t::now() - start);
}

void comma(unsigned long long n)
{
    const unsigned int THOUSAND = 1000;

    if (n < THOUSAND)
        cout << n;
    else {
        int remainder = n % THOUSAND;
        comma(n / THOUSAND);
        cout << ',' << remainder;
    }
}
