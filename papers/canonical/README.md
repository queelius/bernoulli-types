# Canonical Bernoulli Types Papers

This directory contains the canonical academic papers on Bernoulli Types, organized as a coherent series suitable for submission to top-tier venues.

## Papers

1. **paper1_latent_observed.tex** - "Bernoulli Types: A Latent/Observed Duality for Approximate Computing"
   - Target venues: POPL, ICFP, PLDI
   - Focus: Type-theoretic foundations and programming language integration

2. **paper2_asymptotic_privacy.tex** - "Asymptotic Privacy Through Rank-Deficient Observation"
   - Target venues: IEEE S&P, USENIX Security, CCS
   - Focus: Privacy guarantees through confusion matrix rank analysis

3. **paper3_hash_constructions.tex** - "Universal Hash Constructions for Bernoulli Types"
   - Target venues: STOC, FOCS, SODA
   - Focus: Algorithmic foundations and hash-based implementations

4. **paper4_bernoulli_sets.tex** - "Bernoulli Sets: A Comprehensive Statistical Framework for Probabilistic Set Membership"
   - Target venues: PODS, SIGMOD, VLDB
   - Focus: Probabilistic set data structures with complete statistical analysis

## Common Files

- **canonical_notation.tex** - Unified notation used across all papers for consistency
- **references.bib** - Shared bibliography

## Building the Papers

### Build all papers:
```bash
make all
```

### Build individual papers:
```bash
make paper1  # Latent/Observed Duality
make paper2  # Asymptotic Privacy
make paper3  # Hash Constructions
make paper4  # Bernoulli Sets
```

### Quick build (single pass, no bibliography):
```bash
make quick
```

### Clean auxiliary files:
```bash
make clean     # Remove aux, log, etc.
make cleanall  # Also remove PDFs
```

## Paper Structure

Each paper follows standard academic format:
- Abstract
- Introduction with motivation and contributions
- Technical content (3-5 main sections)
- Related work
- Conclusion
- References
- Appendices (proofs, additional details)

## Key Concepts

### Model Hierarchy
- **First-order**: Binary symmetric channel (single error parameter ε)
- **Second-order**: Asymmetric errors (separate α and β parameters)
- **Higher-order**: Element-specific or context-dependent error rates

### Notation
All papers use consistent notation from `canonical_notation.tex`:
- Latent values: `S`, `f`, `x`
- Observed values: `~S`, `~f`, `~x` (rendered with \observed{})
- Error rates: `α` (false positive), `β` (false negative), `ε` (symmetric)
- Confusion matrix: `Q`

## Dependencies

- LaTeX distribution with pdflatex
- Standard packages: amsmath, amsthm, algorithm, tikz, hyperref
- BibTeX for bibliography management