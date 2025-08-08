#include <iostream>
#include <string>
#include <vector>

#include <bernoulli/bloom_filter.hpp>
#include <bernoulli/observed_set.hpp>

// Adapter so bloom_filter<T> matches the observed_set backend concept
template <typename T>
struct bloom_filter_set_adapter
{
    bernoulli::bloom_filter<T> bf;

    explicit bloom_filter_set_adapter(bernoulli::bloom_filter<T> b) : bf(std::move(b)) {}

    bool contains(T const& x) const { return bf.contains(x); }
    bernoulli::rate_span false_positive_rate() const { return bf.false_positive_rate(); }
    bernoulli::rate_span false_negative_rate() const { return bf.false_negative_rate(); }
};

int main()
{
    std::vector<std::string> items = {"alpha", "beta", "gamma", "delta"};

    // Build Bloom filter targeting ~1% FPR
    auto bf = bernoulli::make_bloom_filter_fpr(items.begin(), items.end(), 0.01);

    // Wrap as observed_set backend
    bloom_filter_set_adapter<std::string> backend{std::move(bf)};
    observed_set<std::string> S{backend};

    std::cout << std::boolalpha;
    std::cout << "contains('alpha'): " << S.contains("alpha") << "\n";
    std::cout << "contains('omega'): " << S.contains("omega") << "\n";

    auto fpr = S.false_positive_rate();
    auto fnr = S.false_negative_rate();
    std::cout << "FPR in [" << fpr.min << ", " << fpr.max << "]\n";
    std::cout << "FNR in [" << fnr.min << ", " << fnr.max << "]\n";

    return 0;
}

