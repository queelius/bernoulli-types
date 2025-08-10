# Oblivious Computing Academic Series - Organization Plan

## Core Theme
Oblivious computing: Systems that compute on hidden data while preserving privacy through controlled information leakage.

## Proposed Paper Structure

### Part 1: Foundations of Oblivious Computing
- Define oblivious data structures and computation
- Information-theoretic framework for privacy
- Relationship to secure multi-party computation
- Connection to Bernoulli Types (observation through constrained channels)

### Part 2: Secure Indexes and Encrypted Search
- Perfect hash filters for space-optimal secure indexes
- Entropy analysis of secure index constructions
- Bloom filters vs. perfect hash filters for encrypted search
- Confidentiality measures and information leakage bounds

### Part 3: Oblivious Data Structures
- Oblivious RAM and path-ORAM constructions
- Oblivious priority queues and sorting
- Trade-offs between access pattern hiding and performance
- Connection to differential privacy

### Part 4: Trapdoor Functions and Searchable Encryption
- Cipher sets over trapdoors
- Symmetric searchable encryption schemes
- Public-key encryption with keyword search
- Forward and backward privacy definitions

### Part 5: Private Information Retrieval
- Single-server PIR with computational assumptions
- Multi-server information-theoretic PIR
- Batch codes and PIR with preprocessing
- Applications to private database queries

### Part 6: Statistical Analysis and Inference Attacks
- Frequency analysis on encrypted searches
- Query recovery attacks and defenses
- Bootstrap methods for confidentiality estimation
- Maximum likelihood estimation of hidden queries

### Part 7: Applications and Systems
- Private messaging and Signal protocol
- Anonymous credentials and zero-knowledge proofs
- Blockchain privacy techniques
- Secure indexes for cloud storage

## Relationship to Bernoulli Types Series

### Shared Concepts
- **Latent vs. Observed**: Both series distinguish between hidden truth and observable approximations
- **Information channels**: Bernoulli uses probabilistic channels, Oblivious uses cryptographic channels
- **Space-optimal constructions**: HashSet (Bernoulli) and Perfect Hash Filters (Oblivious) share theoretical foundations
- **Error/leakage bounds**: False positive rates vs. information leakage rates

### Cross-References
- Bernoulli Paper 5 (Search/Retrieval) → Oblivious Paper 2 (Secure Indexes)
- Bernoulli Paper 2 (Sets) → Oblivious Paper 3 (Oblivious Data Structures)
- Bernoulli Paper 1 (Foundations) → Oblivious Paper 1 (Foundations)

## Materials from `other/` Folder

### Core Secure Index Papers
- `secure_index_entropy/` → Part 2 (entropy analysis)
- `encrypted_search_probabilistic_estimator_conf/` → Part 6 (statistical analysis)
- `estimating_es_conf_moving_avg_bootstrap/` → Part 6 (bootstrap methods)

### Trapdoor and Cipher Types
- `cipher_trapdoor_sets/` → Part 4 (searchable encryption)
- `algebraic_type_set_map_over_cipher/` → Part 4 (algebraic structures)

### Probabilistic Foundations
- `perfect_hash_filters/` → Part 2 (space-optimal constructions)
- `semantic_security_of_sketch_and_pht/` → Part 2 (security proofs)

### Applications
- `oblivious_turing_machine/` → Part 3 (theoretical foundations)
- Materials for cloud storage, messaging → Part 7

## Implementation Strategy

1. **Start with Foundations**: Establish oblivious computing framework connecting to Bernoulli types
2. **Focus on Secure Indexes**: This is the most mature area with existing papers
3. **Expand to General Oblivious Structures**: Build on secure index theory
4. **Add Cryptographic Layers**: Introduce trapdoors and searchable encryption
5. **Statistical Analysis**: Formalize attack models and defenses
6. **Systems and Applications**: Demonstrate practical deployments

## Benefits of Separate Series

1. **Clarity**: Oblivious computing has distinct cryptographic focus vs. Bernoulli's probabilistic focus
2. **Audience**: Different communities (cryptography vs. algorithms/data structures)
3. **Depth**: Each series can develop its theory fully without conflating concepts
4. **Cross-pollination**: Explicit connections enrich both series

## Next Steps

1. Draft Part 1 (Foundations) connecting to Bernoulli framework
2. Adapt existing secure index papers for Part 2
3. Outline remaining parts with clear scope
4. Ensure consistent notation across series
5. Create unified bibliography with cross-series references