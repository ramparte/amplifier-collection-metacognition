# Poetiq's Metacognitive Patterns

This document summarizes the key metacognitive patterns from Poetiq's record-breaking ARC-AGI solver.

**Source**: https://github.com/poetiq-ai/poetiq-arc-agi-solver

## Overview

Poetiq achieved state-of-the-art results on ARC-AGI benchmarks using a metacognitive approach that:
- Measures progress rather than predicting success
- Iterates with rich feedback
- Explores solutions in parallel
- Votes on consensus

## Core Patterns

### 1. Iterative Refinement with Soft Scoring

**Problem**: Binary pass/fail doesn't track progress toward solution.

**Solution**: Score partial success on 0.0-1.0 scale.

```python
def soft_score(prediction, truth):
    if shapes_dont_match:
        return 0.0
    return percent_cells_correct  # 0.0 to 1.0
```

**Key Insight**: Even failed solutions provide signal. A 0.6 score means "60% correct, getting closer."

**Iteration Loop**:
```
1. Generate solution (code/design/implementation)
2. Execute/evaluate against test cases
3. Compute soft score (% correct)
4. Build detailed feedback (what's wrong, where, why)
5. Add to solution history with score
6. Sample best solutions from history
7. Generate next attempt incorporating feedback
8. Repeat until score >= 0.9 OR max iterations
```

### 2. Rich Feedback Generation

**Problem**: "Wrong answer" doesn't help LLM improve.

**Solution**: Detailed, actionable feedback for each failure.

**Feedback Structure**:
```python
feedback = {
    "example_1": {
        "status": "failed",
        "your_output": [[0, 1], [1, 0]],
        "expected": [[1, 0], [0, 1]],
        "diff_visualization": "0/1 1/0\n1/0 0/1",
        "shape_match": True,
        "accuracy": 0.0,  # 0% cells correct
        "error": None
    },
    "example_2": {
        "status": "passed",
        "accuracy": 1.0
    }
}
```

**Key Principle**: Show exactly what's wrong, where, and how close they got.

### 3. Solution History & Learning

**Problem**: Each attempt starts from scratch, doesn't learn from past failures.

**Solution**: Maintain history of attempts with scores, show LLM its own evolution.

```python
solutions_history = [
    {"code": "...", "score": 0.4, "feedback": "Shape mismatch"},
    {"code": "...", "score": 0.6, "feedback": "Close, but rotated wrong"},
    {"code": "...", "score": 0.8, "feedback": "Minor edge case issue"}
]

# Sample best solutions (probabilistic)
selected = sample(solutions_history, p=selection_probability)

# Show to LLM as examples
prompt += format_examples(selected)  # Shows past attempts + feedback
```

**Key Insight**: LLM learns from its own mistakes when shown history.

### 4. Parallel Expert Consensus

**Problem**: Single attempt might miss the best solution due to randomness.

**Solution**: Run multiple solving strategies in parallel, vote on best.

**Poetiq's Approach**:
```python
# Run N experts in parallel
expert_configs = [
    {"seed": 0, "temp": 0.7, "prompt": PROMPT_1},
    {"seed": 100, "temp": 0.7, "prompt": PROMPT_1},
    {"seed": 200, "temp": 0.7, "prompt": PROMPT_2},
    # ... N experts
]

results = await asyncio.gather(*[
    solve_coding(config) for config in expert_configs
])

# Vote: group identical outputs
consensus_groups = group_by_identical_output(results)

# Rank by vote count (diversity-first)
ranked = sorted(consensus_groups, key=len, reverse=True)

# Return top consensus solution
best = ranked[0][0]  # First solution from largest group
```

**Voting Logic**:
1. **Identical outputs** = consensus (high confidence)
2. **Group by identity**, rank by vote count
3. **Diversity-first**: One solution per group
4. **Tiebreaker**: Use soft scores for failed solutions

**Example**:
```
5 experts run in parallel:
- Expert 1, 2, 3: Same solution A → 3 votes
- Expert 4: Solution B → 1 vote  
- Expert 5: Solution C → 1 vote

Result: Solution A wins (60% consensus)
Confidence: HIGH
```

### 5. Dynamic Resource Management

**Problem**: Don't know in advance how many iterations needed.

**Solution**: Budget-based execution with early termination.

```python
config = {
    "max_iterations": 10,
    "max_total_time": 300,  # 5 minutes per problem
    "max_total_timeouts": 15,
    "per_iteration_retries": 2,
}

for iteration in range(max_iterations):
    try:
        response = await llm(
            prompt,
            max_remaining_time=max_total_time,
            max_remaining_timeouts=max_total_timeouts
        )
        max_total_time -= elapsed
        max_total_timeouts -= (1 if timeout else 0)
        
    except BudgetExceeded:
        break  # Time/timeout budget exhausted
    
    if all_training_correct:
        return solution  # Early success
```

**Key Principles**:
- **Time budget**: Stop if taking too long
- **Timeout budget**: Stop if too many API failures
- **Early termination**: Stop on success (score >= threshold)
- **Best tracking**: Always keep best-so-far

### 6. Configuration Diversity

**Problem**: Single config might not be optimal for all problems.

**Solution**: Scale expert count and diversity for cost/performance trade-off.

**Poetiq's Scaling**:
```
Poetiq-1: 1 expert, 10 iterations  → Fast, cheap
Poetiq-2: 2 experts, 10 iterations → Better accuracy
Poetiq-3: 8 experts, 10 iterations → SOTA accuracy
```

**Diversity Strategies**:
- Different seeds (different random sampling)
- Different temperatures (0.3 conservative, 0.7 exploratory)
- Different prompts (analytical vs creative framing)
- Different models (Gemini vs GPT vs Claude)

## Application to Software Tasks

### Code Generation

```
Task: "Implement caching layer"

1. Generate initial implementation (iteration 1)
2. Evaluate: Run tests, check coverage, review code
3. Soft score: 0.6 (works but missing edge cases)
4. Feedback: "No cache invalidation, no TTL support"
5. Iteration 2: Add invalidation and TTL
6. Soft score: 0.85 (good, minor issues)
7. Iteration 3: Fix minor issues
8. Soft score: 0.95 → SUCCESS
```

### Architecture Design

```
Task: "Design authentication system"

Parallel Experts:
1. zen-architect (conservative) → JWT + Redis
2. modular-builder (balanced) → JWT + Redis  ← CONSENSUS
3. modular-builder (exploratory) → JWT + Redis ←
4. bug-hunter (security-first) → OAuth2 + DB
5. researcher (innovative) → Stateless JWT only

Voting: 3 for JWT+Redis (60% consensus)
Confidence: HIGH
Result: JWT with Redis sessions
```

### Debugging

```
Task: "Fix bug in authentication"

1. Analyze error (iteration 1)
2. Hypothesis: Token validation failing
3. Soft score: 0.3 (partial understanding)
4. Test fix, still broken
5. Iteration 2: Deeper investigation
6. Hypothesis: Race condition in Redis
7. Soft score: 0.7 (found root cause)
8. Iteration 3: Fix race condition
9. Soft score: 1.0 → FIXED
```

## Key Takeaways

**For Amplifier Integration**:

1. ✅ **Use soft scoring**: Track progress, not just pass/fail
2. ✅ **Rich feedback**: Specific, actionable critique
3. ✅ **Iteration history**: Show LLM its own evolution
4. ✅ **Parallel exploration**: Multiple strategies for critical decisions
5. ✅ **Budget management**: Time/iteration limits with early termination
6. ✅ **Consensus voting**: Identical outputs = high confidence

**What Poetiq Teaches Us**:
- Don't predict success upfront → measure and adapt
- Partial progress is valuable signal
- LLMs can self-improve with good feedback
- Parallel = robustness through diversity
- Code orchestrates, LLM thinks

## References

- Poetiq Blog: https://poetiq.ai/posts/arcagi_announcement/
- GitHub: https://github.com/poetiq-ai/poetiq-arc-agi-solver
- ARC-AGI Benchmark: https://arcprize.org/
