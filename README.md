# Amplifier Collection: Metacognition

**Metacognitive agents for adaptive problem-solving inspired by Poetiq's record-breaking ARC-AGI solver.**

This collection provides agents that reason about *how* to solve problems, not just solve them directly. Based on research from Poetiq's SOTA ARC-AGI approach, these agents enable:

- **Complexity assessment**: Judge if tasks are at a scale likely to succeed
- **Iterative refinement**: Multiple attempts with measured feedback (soft scoring)
- **Solution evaluation**: Objective scoring with detailed feedback
- **Ensemble consensus**: Parallel strategies with voting for critical decisions

## Quick Start

### Installation

```bash
# Install collection
amplifier collection add git+https://github.com/microsoft/amplifier-collection-metacognition@main

# Verify installation
amplifier collection list
amplifier collection show metacognition

# Use the metacognitive profile
amplifier profile use metacognitive
```

### Basic Usage

The metacognitive profile enables adaptive problem-solving:

```bash
# Start with metacognitive profile
amplifier profile use metacognitive

# The coordinator will automatically assess complexity and adapt strategy
amplifier run "Design and implement caching layer"

# Behind the scenes:
# 1. Delegates to complexity-assessor → score 7, "iterative-refinement"
# 2. Delegates to iterative-refiner → runs 3 iterations with feedback
# 3. Returns best solution with score 0.92
```

## What This Collection Provides

### 1. Metacognitive Agents

Four specialized agents that orchestrate problem-solving:

**complexity-assessor**
- Analyzes task complexity (1-10 scale)
- Recommends strategy: solve-directly, single-pass-with-review, iterative-refinement, ensemble, decompose
- Considers scope, novelty, integration points, success criteria

**iterative-refiner**
- Implements poetiq-style iterative refinement
- Soft scoring (0.0-1.0) tracks progress
- Learns from past attempts with rich feedback
- Terminates on success (score ≥ 0.9) or max iterations

**solution-evaluator**
- Objective evaluation across 4 dimensions
- Scores: correctness, completeness, quality, testability
- Detailed feedback with specific locations and suggestions
- Recommendations: accept, iterate, reject

**ensemble-coordinator**
- Runs multiple strategies in parallel
- Groups identical solutions (consensus)
- Votes on best solution
- High consensus = high confidence

### 2. Context Files

Three comprehensive guides:

- **poetiq-patterns.md**: Poetiq's metacognitive patterns from ARC-AGI research
- **complexity-signals.md**: How to assess task complexity
- **scoring-rubrics.md**: Detailed rubrics for solution evaluation

### 3. Metacognitive Profile

Pre-configured profile loading all agents with optimal settings.

## How It Works

### The Metacognitive Loop

```
Task → complexity-assessor → Strategy Recommendation
                              ↓
                    ┌─────────┴─────────┐
        solve-directly        iterative-refinement        ensemble
              ↓                       ↓                        ↓
           Execute             iterative-refiner     ensemble-coordinator
              ↓                       ↓                        ↓
      solution-evaluator              ↓                        ↓
              ↓                       ↓                        ↓
            Result ←──────────────────┴────────────────────────┘
```

### Example Flow: Medium Complexity Task

```
User: "Add logging to authentication module"

1. Coordinator delegates to complexity-assessor
   → Score: 4.0 (medium)
   → Recommendation: "single-pass-with-review"

2. Coordinator implements logging

3. Coordinator delegates to solution-evaluator
   → Score: 0.75 (good, some improvements needed)
   → Feedback: "Add structured logging, improve error messages"

4. Coordinator refines based on feedback

5. Coordinator evaluates again
   → Score: 0.92 (excellent)
   → Recommendation: "accept"

Result: High-quality implementation with objective validation
```

### Example Flow: High Complexity Task

```
User: "Design and implement caching layer"

1. Coordinator delegates to complexity-assessor
   → Score: 7.0 (high)
   → Recommendation: "iterative-refinement"

2. Coordinator delegates to iterative-refiner
   
   iterative-refiner orchestrates:
   - Iteration 1: Generate solution → evaluate → score 0.6
     Feedback: "Missing TTL support, no invalidation"
   
   - Iteration 2: Add TTL and invalidation → evaluate → score 0.8
     Feedback: "Good progress, but race conditions in concurrent access"
   
   - Iteration 3: Fix race conditions → evaluate → score 0.93
     Success! Return solution

3. Coordinator presents solution with confidence score

Result: Robust solution refined through measured iteration
```

### Example Flow: Critical Decision

```
User: "Design authentication architecture for microservices"

1. Coordinator delegates to complexity-assessor
   → Score: 9.0 (very high)
   → Recommendation: "ensemble"

2. Coordinator delegates to ensemble-coordinator
   
   ensemble-coordinator spawns 5 parallel strategies:
   - zen-architect (temp=0.3) → JWT + Redis
   - modular-builder (temp=0.5) → JWT + Redis  ← CONSENSUS
   - modular-builder (temp=0.7) → JWT + Redis  ←
   - bug-hunter (temp=0.3) → OAuth2 + DB
   - zen-architect (temp=0.7) → Stateless JWT

   Vote: 3 for JWT+Redis (60% consensus)
   Confidence: HIGH

3. Coordinator returns consensus solution with rationale

Result: Robust decision backed by multiple independent analyses
```

## Poetiq's Inspiration

This collection is inspired by Poetiq's record-breaking ARC-AGI solver:
- **SOTA Results**: Achieved state-of-the-art on ARC-AGI-1 and ARC-AGI-2 benchmarks
- **Iterative Refinement**: Generate → Evaluate → Refine → Repeat
- **Soft Scoring**: Track progress with 0.0-1.0 scores (not just pass/fail)
- **Rich Feedback**: Detailed, actionable critique guides improvement
- **Parallel Exploration**: Multiple experts vote on best solution

**Key Insight**: Don't predict success upfront → measure and adapt in real-time.

See [poetiq-patterns.md](context/poetiq-patterns.md) for complete details.

## Agent Details

### complexity-assessor

**Purpose**: Assess task complexity and recommend strategy

**Inputs**:
- Task description
- Available context (files, systems, etc.)

**Outputs**:
```json
{
  "complexity_score": 7.0,
  "confidence": 0.85,
  "recommendation": "iterative-refinement",
  "reasoning": "Novel architecture with multiple integration points...",
  "suggested_strategy": {
    "approach": "decompose-then-iterate",
    "substeps": [...],
    "estimated_iterations": 3
  }
}
```

**When to use**: Before starting any non-trivial task

### iterative-refiner

**Purpose**: Implement poetiq-style iterative refinement

**Inputs**:
- Task to solve
- Max iterations (default: 5)
- Success threshold (default: 0.9)

**Outputs**:
```json
{
  "iteration": 3,
  "solution": "...",
  "self_score": 0.92,
  "breakdown": {
    "correctness": 0.95,
    "completeness": 0.90,
    "quality": 0.92,
    "clarity": 0.90
  },
  "history": [...],
  "best_iteration": 3
}
```

**When to use**: Novel work, creative tasks, complex implementations

### solution-evaluator

**Purpose**: Objective evaluation with detailed feedback

**Inputs**:
- Solution (code/design/implementation)
- Requirements

**Outputs**:
```json
{
  "overall_score": 0.85,
  "scores": {
    "correctness": 0.9,
    "completeness": 0.8,
    "quality": 0.85,
    "testability": 0.85
  },
  "strengths": ["Clean separation of concerns", "..."],
  "weaknesses": [
    {
      "issue": "Missing null validation",
      "location": "auth.py:23",
      "severity": "high",
      "suggestion": "Add guard clause"
    }
  ],
  "recommendation": "iterate"
}
```

**When to use**: After completing medium+ complexity tasks, or to evaluate iterative-refiner's output

### ensemble-coordinator

**Purpose**: Parallel strategy exploration with voting

**Inputs**:
- Problem requiring multiple perspectives
- Number of strategies (default: 5)
- Agent/temperature diversity settings

**Outputs**:
```json
{
  "strategies_tried": 5,
  "consensus_groups": [
    {
      "solution_id": "A",
      "vote_count": 3,
      "agents": ["zen-architect", "modular-builder", "..."],
      "quality_score": 0.85,
      "solution": "..."
    }
  ],
  "recommendation": {
    "selected_solution": "A",
    "confidence": 0.9,
    "reasoning": "60% consensus with high quality score"
  }
}
```

**When to use**: Critical decisions, architectural choices, high-stakes work

## Integration with Standard Agents

Metacognitive agents work alongside standard Amplifier agents:

```yaml
agents:
  # Standard agents (if you have them)
  - zen-architect
  - modular-builder
  - bug-hunter
  
  # Metacognitive agents (from this collection)
  - complexity-assessor
  - iterative-refiner
  - solution-evaluator
  - ensemble-coordinator
```

**Use cases**:
- Use complexity-assessor to decide which standard agent to use
- Use iterative-refiner to orchestrate multiple attempts by standard agents
- Use ensemble-coordinator to get consensus from multiple standard agents
- Use solution-evaluator to assess standard agents' work

## Best Practices

### When to Use Metacognition

**DO use for**:
- Novel or creative work
- Critical decisions (architecture, security)
- Complex multi-step tasks
- When quality bar is high

**DON'T use for**:
- Simple, routine tasks (overhead not worth it)
- Time-sensitive work (adds latency)
- Well-defined, pattern-based work

### Resource Management

**Complexity assessment**: Fast, always worth it (~5s)
**Iterative refinement**: Medium cost (N iterations × task time)
**Solution evaluation**: Fast (~10s per evaluation)
**Ensemble coordination**: High cost (N parallel strategies)

Use ensemble sparingly - only for critical decisions worth the cost.

### Score Interpretation

**0.9-1.0**: Excellent, ship it
**0.7-0.9**: Good, minor iteration recommended
**0.5-0.7**: Acceptable, needs iteration
**0.3-0.5**: Poor, major rework
**0.0-0.3**: Unacceptable, try different approach

Be honest with scores - 0.6 is okay and means "needs work."

## Examples

See the [examples/](examples/) directory for complete working examples:

- **example-simple.md**: Low complexity task
- **example-medium.md**: Medium complexity with review
- **example-complex.md**: High complexity with iteration
- **example-critical.md**: Critical decision with ensemble

## Philosophy

This collection embodies Amplifier's core principles:

**Ruthless Simplicity**: Agents are markdown files, no complex orchestration code
**Measurement Over Prediction**: Use soft scoring to track actual progress
**Present-Moment Focus**: Solve current problems, don't future-proof
**Code for Structure, AI for Intelligence**: Agents think, you orchestrate

**From Poetiq**:
- Don't guess if you'll succeed → measure and adapt
- Rich feedback enables learning
- Parallel exploration reduces bias
- Consensus = confidence

## Contributing

Found a pattern that works well? Improve the scoring rubrics? Share!

This collection welcomes contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - See [LICENSE](LICENSE)

## Acknowledgments

Inspired by Poetiq's groundbreaking work on ARC-AGI:
- Blog: https://poetiq.ai/posts/arcagi_announcement/
- Code: https://github.com/poetiq-ai/poetiq-arc-agi-solver
- Paper: "Traversing the Frontier of Superintelligence"

## Version

**Collection Version**: 0.1.0  
**Last Updated**: 2025-01-08

---

**Ready to get started?**

```bash
amplifier collection add git+https://github.com/microsoft/amplifier-collection-metacognition@main
amplifier profile use metacognitive
amplifier run "Your complex task here"
```

Let the agents reason about how to solve your problems!
