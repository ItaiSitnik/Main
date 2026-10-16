#include <stdio.h>

class CPoint {
    int x, y;

   public:
    CPoint(int ax, int ay) {
        x = ax;
        y = ay;
    }
    ~CPoint() {
        printf("CPoint destructor was called %d, %d\n", x, y);
    }
};

CPoint dummyl(CPoint& pnt) { return pnt; }
void dummy2(CPoint pnt) {}
void dummy3(const CPoint& pnt) {}

int main() {
    const CPoint p1(10, 10);
    // dummyl(p1);
    dummy2(p1);
    dummy3(p1);
    CPoint p2(20, 20);
    dummyl(p2);
    dummy2(p2);
    dummy3(p2);
    p2 = p1;
    CPoint p3 = p2;
    return 0;
}
