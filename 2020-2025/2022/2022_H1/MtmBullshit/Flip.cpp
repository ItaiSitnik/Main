#include <iostream>
#include <iterator>

using namespace std;

void reverse(char s[], int size)
{
    if (size < 2)
        return;
    s[0] ^= s[size - 1] ^= s[0] ^= s[size - 1];
    reverse(s + 1, size - 2);
}

int main(void)
{
    char s[] = "The path of the righteous man";
    cout << "Before: " << s << endl;
    reverse(s, sizeof(s) / sizeof(*s) - 1);
    cout << "After: " << s << endl;
    return 0;
}
