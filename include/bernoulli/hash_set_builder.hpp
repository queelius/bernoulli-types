#pragma once

#include <bernoulli/hash_set.hpp>
#include <algorithm>
#include <vector>
#include <random>
#include <stdexcept>
#include <cmath>

namespace bernoulli {

/**
 * @brief Builder for constructing hash_set instances
 * 
 * This builder finds a suitable seed value l0 such that all elements
 * in the input set hash to values below the threshold N, which is
 * determined by the desired false positive rate.
 * 
 * Usage:
 *   auto observed_set = hash_set_builder<>()
 *       .false_positive_rate(0.01)
 *       .max_attempts(1000)
 *       .build(elements);
 * 
 * @tparam H Hash function type
 */
template <typename H = simple_hash>
class hash_set_builder {
public:
    hash_set_builder() 
        : fpr_(0.01), max_attempts_(10000), rng_(std::random_device{}()) {}
    
    /**
     * Set desired false positive rate (default: 0.01)
     */
    hash_set_builder& false_positive_rate(double fpr) {
        if (fpr <= 0.0 || fpr >= 1.0) {
            throw std::invalid_argument("False positive rate must be in (0, 1)");
        }
        fpr_ = fpr;
        return *this;
    }
    
    /**
     * Set maximum attempts to find a suitable seed (default: 10000)
     */
    hash_set_builder& max_attempts(std::size_t attempts) {
        max_attempts_ = attempts;
        return *this;
    }
    
    /**
     * Set random seed for reproducibility
     */
    hash_set_builder& seed(std::size_t s) {
        rng_.seed(s);
        return *this;
    }
    
    /**
     * Build a hash_set from the given elements
     * 
     * @param elements Container of elements to include in the set
     * @return hash_set instance configured for the given elements
     * @throws std::runtime_error if no suitable seed is found
     */
    template <typename Container>
    hash_set<H> build(const Container& elements) {
        if (elements.empty()) {
            return hash_set<H>(0, H{}, 0, 0.0);
        }
        
        // Calculate threshold N from false positive rate
        const auto N = static_cast<std::size_t>(fpr_ * H::max());
        
        // Try to find a seed where all elements hash below N
        std::uniform_int_distribution<std::size_t> dist(0, H::max());
        
        for (std::size_t attempt = 0; attempt < max_attempts_; ++attempt) {
            const auto l0 = dist(rng_);
            H h;
            
            bool all_below_threshold = true;
            for (const auto& x : elements) {
                if (h.mix(l0, x) > N) {
                    all_below_threshold = false;
                    break;
                }
            }
            
            if (all_below_threshold) {
                // Success! All elements hash below threshold with this seed
                return hash_set<H>(N, h, l0, 0.0); // 0 false negative rate
            }
        }
        
        // Could not find perfect seed, return best effort with some false negatives
        // In practice, you might want to implement a more sophisticated strategy
        throw std::runtime_error("Could not find suitable hash seed after " + 
                                 std::to_string(max_attempts_) + " attempts");
    }
    
    /**
     * Alternative build method that accepts iterators
     */
    template <typename Iterator>
    hash_set<H> build(Iterator begin, Iterator end) {
        std::vector<typename std::iterator_traits<Iterator>::value_type> elements(begin, end);
        return build(elements);
    }
    
private:
    double fpr_;
    std::size_t max_attempts_;
    std::mt19937_64 rng_;
};

} // namespace bernoulli