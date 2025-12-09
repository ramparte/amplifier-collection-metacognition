# Example: Complex Task (Iterative Refinement)

This example shows iterative-refiner handling a novel, complex implementation task.

## Task

"Design and implement a caching layer for our API with TTL support and intelligent invalidation"

## Coordinator Flow

### Step 1: Assess Complexity

```
Coordinator: This sounds complex. Delegating to complexity-assessor.

[Delegates to complexity-assessor]

complexity-assessor analyzes:
  - Scope: Large (design + implement + TTL + invalidation)
  - Novelty: Novel design for this system
  - Integration: Affects API endpoints, needs Redis/memory decision
  - Success Criteria: Somewhat vague ("intelligent invalidation")
  - Context: Need to understand API patterns, data flows
  - Risk: High (performance critical, correctness critical)

Output:
{
  "complexity_score": 7.5,
  "confidence": 0.85,
  "recommendation": "iterative-refinement",
  "reasoning": "Novel design with multiple concerns (storage, TTL, invalidation).
               High risk (performance/correctness). Success criteria need refinement.
               Best approach is iterative with measurement.",
  "suggested_strategy": {
    "approach": "iterative-refinement",
    "estimated_iterations": 3-4,
    "delegate_to": "iterative-refiner"
  }
}
```

### Step 2: Iterative Refinement

```
Coordinator: Delegating to iterative-refiner for systematic refinement.

[Delegates to iterative-refiner]
```

#### Iteration 1: Initial Design & Implementation

```
iterative-refiner: Let me start with a simple approach and measure.

[Generates initial solution]
Design:
- In-memory cache with dict
- Simple TTL: timestamp + expire_seconds
- Invalidation: clear_all() method
- Cache key: f"{endpoint}:{params_hash}"

Implementation:
class APICache:
    def __init__(self):
        self.cache = {}
        self.ttl_map = {}
    
    def get(self, key):
        if key in self.cache:
            if time.time() < self.ttl_map[key]:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.ttl_map[key]
        return None
    
    def set(self, key, value, ttl=3600):
        self.cache[key] = value
        self.ttl_map[key] = time.time() + ttl
    
    def invalidate_all(self):
        self.cache.clear()
        self.ttl_map.clear()

[Self-evaluation]
Testing against requirements:
✓ Basic caching works
✓ TTL expires old entries
✗ No pattern-based invalidation
✗ No memory limits
✗ Not thread-safe
✗ No cache statistics

Soft Score:
- Correctness: 0.7 (works but has gaps)
- Completeness: 0.5 (missing features)
- Quality: 0.6 (simple but naive)
- Clarity: 0.8 (clear code)
Average: 0.65

Feedback:
"Basic implementation works but missing:
1. Intelligent invalidation (no pattern matching)
2. Memory management (unbounded growth)
3. Thread safety (race conditions possible)
4. Observability (no stats)"

Continue: YES (score < 0.9)
```

#### Iteration 2: Add Missing Features

```
iterative-refiner: Score 0.65 → needs significant improvement.
                   Addressing feedback systematically.

[Generates improved solution]
Design changes:
- Add pattern-based invalidation (wildcards)
- Add LRU eviction for memory limits
- Add threading.Lock for thread safety
- Add statistics tracking

Implementation:
from collections import OrderedDict
import threading
import fnmatch

class APICache:
    def __init__(self, max_size=1000):
        self.cache = OrderedDict()
        self.ttl_map = {}
        self.max_size = max_size
        self.lock = threading.Lock()
        self.stats = {"hits": 0, "misses": 0, "evictions": 0}
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                if time.time() < self.ttl_map[key]:
                    self.stats["hits"] += 1
                    self.cache.move_to_end(key)  # LRU
                    return self.cache[key]
                else:
                    self._remove(key)
            self.stats["misses"] += 1
            return None
    
    def set(self, key, value, ttl=3600):
        with self.lock:
            if key in self.cache:
                self._remove(key)
            elif len(self.cache) >= self.max_size:
                self._evict_lru()
            
            self.cache[key] = value
            self.ttl_map[key] = time.time() + ttl
    
    def invalidate_pattern(self, pattern):
        """Invalidate keys matching pattern (e.g., 'users/*')"""
        with self.lock:
            keys_to_remove = [
                k for k in self.cache.keys() 
                if fnmatch.fnmatch(k, pattern)
            ]
            for key in keys_to_remove:
                self._remove(key)
    
    def _evict_lru(self):
        key, _ = self.cache.popitem(last=False)
        del self.ttl_map[key]
        self.stats["evictions"] += 1
    
    def _remove(self, key):
        del self.cache[key]
        del self.ttl_map[key]
    
    def get_stats(self):
        return self.stats.copy()

[Self-evaluation]
Testing:
✓ Pattern-based invalidation works
✓ Memory limits enforced with LRU
✓ Thread-safe operations
✓ Statistics tracking
✗ TTL cleanup is lazy (not proactive)
✗ No persistence option
⚠️ Lock contention under high load

Soft Score:
- Correctness: 0.85 (works well, minor issues)
- Completeness: 0.8 (major features present)
- Quality: 0.75 (good but could optimize)
- Clarity: 0.8 (clear with more complexity)
Average: 0.80

Feedback:
"Much improved! Now has core features. Remaining issues:
1. TTL cleanup is reactive (check on access). Should have background cleanup.
2. Lock could cause contention. Consider sharded locks.
3. No persistence option for cache warmup."

Continue: YES (score < 0.9, still room for improvement)
```

#### Iteration 3: Performance & Polish

```
iterative-refiner: Score 0.80 → good, one more iteration for excellence.
                   Focusing on performance and robustness.

[Generates final solution]
Design improvements:
- Background TTL cleanup thread
- Sharded locks (reduce contention)
- Optional Redis backend for persistence
- Graceful shutdown

Implementation highlights:
class APICache:
    def __init__(self, max_size=1000, num_shards=16, backend='memory'):
        self.num_shards = num_shards
        self.shards = [
            {
                'cache': OrderedDict(),
                'ttl_map': {},
                'lock': threading.Lock(),
                'stats': {"hits": 0, "misses": 0, "evictions": 0}
            }
            for _ in range(num_shards)
        ]
        self.max_size_per_shard = max_size // num_shards
        self.backend = backend
        
        # Background cleanup
        self.cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True
        )
        self.cleanup_thread.start()
    
    def _get_shard(self, key):
        return hash(key) % self.num_shards
    
    def get(self, key):
        shard = self.shards[self._get_shard(key)]
        with shard['lock']:
            # ... implementation with sharded access
    
    def _cleanup_loop(self):
        """Background thread removes expired entries"""
        while True:
            time.sleep(60)  # Run every minute
            for shard in self.shards:
                with shard['lock']:
                    now = time.time()
                    expired = [
                        k for k, expire_time in shard['ttl_map'].items()
                        if now >= expire_time
                    ]
                    for key in expired:
                        self._remove(key, shard)

# Plus Redis backend option for persistence

[Self-evaluation]
Testing:
✓ Background cleanup prevents memory bloat
✓ Sharded locks reduce contention (benchmarked)
✓ Redis backend works for persistence
✓ Graceful shutdown
✓ All original requirements met
✓ Performance is excellent

Soft Score:
- Correctness: 0.95 (robust, well-tested)
- Completeness: 0.95 (all features + extras)
- Quality: 0.90 (clean, performant)
- Clarity: 0.85 (complex but well-documented)
Average: 0.9125

Feedback:
"Excellent implementation! Production-ready caching layer with:
- All required features (TTL, intelligent invalidation)
- Performance optimizations (sharding, background cleanup)
- Flexibility (memory or Redis backend)
- Observability (comprehensive stats)
- Robustness (thread-safe, graceful shutdown)

Minor notes:
- Documentation is good, could add usage examples
- Consider adding cache warming helper"

Continue: NO (score >= 0.9, success threshold met!)
```

### Step 3: Final Result

```
iterative-refiner returns:
{
  "best_iteration": 3,
  "best_score": 0.9125,
  "solution": "... (iteration 3 code) ...",
  "history": [
    {"iteration": 1, "score": 0.65, "approach": "Simple dict cache"},
    {"iteration": 2, "score": 0.80, "approach": "Added features + thread safety"},
    {"iteration": 3, "score": 0.9125, "approach": "Performance + robustness"}
  ],
  "iterations_used": 3,
  "learning": "Started simple, added features, then optimized. Each iteration 
               built on previous feedback. Final solution is production-ready."
}

Coordinator: Excellent! Caching layer implemented with score 0.9125 in 3 iterations.
```

## Evolution Visualization

```
Iteration 1 (Score 0.65):
  Basic dict → Works but naive
  ↓
  Feedback: Missing features, no memory limits, not thread-safe
  ↓
Iteration 2 (Score 0.80):
  + Pattern invalidation
  + LRU eviction
  + Thread safety
  + Statistics
  ↓
  Feedback: Good but lazy TTL, lock contention, no persistence
  ↓
Iteration 3 (Score 0.9125):
  + Background cleanup
  + Sharded locks
  + Redis backend
  + Graceful shutdown
  ↓
  SUCCESS: Production-ready!
```

## Key Insights

1. **Start simple, iterate**: Iteration 1 was deliberately simple
2. **Measured progress**: Scores showed clear improvement (0.65 → 0.80 → 0.91)
3. **Specific feedback**: Each iteration had actionable improvements
4. **Learning from history**: Each iteration built on previous learnings
5. **Automatic termination**: Stopped at score ≥ 0.9, not "max iterations"

## Without Iterative Refinement

Without this approach:
- Might try to get everything perfect in one shot (fail)
- Or ship iteration 1 (score 0.65, not production-ready)
- No systematic improvement process
- No measurement of progress

## Cost Analysis

**Time**:
- Iteration 1: 3 minutes (design + implement + evaluate)
- Iteration 2: 4 minutes (add features + evaluate)
- Iteration 3: 3 minutes (optimize + evaluate)
- Total: ~10 minutes

**LLM calls**:
- Complexity assessment: 1 call
- Iterative refiner: 6 calls (2 per iteration: generate + evaluate)
- Total: 7 calls

**Result**: Production-ready caching layer in 10 minutes with measured confidence.

## Comparison to Single-Pass

Single-pass approach:
- Try to get everything right first time
- Likely score: 0.6-0.7 (missing something)
- Need manual review and refinement
- No systematic improvement process

Iterative approach:
- Start simple, measure, improve
- Final score: 0.91 (excellent)
- Each step validated
- Confidence in result

**Conclusion**: For complex tasks, iteration with measurement beats "get it perfect first time."
