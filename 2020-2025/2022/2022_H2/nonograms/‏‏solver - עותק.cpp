#include <algorithm>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <memory>
#include <random>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

bool equals(vector<int> a, vector<int> b) {
    if (a.size() != b.size()) return false;
    for (int i = 0; i < (int)a.size(); i++)
        if (a[i] != b[i]) return false;
    return true;
}

struct Game {
    int dimension;
    vector<vector<int>> matrix, lines, columns;

    Game(int _dimension) {
        this->dimension = _dimension;

        matrix.resize(dimension);
        for (auto row : matrix)
            row.resize(dimension, -1);

        lines.resize(dimension);
        columns.resize(dimension);
    }

    void showMatrix() {
        cout << "Resulting grid is: " << endl;
        for (int i = 0; i < dimension; i++) {
            for (int j = 0; j < dimension; j++) {
                if (j != 0)
                    cout << " ";
                cout << ((matrix[i][j] == 1) ? 'X' : ' ');
            }
            cout << endl;
        }
    }

    bool updateLine(int idx) {
        int newVal, pos;
        bool hasChanged = false, go;

        vector<int> aux;
        vector<vector<int>> auxLines;

        for (int i = 1; i < (1 << dimension); i++) {
            go = true;
            aux.clear();
            for (int j = 0; j < dimension; j++) {
                if ((i & (1 << j)) != 0)
                    newVal = 1;
                else
                    newVal = 0;

                if (matrix[idx][j] != -1 && matrix[idx][j] != newVal) go = false;
                aux.push_back(newVal);
            }
            if (go) auxLines.push_back(aux);
        }

        for (int i = auxLines.size() - 1; i >= 0; i--) {
            aux.clear();
            newVal = pos = 0;
            while (pos < dimension) {
                if (auxLines[i][pos] == 0) {
                    if (newVal != 0) aux.push_back(newVal), newVal = 0;
                } else
                    newVal++;
                pos++;
            }
            if (newVal != 0) aux.push_back(newVal);
            if (!equals(aux, lines[idx])) auxLines.erase(auxLines.begin() + i);
        }

        if (auxLines.size() > 0) {
            for (int j = 0; j < dimension; j++) {
                if (matrix[idx][j] != -1) continue;
                go = true;
                newVal = auxLines[0][j];
                for (int i = 1; i < (int)auxLines.size(); i++) {
                    if (newVal != auxLines[i][j])
                        go = false;
                }
                if (go)
                    matrix[idx][j] = newVal, hasChanged = true;
            }
        }

        return hasChanged;
    }

    bool updateColumn(int idx) {
        int newVal, pos;
        bool hasChanged = false, go;

        vector<int> aux;
        vector<vector<int>> auxLines;

        for (int i = 1; i < (1 << dimension); i++) {
            go = true;
            aux.clear();
            for (int j = 0; j < dimension; j++) {
                if ((i & (1 << j)) != 0)
                    newVal = 1;
                else
                    newVal = 0;

                if (matrix[j][idx] != -1 && matrix[j][idx] != newVal) go = false;
                aux.push_back(newVal);
            }
            if (go) auxLines.push_back(aux);
        }

        for (int i = auxLines.size() - 1; i >= 0; i--) {
            aux.clear();
            newVal = pos = 0;
            while (pos < dimension) {
                if (auxLines[i][pos] == 0) {
                    if (newVal != 0) aux.push_back(newVal), newVal = 0;
                } else
                    newVal++;
                pos++;
            }
            if (newVal != 0) aux.push_back(newVal);
            if (!equals(aux, columns[idx])) auxLines.erase(auxLines.begin() + i);
        }

        if (auxLines.size() > 0) {
            for (int j = 0; j < dimension; j++) {
                if (matrix[j][idx] != -1) continue;
                go = true;
                newVal = auxLines[0][j];
                for (int i = 1; i < (int)auxLines.size(); i++) {
                    if (newVal != auxLines[i][j])
                        go = false;
                }
                if (go)
                    matrix[j][idx] = newVal, hasChanged = true;
            }
        }

        return hasChanged;
    }

    void solve() {
        bool finished = false;
        while (!finished) {
            finished = true;
            for (int i = 0; i < dimension; i++) {
                if (updateLine(i)) finished = false;
                if (updateColumn(i)) finished = false;
            }
        }
    }
};

vector<int> stoiVec(string in) {
    string word = "";
    vector<int> out;
    for (auto x : in)
        if (x == ' ') {
            out.push_back(stoi(word));
            word = "";
        } else
            word = word + x;
    out.push_back(stoi(word));
    return out;
}

Game readInput() {
    std::ifstream infile("samples/inputs/guntz.txt");

    string line;
    getline(infile, line);
    int dimension = stoi(line);

    Game game = Game(dimension);

    // reading lines
    for (int i = 0; i < dimension; i++) {
        getline(infile, line);
        game.lines[i] = stoiVec(line);
    }

    // reading columns
    for (int i = 0; i < dimension; i++) {
        getline(infile, line);
        game.columns[i] = stoiVec(line);
    }
    return game;
}

int main() {
    cout << "BEGIN\n";
    Game game = readInput();
    cout << "HERE1\n";
    game.solve();
    cout << "HERE2\n";
    game.showMatrix();
    cout << "DONE\n";
    return 0;
}
