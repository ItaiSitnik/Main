#include <iostream>
#include <vector>

using namespace std;

template <class T>
class Matrix {
   private:
    int rows, cols;
    T** data;

   public:
    Matrix(int rows, int cols) : rows(rows), cols(cols) {
        data = new T*[rows];
        for (int i = 0; i < rows; i++)
            data[i] = new T[cols];

        for (int y = 0; y < rows; y++)
            for (int x = 0; x < cols; x++)
                data[y][x] = 0;
    }

    ~Matrix() {
        for (int i = 0; i < rows; i++)
            delete[] data[i];
        delete[] data;
    }

    T& operator()(int x, int y) {
        return data[y][x];
    }

    friend Matrix operator*(const Matrix& A, const Matrix& B) {
        if (A.cols != B.rows)
            throw runtime_error("Size Missmatch");
        Matrix C(A.rows, B.cols);
        for (int y = 0; y < C.rows; y++)
            for (int x = 0; x < C.cols; x++)
                for (int k = 0; k < A.cols; k++)
                    C(x, y) += (A.data[y][k] * B.data[k][x]);
        return C;
    }

    friend ostream& operator<<(ostream& os, const Matrix& matrix) {
        for (int y = 0; y < matrix.rows; y++) {
            os << (y == 0 ? "[[" : " [");
            for (int x = 0; x < matrix.cols; x++) {
                os << matrix.data[y][x];
                if (x != matrix.cols - 1)
                    os << ", ";
                else if (y != matrix.rows - 1)
                    os << "],\n";
                else
                    os << "]]\n";
            }
        }
        return os;
    }
};

int main() {
    cout << "hi\n";
    Matrix<int> a(3, 3), b(3, 3);
    for (int y = 0; y < 3; y++)
        for (int x = 0; x < 3; x++) {
            a(x, y) = y * 3 + x + 1;
            b(x, y) = y * 3 + x + 1 + 9;
        }
    cout << a;
    cout << b;
    Matrix<int> c = a * b;
    cout << c;
    cout << "end\n";
    return 0;
}
