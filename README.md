# Bernoulli Types

A unified C++ framework for probabilistic data structures based on the fundamental distinction between latent (true but unobservable) values and their observed (noisy but measurable) approximations.

## Overview

The Bernoulli Types library provides a principled approach to building and reasoning about probabilistic data structures. By making approximation a first-class concept at the type level, it enables:

- **Formal reasoning** about error propagation
- **Composable** probabilistic data structures  
- **Explicit** accuracy/resource tradeoffs
- **Type-safe** error handling

## Key Concepts

### Latent vs. Observed

The framework is built on a fundamental distinction:

- **Latent values** (`S`, `f`, `x`): The true mathematical objects we care about
- **Observed values** (`~S`, `~f`, `~x`): The noisy approximations we compute with

```cpp
// Latent set S - exists mathematically but not computationally accessible
Set<int> S = {1, 2, 3, 4, 5};

// Observed set ~S - what we actually work with
observed_set<int> obs_S = bloom_filter<int>(1000, 3);
obs_S.insert(1);
obs_S.insert(2);
// ...

// Query with possible false positives
if (obs_S.contains(6)) {  // May return true even though 6 ∉ S
    // ...
}
```

### Examples in Practice

- **Bloom filters**: Observe latent sets through membership queries
- **Count-Min sketches**: Observe latent frequency distributions  
- **MinHash**: Observe latent set similarities
- **Miller-Rabin**: Observe latent primality property

## Quick Start

### Requirements

- C++17 or later
- CMake 3.14 or later
- (Optional) Google Test for unit tests

### Building

```bash
mkdir build && cd build
cmake ..
make
make test  # Run unit tests
```

### Basic Usage

```cpp
#include <bernoulli/observed_bool.hpp>
#include <bernoulli/observed_set.hpp>
#include <bernoulli/bloom_filter.hpp>

// Observed boolean with error rate
observed_bool obs_true(true, 0.1);  // 10% error rate

// Bloom filter as observed set
bloom_filter<std::string> filter(10000, 4);
filter.insert("hello");
filter.insert("world");

if (filter.contains("hello")) {
    // Definitely in the set
}

if (filter.contains("goodbye")) {
    // Might be a false positive!
}

// Get error characteristics
auto fpr = filter.false_positive_rate();
std::cout << "FPR: [" << fpr.min << ", " << fpr.max << "]" << std::endl;
```

## Documentation

- [Theory Guide](docs/theory.md) - Mathematical foundations and concepts
- [Examples](docs/examples.md) - Practical examples and use cases
- [Implementation Guide](docs/implementation.md) - C++ implementation details
- [API Reference](https://yourusername.github.io/bernoulli-types/) - Generated from headers

## Research Papers

The `papers/` directory contains LaTeX source for research papers developing the theory:

1. **Foundations of Bernoulli Types** - Core framework and mathematical foundations
2. **Bernoulli Sets and Boolean Algebra** - Set-theoretic operations and error propagation
3. **Universal Bernoulli Maps** - Function approximation and composition
4. **Regular Types and Bernoulli Types** - Type algebra and limitations
5. **Applications to Search and Retrieval** - Information retrieval applications
6. **Entropy Maps Implementation** - Space-optimal implementations
7. **Statistical Analysis** - Distributions and confidence intervals

Build the papers:
```bash
cd papers
make all
```

## Features

### Data Structures

- **Bloom filters** - Space-efficient set membership
- **Count-Min sketch** - Frequency estimation
- **MinHash** - Set similarity  
- **Cuckoo filters** - Deletable Bloom filters

### Type System

- **Type erasure** - Store different implementations uniformly
- **Expression templates** - Lazy evaluation of set operations
- **Error propagation** - Track uncertainty through computations
- **Interval arithmetic** - Handle uncertain error rates

### Algorithms

- **Space-optimal constructions** - Achieve information-theoretic bounds
- **Adaptive error rates** - Adjust parameters dynamically
- **Majority voting** - Improve accuracy with multiple observations

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this library in academic work, please cite:

```bibtex
@software{bernoulli_types,
  author = {Towell, Alexander},
  title = {Bernoulli Types: A Unified Framework for Probabilistic Data Structures},
  year = {2024},
  url = {https://github.com/yourusername/bernoulli-types}
}
```

## Acknowledgments

This work was developed as part of research into probabilistic data structures and their theoretical foundations. Special thanks to the Bloom filter paper authors for inspiration.