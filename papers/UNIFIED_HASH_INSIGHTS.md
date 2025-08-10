# Unified Hash-Based Framework for Bernoulli and Oblivious Types

## Core Insight

Both Bernoulli types and oblivious computing can be understood through a unified hash-based construction where:

1. **Controlled mappings**: We find seeds to ensure correct mappings for known inputs
2. **Natural randomness**: Unknown/invalid inputs map randomly via hash function properties
3. **Emergent error rates**: False positives/negatives emerge naturally from encoding set sizes

## The General Construction

For any function `f: X → Y`:

```
1. Choose encoding functions:
   - encode_X: X → {0,1}*
   - encode_Y: Y → P({0,1}^m)  // Y maps to SETS of valid encodings

2. Find seed s such that:
   - ∀x ∈ X: h(encode_X(x) || s) ∈ encode_Y(f(x))
   - With probability ≥ (1 - β) for Bernoulli types

3. For queries:
   - x ∈ X: Maps correctly (with probability 1-β)
   - u ∉ X: Maps to random output, hits encode_Y(y) with probability |encode_Y(y)|/2^m
```

## Key Design Principles

### 1. Encoding Set Sizes Control Error Rates

For set indicator `I_X`:
- `|encode_Y(True)|/2^m = α` (false positive rate)
- `|encode_Y(False)|/2^m = 1-α`

### 2. Uniformity for Privacy

For oblivious computing, choose encoding sizes to achieve uniform distribution:
- If `y₁` appears twice as often as `y₂` in range of f
- Set `|encode_Y(y₁)| = 2 × |encode_Y(y₂)|`
- Result: Each individual encoding appears with equal frequency

### 3. Noise Injection is Free

Invalid inputs naturally provide noise:
- Don't need to explicitly handle u ∉ X
- Hash function maps them uniformly
- Indistinguishable from intentional outputs

## Spectrum of Constructions

### Singular Hash Map (Overly Restrictive)
- `|encode_Y(y)| = 1` for all y
- Hardest seed finding
- Most space efficient
- Potentially leaky

### Entropy-Optimal Map
- `|encode_Y(y)| ∝ |{x : f(x) = y}|`
- Balances seed finding difficulty with space
- Natural for compression

### Privacy-Optimal Map
- `|encode_Y(y)|` chosen for uniform output distribution
- Best privacy properties
- May require more space

### Bernoulli Map (Approximate)
- Allow β fraction of X to map incorrectly
- Much easier seed finding
- Natural error rates

## Implications for Bernoulli Types

### Bloom Filters from First Principles

A Bloom filter is just:
```
f: X → {True}  (constant function)
encode_Y(True) = {0, 1, ..., α·2^m - 1}
encode_Y(False) = {α·2^m, ..., 2^m - 1}
```

Where:
- Members of X map to True encodings (by construction)
- Non-members map randomly, hitting True encodings with probability α

### No Explicit Bit Setting

Traditional view: Set k bits at positions h₁(x), h₂(x), ..., hₖ(x)
Our view: Find seed where h(x||s) ∈ ValidEncodings(True)

Single hash evaluation, same false positive guarantees!

## Implications for Oblivious Computing

### Composition with Noise Preservation

For `g ∘ f`:
```
Valid path:    x → f(x) → g(f(x))
Invalid path:  u → random → random
```

Both paths use same operations, indistinguishable to observer.

### Uniform Observable Layer

The observable computation `ĝ ∘ f̂` achieves:
- Uniform input distribution (with noise injection)
- Uniform output distribution (with proper encoding sizes)
- Uniform intermediate values (composition preserves uniformity)

## Update Locations

### Bernoulli Series Updates

1. **Paper 1 (Foundations)**: Add section on hash-based construction as alternative to traditional Bloom filters

2. **Paper 2 (Sets)**: Replace traditional Bloom filter construction with general hash-based framework

3. **Paper 5 (Search/Retrieval)**: Show how search uses natural false positives from hash construction

### Oblivious Series Updates

1. **Paper 2 (Secure Indexes)**: Emphasize encoding ranges and uniformity requirements

2. **Paper 4 (Boolean Rings)**: Connect XOR/OR constructions to encoding set choices

3. **Paper 6 (Applications)**: Show how real systems use noise injection

## New Unified Paper?

Consider adding a bridge paper:
"Hash-Based Constructions for Bernoulli and Oblivious Types: A Unified Framework"

Content:
- General construction algorithm
- Seed finding strategies
- Encoding design for different objectives
- Composition and noise propagation
- Implementation techniques

## Key Takeaways

1. **One Framework**: Hash-based construction unifies Bernoulli and oblivious types
2. **Natural Errors**: False positives/negatives emerge from encoding set sizes
3. **Free Noise**: Invalid inputs provide automatic noise for privacy
4. **Flexible Trade-offs**: Encoding choices control space/privacy/accuracy balance
5. **Elegant Theory**: Cleaner than traditional bit-setting approaches