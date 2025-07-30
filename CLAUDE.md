# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

### Building the Project
```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
```

### Running Tests
```bash
# From build directory
make test                    # Run all tests
ctest --output-on-failure   # Run tests with failure details
make check                  # Custom target with output on failure
./tests/bernoulli_tests     # Run test binary directly
```

### Building with Options
```bash
cmake -DBERNOULLI_BUILD_TESTS=ON \
      -DBERNOULLI_BUILD_EXAMPLES=ON \
      -DBERNOULLI_BUILD_BENCHMARKS=ON \
      -DBERNOULLI_BUILD_DOCS=ON ..
```

### Building Documentation
```bash
# Requires Doxygen
cmake -DBERNOULLI_BUILD_DOCS=ON ..
make docs
```

### Building Research Papers
```bash
cd papers
make all    # Build all LaTeX papers
make clean  # Clean LaTeX build artifacts
```

## Architecture Overview

### Core Concept: Latent vs Observed Types
The framework distinguishes between:
- **Latent values** (S, f, x): True mathematical objects that exist conceptually but aren't computationally accessible
- **Observed values** (~S, ~f, ~x): Noisy approximations we actually compute with

This duality is central to all data structures in the library.

### Project Structure
- `include/bernoulli/`: Header-only library implementation
  - Core types: `observed_bool`, `observed_set`, `observed_map`
  - Data structures: `bloom_filter/`, `hash_set`, `hash_map`
  - Utilities: `rate_span` (error rate intervals), `hash_set_builder`
- `tests/`: Google Test based unit tests
- `examples/`: Usage examples for each major component
- `papers/`: LaTeX source for 7 research papers developing the theory

### Key Design Patterns
1. **Error Propagation**: All operations track error rates through `rate_span` intervals
2. **Type Erasure**: Allows storing different probabilistic implementations uniformly
3. **Expression Templates**: Enable lazy evaluation of set operations
4. **Header-Only**: Entire library is template-based in headers

### Testing Philosophy
- Each data structure has comprehensive unit tests
- Tests verify both functional correctness and statistical properties
- Error propagation is tested through composed operations
- Performance benchmarks track space/time tradeoffs

## Important Implementation Notes

### Error Rate Handling
- Error rates are represented as intervals `[min, max]` using `rate_span`
- Operations compose error rates following probability theory
- Conservative bounds are used when exact rates are unknown

### Hash Function Requirements
- Data structures use templated hash functions (default `std::hash`)
- Multiple independent hash functions required for Bloom filters
- Hash quality directly impacts false positive rates

### Memory Management
- RAII used throughout - no manual memory management
- Move semantics optimized for large data structures
- Copy operations may be expensive for large filters

### C++ Standard Requirements
- Requires C++17 or later
- Uses structured bindings, if constexpr, and other C++17 features
- No external dependencies beyond standard library (except Google Test for tests)