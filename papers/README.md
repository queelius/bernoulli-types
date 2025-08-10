# Research Papers Organization

This directory contains three interconnected series of academic papers on probabilistic and oblivious computing.

## Directory Structure

```
papers/
├── bernoulli_series/     # Bernoulli Types (7 papers + addendum)
├── oblivious_series/     # Oblivious Computing (6 papers + addendum)
├── bridge_paper/         # Unified hash-based framework
└── Makefile             # Master build system
```

## Paper Series

### 1. Bernoulli Types Series (`bernoulli_series/`)

Explores probabilistic data structures with controlled error rates:

1. **Foundations of Bernoulli Types** - Latent/observed duality framework
2. **Bernoulli Sets and Algebra** - Set operations with false positives/negatives
3. **Bernoulli Maps and Composition** - Function approximation and composition
4. **Regular Bernoulli Types** - Type-theoretic properties
5. **Search and Retrieval** - Information retrieval with Bernoulli sets
6. **Implementation and Applications** - Practical systems
7. **Case Study and Statistics** - Statistical analysis methods
8. **Addendum: Hash-Based Construction** - Unified construction via encoding sets

### 2. Oblivious Computing Series (`oblivious_series/`)

Covers privacy-preserving computation hiding access patterns:

1. **Foundations of Oblivious Computing** - Hidden data, observable computation
2. **Secure Indexes with Oblivious Bernoulli** - Combining approximation and privacy
3. **Oblivious Data Structures** - Arrays, trees, heaps with hidden access
4. **Cipher Boolean Rings** - XOR-based constructions for equality testing
5. **Private Information Retrieval** - Oblivious access to public data
6. **Applications and Systems** - Real-world deployments
7. **Addendum: Uniform Encoding** - Achieving perfect obliviousness

### 3. Bridge Paper (`bridge_paper/`)

**Hash-Based Constructions: A Unified Framework** - Shows how both Bernoulli and Oblivious types emerge from the same hash-based construction with encoding sets.

## Building the Papers

### Build Everything
```bash
make all          # Build all three series
```

### Build Individual Series
```bash
make bernoulli    # Build Bernoulli Types series
make oblivious    # Build Oblivious Computing series  
make bridge       # Build bridge paper
```

### Build Specific Papers
```bash
make -C bernoulli_series 01   # Build paper 1 of Bernoulli series
make -C oblivious_series 03   # Build paper 3 of Oblivious series
```

### Other Commands
```bash
make clean        # Remove auxiliary files
make cleanall     # Remove all generated files including PDFs
make rebuild      # Clean and rebuild everything
make check        # Check for LaTeX warnings
make pages        # Show page counts for all papers
make help         # Show detailed help
```

## Key Insights

The papers reveal a fundamental unity:

1. **Hash-based construction** underlies both paradigms
2. **Encoding set sizes** determine properties:
   - Entropy-optimal → Space-efficient Bernoulli types
   - Privacy-optimal → Uniform oblivious types
3. **Invalid inputs** provide free noise for privacy
4. **Single hash evaluation** replaces complex protocols

## Dependencies

- LaTeX distribution with pdflatex
- BibTeX for bibliography management
- Standard LaTeX packages (amsmath, tikz, algorithm2e, etc.)

## Notes

- The `04_trapdoor_cipher_oblivious_sets.tex.backup` file is an alternative version exploring trapdoor functions (kept for reference)
- Papers share common notation files within each series
- The bridge paper can be read standalone or after either series