#include <fstream>
#include <iostream>
#include <string>
#include <variant>

#include "json.hpp"

using namespace std;

// A variant type to store string, int, or double
using Value = variant<string, int, double>;

// Alias for the nlohmann::json library
using json = nlohmann::json;

// Database class to store and fetch values
class Database {
    map<string, Value> data;

   public:
    void loadFromFile(const string& filename) {
        ifstream file(filename);
        if (!file) {
            cerr << "Unable to open file: " << filename << endl;
            return;
        }

        json jsonData;
        file >> jsonData;

        for (auto& [key, val] : jsonData.items()) {
            // Determine the value type (int, double, or string) and store it in the map
            if (val.is_number_integer())
                data[key] = val.get<int>();
            else if (val.is_number_float())
                data[key] = val.get<double>();
            else if (val.is_string())
                data[key] = val.get<string>();
        }

        file.close();
    }

    // Function to fetch the value by key
    void fetch(const string& key) {
        if (data.find(key) != data.end()) {
            const Value& val = data[key];

            // Check the type of value and print accordingly
            if (holds_alternative<int>(val))
                cout << key << ": " << get<int>(val) << " (int)" << endl;
            else if (holds_alternative<double>(val))
                cout << key << ": " << get<double>(val) << " (double)" << endl;
            else if (holds_alternative<string>(val))
                cout << key << ": " << get<string>(val) << " (string)" << endl;

        } else
            cout << "Key \"" << key << "\" not found." << endl;
    }
};

int main() {
    Database db;

    // Load the data from the JSON file
    db.loadFromFile("../random_data.json");

    // Fetch values by their keys
    db.fetch("one");
    db.fetch("fifty");
    db.fetch("ninety-nine");

    return 0;
}
