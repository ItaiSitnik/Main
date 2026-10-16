#include <algorithm>
#include <ctime>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

const int N = 4, N2 = N * N;

int shuf[N2];

bool numInRow(char board[][N2], int num, int row) {
    for (int i = 0; i < N2; i++)
        if (board[row][i] == num) return true;
    return false;
}

bool numInCol(char board[][N2], int num, int col) {
    for (int i = 0; i < N2; i++)
        if (board[i][col] == num) return true;
    return false;
}

bool numInBox(char board[][N2], int num, int row, int col) {
    int boxRow = row - row % N;
    int boxCol = col - col % N;

    for (int i = boxRow; i < boxRow + N; i++)
        for (int j = boxCol; j < boxCol + N; j++)
            if (board[i][j] == num) return true;
    return false;
}

bool validPlace(char board[][N2], int num, int row, int col) {
    return !numInRow(board, num, row) &&
           !numInCol(board, num, col) &&
           !numInBox(board, num, row, col);
}

bool solve(char board[][N2]) {
    for (int i = 0; i < N2; i++)
        for (int j = 0; j < N2; j++)
            if (board[i][j] == 0) {
                for (int k = 0; k < N2; k++) {
                    int num = shuf[k];
                    if (validPlace(board, num, i, j)) {
                        board[i][j] = num;
                        if (solve(board))
                            return true;
                        else
                            board[i][j] = 0;
                    }
                }
                return false;
            }
    return true;
}

void printBoard(char board[][N2]) {
    for (int i = 0; i < N2; i++) {
        for (int j = 0; j < N2; j++) {
            string out = board[i][j] ? to_string(board[i][j]) : "*";
            if (board[i][j] < 10) out += " ";
            cout << out << " ";
            if (j % N == N - 1 && j != N2 - 1) cout << "| ";
        }
        cout << "\n";
        if (i % N == N - 1 && i != N2 - 1) {
            for (int k = 0; k < 3 * N2 + 2 * (N - 1) - 1; k++)
                cout << "-";
            cout << "\n";
        }
    }
    cout << "\n";
}

bool conflicted(char board[][N2]) {
    for (int i = 0; i < N2; i++)
        for (int j = 0; j < N2; j++) {
            int num = board[i][j];
            if (!num) continue;
            board[i][j] = 0;
            if (!validPlace(board, num, i, j))
                return true;
            board[i][j] = num;
        }
    return false;
}

int main() {
    char board[N2][N2];

    int tries = 0;

    do {
        srand(time(NULL));
        for (int i = 0; i < N2; i++)
            for (int j = 0; j < N2; j++)
                board[i][j] = 0;
        for (int i = 0; i < 16; i++)
            board[rand() % N2][rand() % N2] = rand() % N2 + 1;
        tries++;
    } while (conflicted(board));

    cout << "Generated (in " << tries << " tries):" << endl;

    printBoard(board);

    for (int i = 0; i < N2; i++) shuf[i] = i + 1;
    for (int i = 0; i < 1000; i++) {
        int q = rand() % N2, p = rand() % N2, t = shuf[q];
        shuf[q] = shuf[p];
        shuf[p] = t;
    }

    string out = solve(board) ? "Solved:" : "Cannot be solved:";
    cout << out << endl;

    printBoard(board);

    return 0;
}
