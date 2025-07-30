#include <gtest/gtest.h>
#include <bernoulli/hash_set.hpp>
#include <bernoulli/hash_set_builder.hpp>
#include <bernoulli/observed_set.hpp>
#include <vector>
#include <string>

TEST(HashSetTest, BuilderCreatesValidHashSet) {
    std::vector<std::string> elements = {"alpha", "beta", "gamma", "delta"};
    
    auto set = bernoulli::hash_set_builder<>()
        .false_positive_rate(0.1)
        .seed(42)  // For reproducibility
        .build(elements);
    
    // All elements should be members (no false negatives in this construction)
    for (const auto& elem : elements) {
        EXPECT_TRUE(set.contains(elem));
    }
    
    // FPR should be approximately what we requested
    EXPECT_NEAR(set.false_positive_rate(), 0.1, 0.01);
    
    // FNR should be 0 for this construction
    EXPECT_EQ(set.false_negative_rate(), 0.0);
}

TEST(HashSetTest, EmptySetConstruction) {
    std::vector<std::string> empty;
    auto set = bernoulli::hash_set_builder<>()
        .false_positive_rate(0.01)
        .build(empty);
    
    // Should not contain any elements
    EXPECT_FALSE(set.contains("anything"));
    EXPECT_EQ(set.false_positive_rate(), 0.0);
}

TEST(HashSetTest, TypeErasureWithObservedSet) {
    std::vector<std::string> elements = {"alpha", "beta", "gamma", "delta"};
    
    auto concrete_set = bernoulli::hash_set_builder<>()
        .false_positive_rate(0.05)
        .seed(12345)
        .build(elements);
    
    bernoulli::observed_set<std::string> obs_set(concrete_set);
    
    // Should behave the same as concrete set
    for (const auto& elem : elements) {
        EXPECT_EQ(obs_set.contains(elem), concrete_set.contains(elem));
    }
    
    EXPECT_EQ(obs_set.false_positive_rate(), concrete_set.false_positive_rate());
    EXPECT_EQ(obs_set.false_negative_rate(), concrete_set.false_negative_rate());
}