# Running Example: Private Document Search System
## Progressive Development Throughout the Book

---

## Overview

We'll build a complete private document search system that:
1. Starts simple (set membership)
2. Adds features progressively
3. Culminates in a production-ready system

---

## Stage 1: Basic Document Checker (Chapter 1)
### "Has this document been leaked?"

**Scenario**: A company wants to check if internal documents appear on paste sites.

**Traditional Approach**:
```python
class DocumentChecker:
    def __init__(self):
        self.leaked_docs = set()  # Stores all leaked doc hashes
    
    def add_leaked(self, doc_hash):
        self.leaked_docs.add(doc_hash)
    
    def check(self, doc_hash):
        return doc_hash in self.leaked_docs  # Exact membership
```

**Problems**:
- Storage: Need to store all document hashes (GBs of data)
- Privacy: Server sees which documents are being checked
- Performance: Set grows unbounded

**Bloom Filter Solution**:
```python
class BloomDocumentChecker:
    def __init__(self, expected_docs=1000000, fp_rate=0.001):
        self.bloom = BloomFilter(expected_docs, fp_rate)
    
    def add_leaked(self, doc_hash):
        self.bloom.add(doc_hash)
    
    def check(self, doc_hash):
        return self.bloom.contains(doc_hash)  # May have false positives
```

**Benefits**:
- Storage: 10x reduction
- Performance: O(1) operations
- First step toward privacy

---

## Stage 2: Hash-Based Privacy (Chapter 2)
### "Hide what's being checked"

**Enhancement**: Client hashes document before sending to server.

```python
class HashPrivateChecker:
    def __init__(self, secret_salt):
        self.salt = secret_salt
        self.bloom = BloomFilter(1000000, 0.001)
    
    def add_leaked(self, doc):
        # Server stores hashed version
        doc_hash = sha256(doc + self.salt)
        self.bloom.add(doc_hash)
    
    def check(self, doc_hash):
        # Client sends hash, not document
        return self.bloom.contains(doc_hash)

# Client side
def check_document(doc, salt):
    doc_hash = sha256(doc + salt)
    response = server.check(doc_hash)
    return response
```

**Benefits**:
- Server never sees actual documents
- Hashes look uniformly random
- No patterns visible in queries

---

## Stage 3: Keyword Search (Chapter 3-4)
### "Search for documents containing keywords"

**Evolution**: From document-level to keyword-level search.

```python
class KeywordSearchableDoc:
    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.keywords = extract_keywords(content)
        self.keyword_hashes = [hash_keyword(kw) for kw in self.keywords]

class PrivateKeywordSearch:
    def __init__(self):
        # Inverted index using Bloom filters
        self.keyword_to_docs = {}  # keyword_hash -> BloomFilter of doc_ids
    
    def index_document(self, doc):
        for kw_hash in doc.keyword_hashes:
            if kw_hash not in self.keyword_to_docs:
                self.keyword_to_docs[kw_hash] = BloomFilter(10000, 0.01)
            self.keyword_to_docs[kw_hash].add(doc.doc_id)
    
    def search(self, keyword_hash):
        if keyword_hash in self.keyword_to_docs:
            return self.keyword_to_docs[keyword_hash]
        return EmptyBloomFilter()
```

**New Capabilities**:
- Search by keyword, not just document
- Still private (server sees only hashes)
- Supports large document collections

---

## Stage 4: Boolean Queries (Chapter 5-6)
### "Complex queries with AND, OR, NOT"

```python
class BooleanQuery:
    def __init__(self, query_string):
        self.ast = parse_boolean(query_string)
        # Example: "covid AND (vaccine OR treatment) AND NOT hoax"
    
    def to_oblivious(self, encoder):
        return self.ast.transform(encoder)

class ObliviousBooleanSearch:
    def __init__(self):
        self.index = PrivateKeywordSearch()
    
    def search_and(self, term1_hash, term2_hash):
        docs1 = self.index.search(term1_hash)
        docs2 = self.index.search(term2_hash)
        return docs1.intersect(docs2)  # Bloom filter intersection
    
    def search_or(self, term1_hash, term2_hash):
        docs1 = self.index.search(term1_hash)
        docs2 = self.index.search(term2_hash)
        return docs1.union(docs2)  # Bloom filter union
    
    def search_not(self, term_hash, universe):
        docs = self.index.search(term_hash)
        return universe.difference(docs)  # Approximate difference
    
    def execute_query(self, oblivious_query):
        return oblivious_query.evaluate(self)
```

---

## Stage 5: Correlation Hiding (Chapter 7-8)
### "Hide relationships between search terms"

**Problem**: Searching for "encryption" AND "backdoor" reveals security research.

**Solution**: Tuple encoding for common pairs.

```python
class CorrelationHidingSearch:
    def __init__(self):
        self.single_terms = {}  # term_hash -> docs
        self.term_pairs = {}   # pair_hash -> docs
        self.common_pairs = identify_common_pairs()
    
    def index_document(self, doc):
        keywords = extract_keywords(doc)
        
        # Index single terms
        for kw in keywords:
            self.index_single(kw, doc.id)
        
        # Index common pairs as tuples
        for kw1, kw2 in combinations(keywords, 2):
            if (kw1, kw2) in self.common_pairs:
                pair_hash = hash_tuple(kw1, kw2)
                self.index_pair(pair_hash, doc.id)
    
    def search_and_private(self, term1, term2):
        if (term1, term2) in self.common_pairs:
            # Use tuple encoding - correlation hidden!
            pair_hash = hash_tuple(term1, term2)
            return self.term_pairs.get(pair_hash)
        else:
            # Fall back to separate terms
            return self.search_and(hash(term1), hash(term2))
```

---

## Stage 6: Frequency Hiding (Chapter 9-10)
### "Hide how often terms are searched"

```python
class FrequencyHidingSearch:
    def __init__(self):
        self.index = CorrelationHidingSearch()
        self.term_frequencies = calculate_term_frequencies()
        
        # Create multiple encodings for rare terms
        self.encoding_map = {}
        for term, freq in self.term_frequencies.items():
            num_encodings = int(1.0 / freq)  # More encodings for rare terms
            self.encoding_map[term] = [
                hash(term, salt=i) for i in range(num_encodings)
            ]
    
    def search_uniform(self, term):
        # Pick random encoding for this term
        encodings = self.encoding_map[term]
        chosen_encoding = random.choice(encodings)
        return self.index.search(chosen_encoding)
    
    def add_noise_queries(self, real_query):
        # Add fake queries to hide patterns
        noise_queries = generate_noise_queries()
        all_queries = [real_query] + noise_queries
        random.shuffle(all_queries)
        
        results = []
        for query in all_queries:
            result = self.search_uniform(query)
            if query == real_query:
                real_result = result
            results.append(result)
        
        return real_result  # Return only the real result
```

---

## Stage 7: Ranked Retrieval (Chapter 11)
### "Return most relevant documents"

```python
class RankedPrivateSearch:
    def __init__(self):
        self.index = FrequencyHidingSearch()
        
        # Store approximate scores using Bernoulli values
        self.doc_scores = {}  # doc_id -> BernoulliFloat
    
    def index_with_score(self, doc):
        # Calculate relevance scores
        for keyword in doc.keywords:
            tf_idf = calculate_tf_idf(keyword, doc)
            
            # Store as Bernoulli float (approximate)
            score = BernoulliFloat(tf_idf, error_rate=0.05)
            self.doc_scores[(doc.id, keyword)] = score
    
    def search_ranked(self, query_terms, k=10):
        # Get candidate documents
        candidates = self.search_boolean(query_terms)
        
        # Score each candidate (approximately)
        scored_docs = []
        for doc_id in candidates:
            score = BernoulliFloat(0)
            for term in query_terms:
                if (doc_id, term) in self.doc_scores:
                    score += self.doc_scores[(doc_id, term)]
            scored_docs.append((doc_id, score))
        
        # Sort by approximate scores
        scored_docs.sort(key=lambda x: x[1].expected_value(), reverse=True)
        
        # Return top-k
        return scored_docs[:k]
```

---

## Stage 8: Production System (Chapter 12-14)
### "Deploy at scale"

```python
class ProductionPrivateSearch:
    def __init__(self, config):
        self.config = config
        self.index = RankedPrivateSearch()
        self.query_cache = LRUCache(maxsize=10000)
        self.update_tracker = UpdateTracker()
        
        # Initialize with MAB for update timing
        self.mab = MovingAverageBootstrap()
        self.query_history = []
    
    def process_query(self, encrypted_query):
        # Check cache first
        if encrypted_query in self.query_cache:
            return self.query_cache[encrypted_query]
        
        # Decrypt and process
        query = self.decrypt_query(encrypted_query)
        
        # Add to history for MAB analysis
        self.query_history.append(query)
        
        # Check if we need to update oblivious functions
        if self.mab.should_update(self.query_history):
            self.rotate_keys()
        
        # Execute search
        results = self.index.search_ranked(query)
        
        # Encrypt results
        encrypted_results = self.encrypt_results(results)
        
        # Cache for performance
        self.query_cache[encrypted_query] = encrypted_results
        
        return encrypted_results
    
    def rotate_keys(self):
        """Update oblivious functions when adversary might have learned patterns"""
        new_salt = generate_secure_random()
        self.reindex_with_new_salt(new_salt)
        self.query_cache.clear()
        
    def monitor_performance(self):
        """Track system metrics"""
        return {
            'false_positive_rate': self.index.measure_fpr(),
            'query_latency': self.measure_latency(),
            'cache_hit_rate': self.query_cache.hit_rate(),
            'update_frequency': self.update_tracker.frequency()
        }
```

---

## Stage 9: Advanced Features (Chapter 15-16)
### "Future enhancements"

```python
class AdvancedPrivateSearch:
    def __init__(self):
        self.base_system = ProductionPrivateSearch()
        
    def homomorphic_search(self, encrypted_query):
        """Search on encrypted data without decryption"""
        # Use partially homomorphic operations
        pass
    
    def multi_party_search(self, shared_query):
        """Multiple parties search without revealing individual queries"""
        # Use secure multi-party computation
        pass
    
    def verifiable_search(self, query):
        """Prove search was done correctly without revealing data"""
        # Use zero-knowledge proofs
        pass
    
    def quantum_resistant_search(self, query):
        """Resistant to quantum attacks"""
        # Use lattice-based cryptography
        pass
```

---

## Complete System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Encoder   │────▶│   Server    │
│             │     │             │     │             │
│ Documents   │     │ Hash+Salt   │     │ Oblivious   │
│ Keywords    │     │ Bernoulli   │     │ Index       │
│ Queries     │     │ Encoding    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                            │                    │
                            ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   Privacy   │     │  Storage    │
                    │             │     │             │
                    │ Uniformity  │     │ Bloom       │
                    │ Correlation │     │ Filters     │
                    │ Hiding      │     │             │
                    └─────────────┘     └─────────────┘
```

---

## Learning Progression

1. **Chapter 1**: Basic Bloom filter for documents
2. **Chapter 2**: Add hashing for privacy
3. **Chapter 3**: Understand privacy threats
4. **Chapter 4**: Build first oblivious version
5. **Chapters 5-8**: Add Boolean queries and theory
6. **Chapters 9-11**: Advanced features (correlation hiding, ranking)
7. **Chapters 12-13**: Production deployment
8. **Chapter 14**: Real case study with metrics
9. **Chapters 15-16**: Future enhancements

---

## Key Metrics Throughout

- **Storage**: From 32GB → 1.5GB (95% reduction)
- **Query time**: From milliseconds → microseconds
- **Privacy**: From full visibility → oblivious
- **False positive rate**: Configurable (0.1% typical)
- **Update frequency**: Based on MAB analysis

This running example provides:
- Concrete motivation for each concept
- Progressive complexity
- Real performance numbers
- Practical implementation guidance
- Clear privacy improvements at each stage