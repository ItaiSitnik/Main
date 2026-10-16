#include <iostream>
using namespace std;

class Point {
    int x;
    int y;

public:
    Point(int x, int y)
        : x(x)
        , y(y)
    {
    }

    ostream& print(ostream& os) const
    {
        return os << "X: " << x << " Y: " << y << "\n";
    }
};

ostream& operator<<(ostream& os, const Point& p)
{
    return p.print(os);
}

int main()
{
    Point p1(11, 21);
    Point p2(84, 58);

    cout << p1 << p2 << "\n";
}
