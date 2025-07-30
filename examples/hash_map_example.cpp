#include <iostream>
#include <string>
#include <bernoulli/hash_map.hpp>
#include <bernoulli/observed_map.hpp>

// Custom decoder that maps hash values to colors
struct color_decoder {
    using value_type = std::string;
    
    std::string operator()(std::uint64_t hash) const {
        const std::vector<std::string> colors = {
            "red", "green", "blue", "yellow", 
            "orange", "purple", "black", "white"
        };
        return colors[hash % colors.size()];
    }
};

int main() {
    // Example 1: Simple hash_map with boolean decoder
    {
        std::cout << "Example 1: Boolean hash_map\n";
        
        bernoulli::simple_hash h;
        bernoulli::simple_decoder<bool> d;
        
        // Create hash_map with seed 42 and 10% error rate
        auto bool_map = bernoulli::make_hash_map(h, d, 42, 0.1);
        
        // Test some inputs
        std::vector<std::string> inputs = {"cat", "dog", "bird", "fish"};
        for (const auto& input : inputs) {
            std::cout << "  " << input << " -> " 
                      << (bool_map(input) ? "true" : "false") << "\n";
        }
        std::cout << "  Error rate: " << bool_map.error_rate() << "\n\n";
    }
    
    // Example 2: Hash_map with custom color decoder
    {
        std::cout << "Example 2: Color hash_map\n";
        
        bernoulli::simple_hash h;
        color_decoder d;
        
        // Create hash_map that maps strings to colors
        auto color_map = bernoulli::make_hash_map(h, d, 12345, 0.15);
        
        // Test some inputs
        std::vector<std::string> animals = {"cat", "dog", "bird", "fish", "rabbit"};
        for (const auto& animal : animals) {
            std::cout << "  " << animal << " -> " << color_map(animal) << "\n";
        }
        std::cout << "  Error rate: " << color_map.error_rate() << "\n\n";
    }
    
    // Example 3: Using type-erased observed_map
    {
        std::cout << "Example 3: Type-erased observed_map\n";
        
        bernoulli::simple_hash h;
        color_decoder d;
        auto color_map = bernoulli::make_hash_map(h, d, 54321, 0.05);
        
        // Wrap in observed_map for type erasure
        bernoulli::observed_map<std::string, std::string> obs_map(color_map);
        
        // Can now store different map implementations in same container
        std::vector<std::string> fruits = {"apple", "banana", "cherry"};
        for (const auto& fruit : fruits) {
            std::cout << "  " << fruit << " -> " << obs_map(fruit) << "\n";
        }
        std::cout << "  Average error rate: " << obs_map.error_rate() << "\n";
    }
    
    return 0;
}