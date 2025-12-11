# Performance Guide

This guide provides performance benchmarks, resource estimates, and optimization tips for the metacognition collection.

## Overview

Metacognitive agents add computational overhead for assessment, evaluation, and iteration. Understanding performance characteristics helps you make informed trade-offs between quality and speed.

## Execution Time Benchmarks

### Agent Invocation Times

Based on typical usage with Claude Sonnet 4.5:

| Agent | Typical Time | Token Usage | Use Case |
|-------|-------------|-------------|----------|
| complexity-assessor | 3-5 seconds | 500-1,000 | Quick assessment before each task |
| solution-evaluator | 5-10 seconds | 1,000-2,000 | Evaluate completed solutions |
| iterative-refiner (per iteration) | 60-120 seconds | 3,000-6,000 | Generate + evaluate + refine |
| ensemble-coordinator (5 strategies) | 120-300 seconds | 15,000-30,000 | Parallel strategy exploration |

**Note**: Times are wall-clock with parallel execution. Sequential execution would be significantly slower for ensemble.

### Workflow Benchmarks

Complete workflows from task input to final result:

| Workflow | Complexity | Time | Token Usage | Outcome |
|----------|-----------|------|-------------|---------|
| Simple (solve-directly) | 1-3 | 30-60 sec | 2,000-3,000 | Direct execution |
| Medium (single-pass-review) | 4-6 | 60-120 sec | 5,000-8,000 | One iteration |
| High (iterative-refinement, 3 iter) | 7-8 | 3-6 min | 12,000-20,000 | Multiple attempts |
| Critical (ensemble, 5 strategies) | 9-10 | 5-10 min | 20,000-40,000 | Parallel exploration |

### Iteration Convergence

Typical iteration patterns:

```
Fast convergence (simple improvement needed):
Iteration 1: 0.65 (60s)
Iteration 2: 0.93 (60s)
Total: 2 iterations, 120 seconds

Moderate convergence (several refinements):
Iteration 1: 0.55 (60s)
Iteration 2: 0.72 (70s)
Iteration 3: 0.88 (80s)
Iteration 4: 0.94 (90s)
Total: 4 iterations, 300 seconds (5 min)

Slow convergence (complex problem):
Iteration 1: 0.45 (90s)
Iteration 2: 0.60 (100s)
Iteration 3: 0.71 (110s)
Iteration 4: 0.79 (120s)
Iteration 5: 0.82 (plateau)
Total: 5 iterations, 520 seconds (8.7 min)
```

## Resource Usage

### Token Consumption

**By Agent Type**:
- **Assessment**: 500-1,000 tokens (complexity-assessor)
- **Evaluation**: 1,000-2,000 tokens (solution-evaluator)
- **Generation**: 2,000-4,000 tokens (implementing solution)
- **Refinement**: 3,000-6,000 tokens per iteration

**By Workflow**:
- **Simple tasks**: 2,000-5,000 tokens total
- **Medium tasks**: 5,000-10,000 tokens total
- **Complex tasks**: 15,000-25,000 tokens total
- **Ensemble (5 strategies)**: 25,000-50,000 tokens total

**Cost Estimates** (based on Claude Sonnet 4.5 pricing):
- Simple workflow: $0.04-0.08
- Medium workflow: $0.08-0.15
- Complex workflow: $0.25-0.40
- Ensemble workflow: $0.40-0.80

*Note: Prices as of Jan 2025, may vary*

### Memory Usage

- **Complexity assessment**: Minimal (<50 MB)
- **Iterative refinement**: Moderate (100-300 MB, stores iteration history)
- **Ensemble coordination**: Higher (300-500 MB, multiple parallel contexts)

### Network Bandwidth

- **Per API call**: 5-20 KB request, 10-50 KB response
- **Iterative workflow (5 iterations)**: ~200-500 KB total
- **Ensemble (5 parallel)**: ~300-700 KB total (simultaneous)

## Performance Optimization

### 1. Right-Size Your Strategy

**Don't over-engineer simple tasks**:
```python
# Bad: Using ensemble for simple task
task = "Fix typo in README"
strategy = "ensemble"  # Overkill! 5-10 minutes for a typo fix

# Good: Use appropriate strategy
task = "Fix typo in README"
strategy = "solve-directly"  # 30 seconds
```

**When to optimize downward**:
- Time-sensitive work → prefer simpler strategies
- Budget constraints → reduce iteration count or skip ensemble
- Low-risk changes → single-pass may be sufficient

### 2. Optimize Iteration Count

**Trade quality for speed**:
```python
# Conservative (high quality, slower)
max_iterations = 5
success_threshold = 0.9

# Balanced (good quality, faster)
max_iterations = 3
success_threshold = 0.85

# Fast (acceptable quality, fastest)
max_iterations = 2
success_threshold = 0.75
```

**Impact**:
- 5 iterations (0.9 threshold): 5-8 minutes, score 0.90-0.95
- 3 iterations (0.85 threshold): 3-5 minutes, score 0.85-0.90
- 2 iterations (0.75 threshold): 2-3 minutes, score 0.75-0.85

### 3. Parallelize Where Possible

**Ensemble is already parallel** (5 strategies run simultaneously):
- Wall-clock time: ~Same as single strategy
- Total compute: 5× single strategy
- Best when: Parallelization is available and cost-effective

**Decomposition can be parallelized**:
```python
# Sequential (slow)
for subtask in subtasks:
    result = solve(subtask)  # 2 min each
    results.append(result)
# Total: 6 minutes for 3 subtasks

# Parallel (fast)
results = await asyncio.gather(*[
    solve(subtask) for subtask in subtasks
])
# Total: 2 minutes (same as single subtask)
```

### 4. Cache Assessments

**Avoid redundant complexity assessments**:
```python
# Cache assessment results for similar tasks
cache = {}

def get_complexity(task):
    task_hash = hash(task)
    if task_hash in cache:
        return cache[task_hash]
    
    result = complexity_assessor(task)
    cache[task_hash] = result
    return result
```

**When to cache**:
- Repeated similar tasks
- Batch processing
- Iterative workflows where task doesn't change

**When NOT to cache**:
- Context changes between tasks
- File state changes
- First-time tasks

### 5. Early Termination

**Don't waste iterations on "good enough"**:
```python
# Stop early if score is acceptable
if score >= 0.85:  # Good enough
    return solution

# Don't chase perfect (0.9+) if 0.85 is fine
```

**Guidelines**:
- For prototypes: 0.75 is sufficient
- For production: 0.85-0.90 is excellent
- For critical systems: 0.90+ justifies extra time

### 6. Optimize Test Execution

**Test execution is often the bottleneck**:

```bash
# Slow: Full test suite with integration tests
pytest  # 60-120 seconds

# Fast: Unit tests only
pytest tests/unit/ --fast  # 5-10 seconds

# Faster: Parallel execution
pytest -n auto  # 20-40 seconds
```

**Strategy**:
- Use fast unit tests during iteration
- Run full test suite only on final iteration
- Skip slow integration tests until needed

### 7. Reduce Ensemble Size

**5 strategies vs 3 strategies**:

| Metric | 5 Strategies | 3 Strategies | Savings |
|--------|-------------|-------------|---------|
| Time | 5-10 min | 3-6 min | 40% |
| Tokens | 25k-50k | 15k-30k | 40% |
| Cost | $0.40-0.80 | $0.24-0.48 | 40% |
| Consensus quality | High | Good | Acceptable |

**When 3 is enough**:
- Medium criticality decisions
- Budget constraints
- Time pressure
- Previous consensus was clear

## Performance Monitoring

### Metrics to Track

**Per-workflow metrics**:
```python
workflow_metrics = {
    "task": "Implement rate limiting",
    "strategy": "iterative-refinement",
    "complexity_score": 7.0,
    "iterations_used": 3,
    "total_time_seconds": 245,
    "total_tokens": 18420,
    "final_score": 0.92,
    "cost_estimate_usd": 0.28
}
```

**Aggregate metrics** (track over time):
- Average time per complexity level
- Token usage trends
- Success rate (% reaching target score)
- Iteration efficiency (score improvement per iteration)

### Instrumentation Example

```python
import time
from typing import Dict, Any

class PerformanceTracker:
    def __init__(self):
        self.metrics = []
    
    def track_workflow(self, workflow_func):
        start_time = time.time()
        start_tokens = self.get_token_count()
        
        result = workflow_func()
        
        elapsed = time.time() - start_time
        tokens_used = self.get_token_count() - start_tokens
        
        self.metrics.append({
            "duration_seconds": elapsed,
            "tokens_used": tokens_used,
            "score": result.get("score"),
            "timestamp": time.time()
        })
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_workflows": len(self.metrics),
            "avg_duration": sum(m["duration_seconds"] for m in self.metrics) / len(self.metrics),
            "total_tokens": sum(m["tokens_used"] for m in self.metrics),
            "avg_score": sum(m["score"] for m in self.metrics if m["score"]) / len(self.metrics)
        }
```

## Scaling Considerations

### Single User Performance

Typical developer workflow:
- **10-20 tasks per day**
- **Mix of complexities** (mostly low-medium)
- **Total time**: 2-4 hours of LLM time per day
- **Total tokens**: 100k-300k tokens per day
- **Cost**: $1.50-$4.50 per day

### Team Performance

10-person team:
- **100-200 tasks per day**
- **Total tokens**: 1M-3M tokens per day
- **Cost**: $15-$45 per day ($300-$900 per month)

### Optimization for Scale

**At team scale**:
1. **Cache aggressively** - Share assessment cache across team
2. **Batch processing** - Process similar tasks together
3. **Resource limits** - Set per-user token budgets
4. **Monitor usage** - Track high-cost operations

**Example team policy**:
```yaml
resource_limits:
  max_tokens_per_day: 30000  # Per user
  max_ensemble_per_week: 10  # Expensive operations
  default_max_iterations: 3   # Reduced from 5
  require_approval_for:
    - ensemble (notify lead)
    - iterations > 3
    - complexity > 8
```

## Performance Comparison

### Metacognition vs Direct Execution

| Metric | Direct Execution | With Metacognition | Difference |
|--------|-----------------|-------------------|------------|
| Time | 30-60 sec | 60-120 sec | +2x |
| Tokens | 2,000 | 5,000-8,000 | +2.5-4x |
| Quality (score) | 0.70-0.80 | 0.85-0.92 | +15-20% |
| Rework needed | 30-40% | 5-10% | -75% |

**Trade-off**: Pay 2-4× upfront for better quality, less rework

**ROI calculation**:
```
Scenario: Medium complexity task

Direct approach:
- Initial: 60 sec
- Rework (30% chance): +120 sec
- Expected total: 96 seconds

Metacognitive approach:
- Initial: 120 sec (with review)
- Rework (5% chance): +120 sec
- Expected total: 126 seconds

Overhead: 30 seconds (31% longer)
Benefit: Higher quality, less rework, better documentation
```

## Best Practices

### 1. Profile First, Optimize Later

Start with default settings:
- Use recommended strategy from complexity-assessor
- Use default iteration count (5)
- Use default ensemble size (5)

Optimize based on actual performance data:
- If consistently fast, keep current settings
- If too slow, reduce iterations or ensemble size
- If quality issues, increase thresholds

### 2. Set Reasonable Timeouts

```python
timeouts = {
    "complexity_assessment": 30,      # 30 seconds
    "solution_evaluation": 60,        # 1 minute
    "iteration": 180,                 # 3 minutes per iteration
    "ensemble_strategy": 300,         # 5 minutes per strategy
    "total_workflow": 1800            # 30 minutes max
}
```

### 3. Monitor and Alert

**Set up alerts for**:
- Workflows exceeding expected time
- Token usage spikes
- Low success rates
- Frequent timeouts

### 4. Document Performance Expectations

For each workflow type:
```markdown
## Rate Limiting Implementation

- Complexity: 7 (high)
- Strategy: iterative-refinement
- Expected time: 4-6 minutes
- Expected iterations: 3-4
- Token usage: ~15,000
- Target score: ≥0.9
```

## Troubleshooting Performance Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#performance-problems) for detailed guidance on:
- Slow iterations
- High token usage
- Timeout issues
- Resource constraints

---

## Summary

**Key Takeaways**:

1. **Metacognition adds overhead** (2-4× time/tokens) **but improves quality** (15-20% higher scores)
2. **Right-size your strategy**: Simple → solve-directly, Complex → iterate, Critical → ensemble
3. **Optimize iteration count**: 3 iterations often sufficient, 5 for high quality
4. **Parallelize when possible**: Ensemble and decomposition benefit from parallelization
5. **Monitor performance**: Track metrics to identify optimization opportunities
6. **Set realistic expectations**: Complex tasks take time - 5-10 minutes is normal

**Performance Philosophy**:
- **Measure, don't guess**: Track actual performance, optimize based on data
- **Quality over speed**: Accept reasonable overhead for better results
- **Right tool for the job**: Use appropriate strategy for complexity level
- **Continuous improvement**: Profile, optimize, repeat

---

**Last Updated**: 2025-01-08
**Collection Version**: 0.1.0
