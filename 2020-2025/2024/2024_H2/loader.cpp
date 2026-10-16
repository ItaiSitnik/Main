#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <variant>

using namespace std;

// A variant type to store string, int, or double
using Value = variant<string, int, double>;

// Function to remove extra spaces and quotes from strings
string trim(const string& str) {
    size_t first = str.find_first_not_of(" \t\n\r\"");
    size_t last = str.find_last_not_of(" \t\n\r\"");
    return str.substr(first, (last - first + 1));
}

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

        string line, key, value;
        while (getline(file, line)) {
            if (line.find(':') != string::npos) {
                istringstream ss(line);
                getline(ss, key, ':');
                getline(ss, value, ',');

                key = trim(key);
                value = trim(value);

                // Determine the value type (int, double, or string)
                if (value.find_first_not_of("0123456789") == string::npos)  // Integer
                    data[key] = stoi(value);
                else if (value.find_first_of('.') != string::npos)  // Double
                    data[key] = stod(value);
                else  // String
                    data[key] = value;
            }
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
