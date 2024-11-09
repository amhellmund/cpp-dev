#include <filesystem>
#include <iostream>

int main () {
    std::filesystem::path p {"abc"};
    std::cout << p << "\n";
    return 0;
}