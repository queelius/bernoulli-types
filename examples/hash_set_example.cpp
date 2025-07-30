#include <iostream>
#include <vector>
#include <string>
#include <bernoulli/hash_set.hpp>
#include <bernoulli/hash_set_builder.hpp>
#include <bernoulli/observed_set.hpp>

int main() {
    // Example 1: Build a hash_set from a collection of strings
    std::vector<std::string> words = {"apple", "banana", "cherry", "date", "elderberry"};
    
    try {
        // Build hash_set with 1% false positive rate
        auto hash_set = bernoulli::hash_set_builder<>()
            .false_positive_rate(0.01)
            .max_attempts(10000)
            .build(words);
        
        std::cout << "Built hash_set with:\n";
        std::cout << "  False positive rate: " << hash_set.false_positive_rate() << "\n";
        std::cout << "  False negative rate: " << hash_set.false_negative_rate() << "\n";
        std::cout << "  Threshold: " << hash_set.threshold() << "\n";
        std::cout << "  Seed: " << hash_set.index() << "\n\n";
        
        // Test membership
        std::cout << "Membership tests:\n";
        for (const auto& word : words) {
            std::cout << "  " << word << ": " 
                      << (hash_set.contains(word) ? "present" : "absent") << "\n";
        }
        
        // Test non-members
        std::vector<std::string> non_members = {"fig", "grape", "kiwi"};
        std::cout << "\nNon-member tests:\n";
        for (const auto& word : non_members) {
            std::cout << "  " << word << ": " 
                      << (hash_set.contains(word) ? "present (false positive)" : "absent") << "\n";
        }
        
        // Example 2: Use type-erased observed_set
        std::cout << "\nUsing type-erased observed_set:\n";
        bernoulli::observed_set<std::string> obs_set(hash_set);
        
        // Can now store in containers, pass to functions expecting observed_set, etc.
        std::cout << "apple in observed_set: " 
                  << (obs_set.contains("apple") ? "yes" : "no") << "\n";
        std::cout << "grape in observed_set: " 
                  << (obs_set.contains("grape") ? "yes" : "no") << "\n";
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
    
    return 0;
}