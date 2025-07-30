# Contributing to Bernoulli Types

Thank you for your interest in contributing to the Bernoulli Types library! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Provide a clear description of the problem
- Include minimal reproducible examples when applicable
- Specify your environment (OS, compiler, C++ version)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`make test`)
6. Update documentation as needed
7. Commit with clear messages (`git commit -m 'Add amazing feature'`)
8. Push to your fork (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/yourusername/bernoulli-types.git
cd bernoulli-types
mkdir build && cd build
cmake -DBERNOULLI_BUILD_TESTS=ON -DBERNOULLI_BUILD_EXAMPLES=ON ..
make
make test
```

### Coding Standards

- Follow the existing code style
- Use descriptive variable names
- Document public APIs with Doxygen comments
- Keep the latent/observed distinction clear
- Prefer `const` correctness
- Use RAII and avoid raw pointers

### Testing

- Write unit tests for new features
- Ensure statistical properties are validated
- Test error propagation behavior
- Include edge cases

### Documentation

- Update inline documentation
- Add examples for new features
- Update the theory/implementation guides if needed
- Keep mathematical notation consistent

## Project Structure

```
bernoulli-types/
├── include/bernoulli/    # Public headers
├── tests/                # Unit tests
├── examples/             # Example programs
├── benchmarks/           # Performance tests
├── papers/               # Research papers (LaTeX)
└── docs/                 # Additional documentation
```

## Areas for Contribution

- **New data structures**: Implement more probabilistic data structures
- **Performance**: Optimize existing implementations
- **Documentation**: Improve examples and guides
- **Research**: Extend the theoretical framework
- **Bindings**: Create Python/Rust/other language bindings
- **Visualization**: Tools for visualizing error propagation

## Questions?

Feel free to open an issue for discussion or reach out to the maintainers.

Thank you for contributing!