#include <iostream>
#include <bernoulli/observed_bool.hpp>
#include <bernoulli/rate_span.hpp>

int main() {
    std::cout << "=== Bernoulli Types: Basic Usage ===" << std::endl;
    
    // Create observed booleans with different error rates
    observed_bool definitely_true(true, 0.0);     // No error
    observed_bool probably_true(true, 0.1);       // 10% error rate  
    observed_bool maybe_false(false, 0.3);        // 30% error rate
    
    std::cout << "\nObserved values:" << std::endl;
    std::cout << "definitely_true: " << definitely_true.value 
              << " (error: " << definitely_true.error.min << ")" << std::endl;
    std::cout << "probably_true: " << probably_true.value 
              << " (error: " << probably_true.error.min << ")" << std::endl;
    std::cout << "maybe_false: " << maybe_false.value
              << " (error: " << maybe_false.error.min << ")" << std::endl;
    
    // Logical operations propagate error
    std::cout << "\nLogical operations:" << std::endl;
    
    auto result1 = probably_true & maybe_false;
    std::cout << "probably_true AND maybe_false = " << result1.value
              << " (error: [" << result1.error.min << ", " << result1.error.max << "])" 
              << std::endl;
    
    auto result2 = probably_true | maybe_false;
    std::cout << "probably_true OR maybe_false = " << result2.value
              << " (error: [" << result2.error.min << ", " << result2.error.max << "])"
              << std::endl;
    
    auto result3 = ~probably_true;
    std::cout << "NOT probably_true = " << result3.value
              << " (error: [" << result3.error.min << ", " << result3.error.max << "])"
              << std::endl;
    
    // Rate span arithmetic
    std::cout << "\nRate span arithmetic:" << std::endl;
    rate_span r1(0.1, 0.3);
    rate_span r2(0.2, 0.4);
    
    auto sum = r1 + r2;
    std::cout << "[0.1, 0.3] + [0.2, 0.4] = [" 
              << sum.min << ", " << sum.max << "]" << std::endl;
    
    auto product = r1 * r2;
    std::cout << "[0.1, 0.3] * [0.2, 0.4] = ["
              << product.min << ", " << product.max << "]" << std::endl;
    
    return 0;
}