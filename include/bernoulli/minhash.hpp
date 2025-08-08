#pragma once

#include <vector>
#include <functional>
#include <cstddef>
#include <limits>
#include <algorithm>

namespace bernoulli {

// Simple MinHash signature for sets of hashable elements.
template <typename T, typename Hash = std::hash<T>>
class minhash
{
public:
    using value_type = T;

    explicit minhash(std::size_t signature_size, Hash h = {})
        : k_(signature_size), sig_(signature_size, std::numeric_limits<std::size_t>::max()), hash_(h) {}

    template <typename Iter>
    void add_all(Iter first, Iter last) {
        for (auto it = first; it != last; ++it) add(*it);
    }

    void add(T const& x) {
        const std::size_t hx = hash_(x);
        for (std::size_t i = 0; i < k_; ++i) {
            const std::size_t mixed = hx ^ salt(i);
            sig_[i] = std::min(sig_[i], mixed);
        }
        n_++;
    }

    // Jaccard similarity estimator is fraction of equal components.
    static double jaccard_estimate(minhash const& a, minhash const& b) {
        const std::size_t k = std::min(a.k_, b.k_);
        std::size_t eq = 0;
        for (std::size_t i = 0; i < k; ++i) eq += (a.sig_[i] == b.sig_[i]);
        return k ? static_cast<double>(eq) / static_cast<double>(k) : 0.0;
    }

    std::size_t size() const { return k_; }

private:
    static std::size_t salt(std::size_t i) { return 0x517cc1b727220a95ull ^ (i + (i << 6) + (i >> 2)); }

    std::size_t k_{};
    std::vector<std::size_t> sig_;
    Hash hash_{};
    std::size_t n_{};
};

} // namespace bernoulli

