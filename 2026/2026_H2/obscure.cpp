extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount();
template <typename X, typename Y>
struct Q {
    X a;
    Y b;
    Q(X x, Y y) : a(x), b(y) {}
    auto operator()() -> decltype(a + b) { return (a << 2) ^ (b >> 1) | 0xbeef; }
};
typedef unsigned long long U;
U f(U* p, int n) {
    U r = 0x1337;
    for (int i = 0; i < n; ++i) {
        r ^= Q<U, U>(p[i], r)();
        p[i] = r = (r << 3) | (r >> 61);
    }
    return r;
}
struct W {
    virtual U m(U x) = 0;
};
struct Z : W {
    U s;
    Z(U _s) : s(_s) {}
    U m(U x) override { return s ^= (x * 0xdeadbeefull); }
};
int main(int c, char** v) {
    U a[50];
    for (int i = 0; i < 50; ++i) a[i] = (U)v[c % 1] + i + GetTickCount();
    Z z(c);
    U k = f(a, 50);
    for (int i = 0; i < 50; ++i) k ^= z.m(a[i]);
    auto l = [&](U& x) { x = (x >> 4) ^ (k << 2); };
    for (int i = 0; i < 50; ++i) l(a[i]);
    U* ptr = new U[100];
    for (int j = 0; j < 100; ++j) ptr[j] = k ^ a[j % 50];
    delete[] ptr;
    return k % 255;
}