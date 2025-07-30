#pragma once

#include <cmath>
#include <limits>
#include <cstdint>
#include <functional>

namespace bernoulli {

/**
 * @brief Simple FNV-1a hash function for demonstration
 * 
 * In production, you would use a more sophisticated hash function
 * or allow users to provide their own.
 */
struct simple_hash {
    using hash_type = std::uint64_t;
    
    template <typename T>
    hash_type operator()(const T& x) const {
        return std::hash<T>{}(x);
    }
    
    hash_type mix(hash_type seed, hash_type value) const {
        // Simple mixing function
        return seed ^ (value + 0x9e3779b9 + (seed << 6) + (seed >> 2));
    }
    
    template <typename T>
    hash_type mix(hash_type seed, const T& x) const {
        return mix(seed, operator()(x));
    }
    
    static constexpr hash_type max() {
        return std::numeric_limits<hash_type>::max();
    }
};

/**
 * @brief Concrete implementation of an observed/Bernoulli set using hashing
 *
 * This models a latent set S through an observed set ~S where:
 * - Elements are tested using a hash function
 * - False positives occur when hash collisions happen
 * - False negatives can be controlled during construction
 * 
 * The implementation uses the "hash set" construction where:
 * - We find a seed l0 such that all elements hash below threshold N
 * - Membership test: h.mix(l0, x) <= N
 * 
 * @tparam H Hash function type (default: simple_hash)
 */
template <typename H = simple_hash>
class hash_set {
public:
    using hash_fn_type = H;
    using hash_type = typename H::hash_type;
    using value_type = void; // Sets don't have a specific value type
    
    hash_set(std::size_t N, H h, std::size_t l0, double fnr)
        : N_(N), h_(h), l0_(l0), fnr_(fnr) {}
    
    /**
     * Test if element x is in the observed set ~S
     */
    template <typename X>
    bool contains(const X& x) const {
        return h_.mix(l0_, x) <= N_;
    }
    
    /**
     * False positive rate α = P(x ∈ ~S | x ∉ S)
     */
    double false_positive_rate() const {
        return static_cast<double>(N_) / H::max();
    }
    
    /**
     * False negative rate β = P(x ∉ ~S | x ∈ S)  
     */
    double false_negative_rate() const {
        return fnr_;
    }
    
    // Getters for inspection
    H hash_fn() const { return h_; }
    std::size_t index() const { return l0_; }
    std::size_t threshold() const { return N_; }
    
private:
    std::size_t N_;   // Threshold value
    H h_;             // Hash function
    std::size_t l0_;  // Seed/index
    double fnr_;      // False negative rate
};

} // namespace bernoulli