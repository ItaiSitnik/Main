#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

void printVector(vector<int> v) {
    for (int i : v)
        cout << i << ' ';
    cout << "\n";
}

int main() {
    vector<int> v = {1, 1}, old_v;

    for (int n = 2; n <= 15; n++) {
        std::cout << "n = " << n << ": ";
        printVector(v);
        old_v.assign(v.begin(), v.end());
        v.clear();
        for (int i = 0; i < old_v.size() - 1; i++) {
            v.push_back(old_v[i]);
            if (old_v[i] + old_v[i + 1] == n)
                v.push_back(n);
        }
        v.push_back(old_v[old_v.size() - 1]);
    }

    return 0;
}
