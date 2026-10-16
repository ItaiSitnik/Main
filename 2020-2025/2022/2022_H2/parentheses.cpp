#include <iostream>
#include <string>
#include <vector>

using namespace std;

void getParentheses(int n, int opened, int closed, string curr, vector<string>& out) {
    if (opened == n && closed == n) {
        out.push_back(curr);
        return;
    }
    if (opened < n)
        getParentheses(n, opened + 1, closed, curr + "(", out);
    if (closed < opened)
        getParentheses(n, opened, closed + 1, curr + ")", out);
}

vector<string> getParentheses(int n) {
    vector<string> out;
    getParentheses(n, 0, 0, "", out);
    return out;
}

int main() {
    int n = 4;
    vector<string> x = getParentheses(n);
    for (auto s : x)
        cout << s << '\n';
    cout << x.size() << '\n';
}
