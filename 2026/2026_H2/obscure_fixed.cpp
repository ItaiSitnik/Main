// Declaring the Windows API function GetTickCount directly without <windows.h>
// Returns the number of milliseconds since the system was started.
extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount();

typedef unsigned long long uint64;

// A functor (struct acting as a function) that mixes two values using bitwise operations
template <typename T1, typename T2>
struct BitMixer {
    T1 val1;
    T2 val2;

    BitMixer(T1 x, T2 y) : val1(x), val2(y) {}

    auto operator()() -> decltype(val1 + val2) {
        return ((val1 << 2) ^ (val2 >> 1)) | 0xBEEF;
    }
};

// Scrambles the array in-place and returns a combined hash-like state
uint64 scrambleArray(uint64* array, int size) {
    uint64 state = 0x1337;

    for (int i = 0; i < size; ++i) {
        BitMixer<uint64, uint64> mixer(array[i], state);
        state ^= mixer();

        // 64-bit Left Rotate (ROL) by 3 bits
        state = (state << 3) | (state >> 61);
        array[i] = state;
    }
    return state;
}

// Abstract base class (interface)
struct IHasher {
    virtual uint64 updateState(uint64 input) = 0;
};

// Concrete implementation that mutates an internal state using a magic constant
struct StatefulHasher : public IHasher {
    uint64 internalState;

    StatefulHasher(uint64 initialState) : internalState(initialState) {}

    uint64 updateState(uint64 input) override {
        internalState ^= (input * 0xDEADBEEFULL);
        return internalState;
    }
};

int main(int argc, char** argv) {
    uint64 data[50];

    // 1. Initialize the array with semi-random environment values:
    // Note: (argc % 1) is ALWAYS 0, so argv[argc % 1] is just argv[0] (the program's path pointer).
    // It casts the memory address of argv[0] to a 64-bit int, adds the loop index, and adds system uptime.
    for (int i = 0; i < 50; ++i) {
        data[i] = reinterpret_cast<uint64>(argv[0]) + i + GetTickCount();
    }

    StatefulHasher hasher(argc);

    // 2. First pass: scramble the array and get an initial key
    uint64 key = scrambleArray(data, 50);

    // 3. Second pass: mix the key further using the polymorphic hasher
    for (int i = 0; i < 50; ++i) {
        key ^= hasher.updateState(data[i]);
    }

    // 4. Third pass: a lambda function that modifies the array elements again (dead calculation)
    auto modifyElement = [&](uint64& element) {
        element = (element >> 4) ^ (key << 2);
    };

    for (int i = 0; i < 50; ++i) {
        modifyElement(data[i]);
    }

    // 5. Pointless dynamic memory allocation (Dead Store):
    // Allocates an array, fills it, and immediately deletes it without ever reading from it.
    uint64* tempBuffer = new uint64[100];
    for (int j = 0; j < 100; ++j) {
        tempBuffer[j] = key ^ data[j % 50];
    }
    delete[] tempBuffer;

    // 6. Return a value between 0 and 254 as the process exit code
    return key % 255;
}