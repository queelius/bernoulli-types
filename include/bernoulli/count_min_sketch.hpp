#pragma once

#include <vector>
#include <functional>
#include <cmath>
#include <cstddef>
#include <limits>

namespace bernoulli {

template <typename Key, typename Hash = std::hash<Key>>
class count_min_sketch
{
public:
    using key_type = Key;

    count_min_sketch(std::size_t width, std::size_t depth, Hash h = {})
        : w_(width), d_(depth), rows_(depth, std::vector<std::size_t>(width)), hash_(h) {}

    void update(Key const& x, std::size_t count = 1) {
        const std::size_t hx = hash_(x);
        for (std::size_t r = 0; r < d_; ++r) {
            const std::size_t idx = index(r, hx);
            rows_[r][idx] += count;
        }
        n_ += count;
    }

    std::size_t estimate(Key const& x) const {
        const std::size_t hx = hash_(x);
        std::size_t est = std::numeric_limits<std::size_t>::max();
        for (std::size_t r = 0; r < d_; ++r) {
            const std::size_t idx = index(r, hx);
            est = std::min(est, rows_[r][idx]);
        }
        return est == std::numeric_limits<std::size_t>::max() ? 0 : est;
    }

    // Typical CMS guarantees with w = ceil(e/eps), d = ceil(ln(1/delta))
    double epsilon() const { return w_ ? std::exp(1.0) / static_cast<double>(w_) : 1.0; }
    double one_minus_delta() const { return d_ ? 1.0 - std::exp(-static_cast<double>(d_)) : 0.0; }

    std::size_t width() const { return w_; }
    std::size_t depth() const { return d_; }
    std::size_t total() const { return n_; }

private:
    static std::size_t salt(std::size_t r) { return 0x9e3779b97f4a7c15ull ^ (r + (r << 6) + (r >> 2)); }
    std::size_t index(std::size_t r, std::size_t hx) const { return (hx ^ salt(r)) % w_; }

    std::size_t w_{};
    std::size_t d_{};
    std::vector<std::vector<std::size_t>> rows_;
    Hash hash_{};
    std::size_t n_{};
};

} // namespace bernoulli

