#pragma once

#include <cmath>
#include <limits>
#include <cstdint>
#include <functional>

namespace bernoulli {

/**
 * @brief Simple decoder that extracts a value from a hash
 * 
 * This is a placeholder - in practice you'd use more sophisticated
 * encoding/decoding schemes.
 */
template <typename T>
struct simple_decoder {
    using value_type = T;
    
    T operator()(std::uint64_t hash) const {
        // This is a very simple example - just cast the hash
        // In practice, you'd have proper encoding/decoding
        return static_cast<T>(hash);
    }
};

// Specialization for bool
template <>
struct simple_decoder<bool> {
    using value_type = bool;
    
    bool operator()(std::uint64_t hash) const {
        return (hash & 1) != 0;
    }
};

/**
 * @brief Concrete implementation of an observed/Bernoulli map using hashing
 *
 * This models a latent function f: X -> Y through an observed function ~f
 * where the outputs may have errors.
 * 
 * The implementation uses:
 * - A hash function H to map inputs to hash values
 * - A decoder D to extract values of type Y from hash values
 * 
 * @tparam H Hash function type
 * @tparam D Decoder type that extracts values from hashes
 */
template <typename H, typename D>
class hash_map {
public:
    using hash_fn_type = H;
    using decoder_type = D;
    using hash_type = typename H::hash_type;
    using codomain_type = typename D::value_type;
    
    hash_map(H h, D d, std::size_t l, double err)
        : h_(h), d_(d), l_(l), err_(err) {}
    
    /**
     * Apply the observed function ~f to input x
     * Returns d(h.mix(h(x), l))
     */
    template <typename X>
    codomain_type operator()(const X& x) const {
        return d_(h_.mix(h_(x), l_));
    }
    
    /**
     * Get the average error rate
     */
    double error_rate() const { 
        return err_; 
    }
    
    /**
     * Get the error rate for a specific input
     * (In this simple implementation, it's uniform)
     */
    template <typename X>
    double error_rate(const X&) const { 
        return err_; 
    }
    
    // Getters for inspection
    H hash_fn() const { return h_; }
    D decoder_fn() const { return d_; }
    std::size_t seed() const { return l_; }
    
private:
    H h_;        // Hash function
    D d_;        // Decoder function
    std::size_t l_;  // Seed/mixing parameter
    double err_;     // Error rate
};

/**
 * @brief Convenience factory function for hash_map
 */
template <typename H, typename D>
hash_map<H, D> make_hash_map(H h, D d, std::size_t seed, double error_rate) {
    return hash_map<H, D>(h, d, seed, error_rate);
}

} // namespace bernoulli