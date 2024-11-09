#include <concepts>
#include <cstdint>
#include <iostream>
#include <ranges>
#include <vector>

template <std::ranges::range T> 
void print_positive (const T& data) {
    for (const auto& positive: data | std::views::filter([](const auto& value) { return value > 0;} ) ) {
        std::cout << positive << "\n"; 
    }
}

int main () {
    print_positive(std::vector<std::int32_t>{1, -2, 3, -4, 5});
}