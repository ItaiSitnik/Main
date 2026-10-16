#include <omp.h>

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <set>
#include <string>
#include <vector>

using namespace std;

// Convert a grid to a string representation
string grid_to_string(const vector<vector<int>>& grid) {
    string result;
    for (const auto& row : grid) {
        for (const auto& cell : row) {
            result += (cell ? "🟦" : "⬜");
        }
        result += "\n";
    }
    return result;
}

// Generate all rotations and reflections of an n x n grid
vector<vector<vector<int>>> generate_rotations_and_reflections(const vector<vector<int>>& grid) {
    vector<vector<vector<int>>> grids;
    auto rotated = grid;
    int size = grid.size();

    // Rotations
    for (int i = 0; i < 4; ++i) {
        grids.push_back(rotated);

        // Rotate 90 degrees clockwise
        vector<vector<int>> temp(size, vector<int>(size));
        for (int r = 0; r < size; ++r) {
            for (int c = 0; c < size; ++c) {
                temp[c][size - 1 - r] = rotated[r][c];
            }
        }
        rotated = temp;
    }

    // Horizontal reflection
    vector<vector<int>> horizontal_reflection(size, vector<int>(size));
    for (int r = 0; r < size; ++r) {
        horizontal_reflection[r] = vector<int>(rotated[r].rbegin(), rotated[r].rend());
    }
    grids.push_back(horizontal_reflection);

    // Vertical reflection
    vector<vector<int>> vertical_reflection = rotated;
    reverse(vertical_reflection.begin(), vertical_reflection.end());
    grids.push_back(vertical_reflection);

    return grids;
}

// Check if a grid is unique among the given unique grids
bool is_unique(const vector<vector<int>>& grid, const vector<vector<vector<int>>>& unique_grids) {
    for (const auto& unique : unique_grids) {
        auto transformations = generate_rotations_and_reflections(unique);
        if (find(transformations.begin(), transformations.end(), grid) != transformations.end()) {
            return false;
        }
    }
    return true;
}

// Count unique seating arrangements for 0 to n^2 people in an n x n grid
vector<vector<vector<vector<int>>>> count_unique_arrangements(int n) {
    vector<vector<vector<vector<int>>>> results(n * n + 1);
    int total_seats = n * n;

#pragma omp parallel for schedule(dynamic)
    for (int num_people = 0; num_people <= total_seats; ++num_people) {
        vector<vector<vector<int>>> unique_grids;

        // Generate all combinations of positions
        vector<bool> mask(total_seats, false);
        fill(mask.begin(), mask.begin() + num_people, true);
        do {
            vector<vector<int>> grid(n, vector<int>(n, 0));
            for (int i = 0; i < total_seats; ++i) {
                if (mask[i]) {
                    grid[i / n][i % n] = 1;
                }
            }

#pragma omp critical
            {
                if (is_unique(grid, unique_grids)) {
                    unique_grids.push_back(grid);
                }
            }
        } while (prev_permutation(mask.begin(), mask.end()));

#pragma omp critical
        results[num_people] = unique_grids;
    }
    return results;
}

// Display results
void display_results(const vector<vector<vector<vector<int>>>>& results, bool only_counts) {
    for (int num_people = 0; num_people < results.size(); ++num_people) {
        const auto& grids = results[num_people];
        if (only_counts) {
            cout << "Number of people: " << num_people
                 << ", Unique arrangements: " << grids.size() << endl;
        } else {
            cout << "Number of people: " << num_people << endl;
            for (const auto& grid : grids) {
                cout << grid_to_string(grid) << endl;
            }
        }
    }
}

int main() {
    bool only_counts = true;
    for (int n = 1; n <= 10; ++n) {
        cout << "> n = " << n << endl;
        auto results = count_unique_arrangements(n);
        display_results(results, only_counts);
        cout << "\n";
    }
    return 0;
}
