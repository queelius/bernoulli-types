#include <gtest/gtest.h>
#include <bernoulli/observed_bool.hpp>

TEST(ObservedBoolTest, Construction) {
    // Default error
    observed_bool b1(true);
    EXPECT_TRUE(b1.value);
    EXPECT_EQ(b1.error.min, 0.0f);
    EXPECT_EQ(b1.error.max, 0.0f);
    
    // With error rate
    observed_bool b2(false, 0.1f);
    EXPECT_FALSE(b2.value);
    EXPECT_EQ(b2.error.min, 0.1f);
    EXPECT_EQ(b2.error.max, 0.1f);
    
    // With error interval
    observed_bool b3(true, rate_span(0.05f, 0.15f));
    EXPECT_TRUE(b3.value);
    EXPECT_EQ(b3.error.min, 0.05f);
    EXPECT_EQ(b3.error.max, 0.15f);
}

TEST(ObservedBoolTest, LogicalNot) {
    observed_bool b(true, 0.1f);
    auto neg = ~b;
    
    EXPECT_FALSE(neg.value);
    EXPECT_EQ(neg.error.min, 0.1f);  // Error rate preserved
    EXPECT_EQ(neg.error.max, 0.1f);
}

TEST(ObservedBoolTest, LogicalAnd) {
    observed_bool a(true, 0.1f);
    observed_bool b(true, 0.2f);
    
    auto result = a & b;
    EXPECT_TRUE(result.value);
    
    // When both are true, error occurs if either was actually false
    // P(error) = P(a false) + P(b false) - P(both false)
    // = 0.1 + 0.2 - 0.1*0.2 = 0.28
    EXPECT_FLOAT_EQ(result.error.min, 0.28f);
    EXPECT_FLOAT_EQ(result.error.max, 0.28f);
}

TEST(ObservedBoolTest, LogicalOr) {
    observed_bool a(false, 0.1f);
    observed_bool b(false, 0.2f);
    
    auto result = a | b;
    EXPECT_FALSE(result.value);
    
    // When both are false, correct unless both were actually true
    // Using De Morgan's law implementation
    auto expected = ~(~a & ~b);
    EXPECT_EQ(result.value, expected.value);
}

TEST(ObservedBoolTest, ImplicitConversion) {
    observed_bool b(true, 0.1f);
    
    // Should be implicitly convertible to bool
    if (b) {
        SUCCEED();
    } else {
        FAIL();
    }
    
    bool raw_value = b;
    EXPECT_TRUE(raw_value);
}

TEST(ObservedBoolTest, ErrorPropagationComplex) {
    // Test complex expression: (a & b) | (~c)
    observed_bool a(true, 0.1f);
    observed_bool b(false, 0.2f);
    observed_bool c(true, 0.15f);
    
    auto result = (a & b) | (~c);
    
    // a & b should be false (since b is false)
    auto and_result = a & b;
    EXPECT_FALSE(and_result.value);
    
    // ~c should be false (since c is true)
    auto not_c = ~c;
    EXPECT_FALSE(not_c.value);
    
    // false | false = false
    EXPECT_FALSE(result.value);
    
    // Error interval should be valid
    EXPECT_GE(result.error.max, result.error.min);
    EXPECT_GE(result.error.min, 0.0f);
    EXPECT_LE(result.error.max, 1.0f);
}