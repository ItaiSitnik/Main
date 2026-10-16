#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

#define INPUT_PATH "samples/inputs/guntz.txt"

struct Game {
    int dimension;
    vector<vector<int>> matrix, lines, columns;

    Game(int dimension) {
        this->dimension = dimension;

        matrix.resize(dimension);
        for (int i = 0; i < dimension; i++)
            matrix[i].resize(dimension, -1);

        lines.resize(dimension);
        columns.resize(dimension);
    }

    void print() {
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

    int& getMatrixSubject(int fixed, int running, bool isRow) {
        return isRow ? matrix[fixed][running] : matrix[running][fixed];
    }

    bool updateVector(int index, bool isRow) {
        int newVal, currVal;
        bool hasChanged = false, go;

        vector<int> aux;
        vector<vector<int>> auxLines;

        for (int i = 1; i < (1 << dimension); i++) {
            go = true;
            aux.clear();
            for (int j = 0; j < dimension; j++) {
                newVal = (i & (1 << j)) != 0;
                currVal = getMatrixSubject(index, j, isRow);
                if (currVal != -1 && currVal != newVal)
                    go = false;
                aux.push_back(newVal);
            }
            if (go)
                auxLines.push_back(aux);
        }

        for (int i = auxLines.size() - 1; i >= 0; i--) {
            aux.clear();
            newVal = 0;
            for (int pos = 0; pos < dimension; pos++)
                if (auxLines[i][pos] == 0) {
                    if (newVal != 0)
                        aux.push_back(newVal), newVal = 0;
                } else
                    newVal++;
            if (newVal != 0)
                aux.push_back(newVal);
            if (aux != (isRow ? lines[index] : columns[index]))
                auxLines.erase(auxLines.begin() + i);
        }

        if (auxLines.size() > 0)
            for (int j = 0; j < dimension; j++) {
                if (getMatrixSubject(index, j, isRow) != -1)
                    continue;
                go = true;
                newVal = auxLines[0][j];
                for (int i = 1; i < (int)auxLines.size(); i++)
                    if (newVal != auxLines[i][j])
                        go = false;
                if (go) {
                    getMatrixSubject(index, j, isRow) = newVal;
                    hasChanged = true;
                }
            }

        return hasChanged;
    }

    void solve() {
        bool finished = false;
        while (!finished) {
            finished = true;
            for (int i = 0; i < dimension; i++)
                if (updateVector(i, true) || updateVector(i, false))
                    finished = false;
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
    std::ifstream infile(INPUT_PATH);

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
    Game game = readInput();
    game.solve();
    game.print();
    return 0;
}
