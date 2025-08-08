#pragma once

#include <vector>
#include <functional>
#include <cmath>
#include <cstddef>
#include <iterator>
#include <limits>
#include <type_traits>

#include <bernoulli/rate_span.hpp>

namespace bernoulli {

// Simple salt table for double-hashing
static inline std::size_t bloom_salt(std::size_t index) {
    static constexpr std::size_t salts[] = {
        0x8CA63C47u, 0x42CC2884u, 0x8E89919Bu, 0x6EDBD7D3u,
        0x15B6796Cu, 0x1D6FDFE4u, 0x63FF9092u, 0xE7401432u,
        0xEFFE9412u, 0xAEAEDF79u, 0x9F245A31u, 0x83C136FCu,
        0xC3DA4A8Cu, 0xA5112C8Cu, 0x5271F491u, 0x9A948DABu,
    };
    constexpr std::size_t n = sizeof(salts) / sizeof(salts[0]);
    return salts[index % n] ^ index;
}

template <typename T, typename H = std::hash<T>>
class bloom_filter
{
public:
    using value_type = T;

    bloom_filter(std::size_t m_bits, std::size_t k_hashes, H h = {})
        : bits_(m_bits, false), k_(k_hashes), n_(0), hash_(h) {}

    template <typename Iter>
    bloom_filter(Iter first, Iter last, std::size_t m_bits, std::size_t k_hashes, H h = {})
        : bloom_filter(m_bits, k_hashes, h)
    {
        for (auto it = first; it != last; ++it) insert(*it);
    }

    void insert(T const& x) {
        const std::size_t hx = hash_(x);
        for (std::size_t s = 0; s < k_; ++s) {
            const std::size_t idx = (bloom_salt(s) ^ hx) % m();
            bits_[idx] = true;
        }
        ++n_;
    }

    bool contains(T const& x) const {
        const std::size_t hx = hash_(x);
        for (std::size_t s = 0; s < k_; ++s) {
            const std::size_t idx = (bloom_salt(s) ^ hx) % m();
            if (!bits_[idx]) return false;
        }
        return true;
    }

    // Approximate false positive rate: (1 - e^{-k n / m})^k
    rate_span false_positive_rate() const {
        if (m() == 0) return rate_span(0.0f);
        const double one_minus = std::exp(-static_cast<double>(k_) * static_cast<double>(n_) / static_cast<double>(m()));
        const double p = std::pow(1.0 - one_minus, static_cast<double>(k_));
        return rate_span(static_cast<float>(p));
    }

    // Standard Bloom filters have no false negatives under normal operation
    rate_span false_negative_rate() const { return rate_span(0.0f); }

    std::size_t m() const { return bits_.size(); }
    std::size_t k() const { return k_; }
    std::size_t n() const { return n_; }

private:
    std::vector<bool> bits_;
    std::size_t k_;
    std::size_t n_;
    H hash_;
};

// Builder helpers
namespace detail {
    inline std::pair<std::size_t, std::size_t> bloom_params(std::size_t n, double target_fpr) {
        if (n == 0) return {0, 0};
        const double m = std::ceil(-(static_cast<double>(n) * std::log(target_fpr)) / (std::log(2.0) * std::log(2.0)));
        const double k = std::round((m / static_cast<double>(n)) * std::log(2.0));
        return {static_cast<std::size_t>(m), static_cast<std::size_t>(k)};
    }
}

template <typename Iter, typename H = std::hash<typename std::iterator_traits<Iter>::value_type>>
auto make_bloom_filter_fpr(Iter first, Iter last, double target_fpr, H h = H{})
{
    using TVal = typename std::iterator_traits<Iter>::value_type;
    const std::size_t n = static_cast<std::size_t>(std::distance(first, last));
    const auto [m, k] = detail::bloom_params(n, target_fpr);
    return bloom_filter<TVal, H>(first, last, m, std::max<std::size_t>(1, k), h);
}

} // namespace bernoulli

