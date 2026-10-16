#include <iostream>
#include <string>
using namespace std;

int main()
{
    string s = "Hello Goodbye";
    int spaceLocation = s.find_first_of(' ');
    string a = s.substr(0, spaceLocation);
    string b = s.substr(spaceLocation + 1);
    cout << "Splitted \"" << a << "\" from \"" << b << "\"\n\n";
    cout << "CMP1: " << (a == b) << "\n";
    cout << "CMP1: " << (a == "Hello") << "\n";
    return 0;
}
