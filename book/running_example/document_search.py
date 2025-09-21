#!/usr/bin/env python3
"""
Private Document Search System - Running Example Implementation
This code progressively builds from Chapter 1 through Chapter 14
"""

import hashlib
import random
import math
from typing import Set, List, Dict, Tuple, Optional
from collections import defaultdict
from itertools import combinations
# import mmh3  # MurmurHash3 for speed (optional dependency)

# ============================================================================
# Stage 1: Basic Bloom Filter (Chapter 1)
# ============================================================================

class BloomFilter:
    """Basic Bloom filter for set membership"""
    
    def __init__(self, expected_items: int, fp_rate: float = 0.001):
        # Calculate optimal size and hash functions
        self.size = self._optimal_size(expected_items, fp_rate)
        self.num_hashes = self._optimal_hashes(expected_items, self.size)
        self.bits = [False] * self.size
        self.count = 0
        
    def _optimal_size(self, n: int, p: float) -> int:
        """Calculate optimal bit array size"""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
    
    def _optimal_hashes(self, n: int, m: int) -> int:
        """Calculate optimal number of hash functions"""
        k = (m / n) * math.log(2)
        return max(1, int(k))
    
    def _hash(self, item: str, seed: int) -> int:
        """Generate hash with seed"""
        # Use built-in hash with seed mixing (not cryptographic but ok for demo)
        h = hashlib.sha256(f"{item}:{seed}".encode()).digest()
        return int.from_bytes(h[:8], 'big') % self.size
    
    def add(self, item: str):
        """Add item to filter"""
        for i in range(self.num_hashes):
            pos = self._hash(item, i)
            self.bits[pos] = True
        self.count += 1
    
    def contains(self, item: str) -> bool:
        """Test membership (may have false positives)"""
        for i in range(self.num_hashes):
            pos = self._hash(item, i)
            if not self.bits[pos]:
                return False
        return True
    
    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """Union of two Bloom filters"""
        if self.size != other.size:
            raise ValueError("Bloom filters must be same size")
        result = BloomFilter(1, 0.001)  # Dummy initialization
        result.size = self.size
        result.num_hashes = max(self.num_hashes, other.num_hashes)
        result.bits = [a or b for a, b in zip(self.bits, other.bits)]
        return result
    
    def intersect(self, other: 'BloomFilter') -> 'BloomFilter':
        """Approximate intersection (higher false positive rate)"""
        if self.size != other.size:
            raise ValueError("Bloom filters must be same size")
        result = BloomFilter(1, 0.001)  # Dummy initialization
        result.size = self.size
        result.num_hashes = max(self.num_hashes, other.num_hashes)
        result.bits = [a and b for a, b in zip(self.bits, other.bits)]
        return result

# ============================================================================
# Stage 2: Hash-Based Privacy (Chapter 2)
# ============================================================================

class HashEncoder:
    """Encodes values using cryptographic hashing"""
    
    def __init__(self, salt: bytes = None):
        self.salt = salt or random.randbytes(32)
    
    def encode(self, value: str) -> str:
        """Hash value with salt"""
        data = value.encode() + self.salt
        return hashlib.sha256(data).hexdigest()
    
    def encode_multiple(self, value: str, count: int) -> List[str]:
        """Generate multiple encodings for frequency hiding"""
        return [self.encode(f"{value}:{i}") for i in range(count)]

# ============================================================================
# Stage 3: Document and Keyword Management (Chapter 3-4)
# ============================================================================

class Document:
    """Document with extractable keywords"""
    
    def __init__(self, doc_id: str, content: str):
        self.id = doc_id
        self.content = content
        self.keywords = self._extract_keywords()
    
    def _extract_keywords(self) -> Set[str]:
        """Simple keyword extraction (real system would use NLP)"""
        # Simplified: split on whitespace and lowercase
        words = self.content.lower().split()
        # Remove common stop words (simplified list)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        return {w for w in words if w not in stop_words and len(w) > 2}

class InvertedIndex:
    """Inverted index using Bloom filters"""
    
    def __init__(self, docs_per_keyword: int = 10000):
        self.encoder = HashEncoder()
        self.keyword_to_docs = {}  # keyword_hash -> BloomFilter
        self.docs_per_keyword = docs_per_keyword
    
    def index_document(self, doc: Document):
        """Add document to index"""
        for keyword in doc.keywords:
            kw_hash = self.encoder.encode(keyword)
            if kw_hash not in self.keyword_to_docs:
                self.keyword_to_docs[kw_hash] = BloomFilter(
                    self.docs_per_keyword, 0.01
                )
            self.keyword_to_docs[kw_hash].add(doc.id)
    
    def search(self, keyword: str) -> Optional[BloomFilter]:
        """Search for documents containing keyword"""
        kw_hash = self.encoder.encode(keyword)
        return self.keyword_to_docs.get(kw_hash)

# ============================================================================
# Stage 4: Boolean Query Processing (Chapter 5-6)
# ============================================================================

class BooleanQuery:
    """Boolean query AST node"""
    pass

class AndQuery(BooleanQuery):
    def __init__(self, left: BooleanQuery, right: BooleanQuery):
        self.left = left
        self.right = right
    
    def evaluate(self, index: InvertedIndex) -> BloomFilter:
        left_result = self.left.evaluate(index)
        right_result = self.right.evaluate(index)
        if left_result and right_result:
            return left_result.intersect(right_result)
        return BloomFilter(1, 1.0)  # Empty result

class OrQuery(BooleanQuery):
    def __init__(self, left: BooleanQuery, right: BooleanQuery):
        self.left = left
        self.right = right
    
    def evaluate(self, index: InvertedIndex) -> BloomFilter:
        left_result = self.left.evaluate(index)
        right_result = self.right.evaluate(index)
        if left_result and right_result:
            return left_result.union(right_result)
        return left_result or right_result or BloomFilter(1, 1.0)

class TermQuery(BooleanQuery):
    def __init__(self, term: str):
        self.term = term
    
    def evaluate(self, index: InvertedIndex) -> BloomFilter:
        result = index.search(self.term)
        return result or BloomFilter(1, 1.0)  # Empty if not found

# ============================================================================
# Stage 5: Correlation Hiding with Tuple Encoding (Chapter 7-8)
# ============================================================================

class TupleAwareIndex(InvertedIndex):
    """Index that encodes common term pairs as tuples"""
    
    def __init__(self, common_pairs: Set[Tuple[str, str]] = None):
        super().__init__()
        self.common_pairs = common_pairs or set()
        self.pair_to_docs = {}  # pair_hash -> BloomFilter
    
    def index_document(self, doc: Document):
        """Index both single terms and common pairs"""
        super().index_document(doc)
        
        # Index common pairs as tuples
        for kw1, kw2 in combinations(sorted(doc.keywords), 2):
            if (kw1, kw2) in self.common_pairs:
                pair_hash = self.encoder.encode(f"({kw1},{kw2})")
                if pair_hash not in self.pair_to_docs:
                    self.pair_to_docs[pair_hash] = BloomFilter(
                        self.docs_per_keyword, 0.01
                    )
                self.pair_to_docs[pair_hash].add(doc.id)
    
    def search_pair(self, term1: str, term2: str) -> Optional[BloomFilter]:
        """Search using tuple encoding if available"""
        pair = tuple(sorted([term1, term2]))
        if pair in self.common_pairs:
            pair_hash = self.encoder.encode(f"({pair[0]},{pair[1]})")
            return self.pair_to_docs.get(pair_hash)
        return None

# ============================================================================
# Stage 6: Frequency Hiding (Chapter 9-10)
# ============================================================================

class FrequencyHidingIndex(TupleAwareIndex):
    """Index that hides term frequencies"""
    
    def __init__(self, term_frequencies: Dict[str, float] = None):
        super().__init__()
        self.term_frequencies = term_frequencies or {}
        self.encoding_map = self._compute_encodings()
    
    def _compute_encodings(self) -> Dict[str, List[str]]:
        """Compute multiple encodings based on frequency"""
        encoding_map = {}
        for term, freq in self.term_frequencies.items():
            # More encodings for rare terms (1/p(x) principle)
            num_encodings = max(1, int(1.0 / freq))
            encoding_map[term] = self.encoder.encode_multiple(term, num_encodings)
        return encoding_map
    
    def search_uniform(self, term: str) -> Optional[BloomFilter]:
        """Search with random encoding selection"""
        if term in self.encoding_map:
            # Pick random encoding
            encodings = self.encoding_map[term]
            chosen = random.choice(encodings)
            # Search using chosen encoding
            return self.keyword_to_docs.get(chosen)
        return self.search(term)
    
    def add_noise_queries(self, real_queries: List[str], noise_rate: float = 0.2):
        """Add fake queries to hide patterns"""
        num_noise = int(len(real_queries) * noise_rate)
        noise_terms = random.sample(list(self.term_frequencies.keys()), 
                                   min(num_noise, len(self.term_frequencies)))
        all_queries = real_queries + noise_terms
        random.shuffle(all_queries)
        return all_queries

# ============================================================================
# Stage 7: Complete Private Search System (Chapter 11-14)
# ============================================================================

class PrivateDocumentSearch:
    """Complete private document search system"""
    
    def __init__(self):
        # Identify common pairs for correlation hiding
        self.common_pairs = {
            ("covid", "vaccine"),
            ("security", "breach"),
            ("password", "leak"),
            ("data", "privacy"),
            ("encryption", "backdoor")
        }
        
        # Estimate term frequencies (would be computed from corpus)
        self.term_frequencies = {
            "covid": 0.3,
            "vaccine": 0.2,
            "security": 0.15,
            "breach": 0.1,
            "password": 0.08,
            "leak": 0.07,
            "data": 0.25,
            "privacy": 0.12,
            "encryption": 0.05,
            "backdoor": 0.02
        }
        
        self.index = FrequencyHidingIndex(self.term_frequencies)
        self.index.common_pairs = self.common_pairs
        self.documents = []
    
    def add_document(self, doc_id: str, content: str):
        """Add document to search system"""
        doc = Document(doc_id, content)
        self.documents.append(doc)
        self.index.index_document(doc)
    
    def search(self, query: str) -> List[str]:
        """Execute private search"""
        # Simple query parsing (real system would have proper parser)
        if " AND " in query:
            terms = query.split(" AND ")
            if len(terms) == 2:
                # Try tuple encoding first
                result = self.index.search_pair(terms[0].strip(), terms[1].strip())
                if result is None:
                    # Fall back to intersection
                    q = AndQuery(TermQuery(terms[0].strip()), 
                                TermQuery(terms[1].strip()))
                    result = q.evaluate(self.index)
        elif " OR " in query:
            terms = query.split(" OR ")
            q = OrQuery(TermQuery(terms[0].strip()), 
                       TermQuery(terms[1].strip()))
            result = q.evaluate(self.index)
        else:
            # Single term query with frequency hiding
            result = self.index.search_uniform(query.strip())
        
        # Check which documents match (with false positives)
        matching_docs = []
        if result:
            for doc in self.documents:
                if result.contains(doc.id):
                    matching_docs.append(doc.id)
        
        return matching_docs

# ============================================================================
# Demo: Progressive Examples
# ============================================================================

def demo_progression():
    """Demonstrate the progression of features"""
    
    print("=" * 60)
    print("Private Document Search System - Progressive Demo")
    print("=" * 60)
    
    # Create system
    search = PrivateDocumentSearch()
    
    # Add sample documents
    documents = [
        ("doc1", "COVID vaccine research shows promising results"),
        ("doc2", "Security breach exposes password database"),
        ("doc3", "Data privacy regulations in healthcare"),
        ("doc4", "Encryption backdoor discovered in software"),
        ("doc5", "COVID treatment options and vaccine efficacy"),
        ("doc6", "Password security best practices guide"),
        ("doc7", "Healthcare data breach affects millions"),
        ("doc8", "Privacy encryption tools for personal data"),
    ]
    
    for doc_id, content in documents:
        search.add_document(doc_id, content)
    
    print("\n1. Basic Search (Single Term):")
    print(f"   Query: 'covid' -> {search.search('covid')}")
    
    print("\n2. Boolean Search (AND):")
    print(f"   Query: 'covid AND vaccine' -> {search.search('covid AND vaccine')}")
    
    print("\n3. Boolean Search (OR):")
    print(f"   Query: 'password OR encryption' -> {search.search('password OR encryption')}")
    
    print("\n4. Correlation Hiding (Tuple Encoding):")
    print(f"   Query: 'encryption AND backdoor' -> {search.search('encryption AND backdoor')}")
    print("   (Note: This pair is encoded as a tuple to hide correlation)")
    
    print("\n5. Frequency Hiding with Noise:")
    real_queries = ["covid", "vaccine", "privacy"]
    all_queries = search.index.add_noise_queries(real_queries)
    print(f"   Real queries: {real_queries}")
    print(f"   With noise: {all_queries}")
    
    print("\n" + "=" * 60)
    print("Features Demonstrated:")
    print("- Bloom filters for space efficiency")
    print("- Hash encoding for query privacy")
    print("- Boolean query processing")
    print("- Tuple encoding for correlation hiding")
    print("- Frequency hiding with multiple encodings")
    print("- Noise injection for pattern obfuscation")
    print("=" * 60)

if __name__ == "__main__":
    demo_progression()