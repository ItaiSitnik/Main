#include <iostream>
using namespace std;

bool isValidID(int id)
{
    int dest = id % 10;
    id /= 10;
    int w_sum = 0;
    for (int i = 0, w = 2; i < 8; i++, w = 3 - w) {
        int digit = id % 10;
        digit *= w;
        if (digit > 10)
            digit = digit / 10 + digit % 10;
        w_sum += digit;
        id /= 10;
    }
    if (w_sum % 10 == 0)
        return dest == 0;
    return ((w_sum / 10 + 1) * 10 - w_sum) == dest;
}

int main()
{
    double number_of_valids = 0;
    for (int i = 1e8; i < 1e9; i++)
        if (isValidID(i))
            number_of_valids++;
    cout << (int)number_of_valids << " numbers of " << 900000000 << " were valid (" << 100 * (number_of_valids / 900000000) << "%)\n";
    return 0;
}
