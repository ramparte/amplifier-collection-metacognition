# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the metacognition collection.

## Table of Contents

- [Complexity Assessment Issues](#complexity-assessment-issues)
- [Evaluation Problems](#evaluation-problems)
- [Iteration Not Converging](#iteration-not-converging)
- [Ensemble Issues](#ensemble-issues)
- [Performance Problems](#performance-problems)
- [Integration Issues](#integration-issues)

---

## Complexity Assessment Issues

### Problem: Complexity assessor returns null score

**Symptoms**:
```json
{
  "complexity_score": null,
  "confidence": 0.0,
  "recommendation": "cannot-assess"
}
```

**Causes**:
1. Missing required context files
2. Task description too vague
3. Unable to access codebase

**Solutions**:

**If missing context**:
```bash
# Ensure files mentioned in task are accessible
ls path/to/mentioned/files

# Provide explicit file list in task description
"Analyze auth.py, user.py, and session.py for complexity"
```

**If task is vague**:
- Add specific details: "Add logging" → "Add structured logging to authentication module (auth.py) with INFO and ERROR levels"
- Specify scope: "Improve performance" → "Optimize database queries in UserService.get_all() method"
- Define success criteria: "Make it better" → "Reduce response time from 500ms to <100ms"

**If assessment confidence is low (<0.5)**:
- Answer the clarifying questions provided
- Break down ambiguous requirements
- Provide examples of desired outcome

---

### Problem: Assessment recommends wrong strategy

**Symptoms**:
- Simple task gets "ensemble" recommendation
- Complex task gets "solve-directly" recommendation

**Debugging**:

1. **Check task description**:
   - Is it clear and specific?
   - Does it mention multiple concerns? (inflates complexity)
   - Does it use ambiguous words like "improve", "optimize"?

2. **Review complexity score**:
   ```
   Score 1-3: Should recommend "solve-directly"
   Score 4-6: Should recommend "single-pass-with-review"
   Score 7-8: Should recommend "iterative-refinement"
   Score 9-10: Should recommend "ensemble" or "decompose"
   ```

3. **Override if needed**:
   - If assessment seems wrong, you can manually choose strategy
   - Document why you overrode the recommendation

**Example override**:
```
Assessment says: complexity 9, ensemble
Your judgment: Task is urgent, use iterative-refinement instead
Action: "I'm using iterative refinement instead of ensemble due to time constraints"
```

---

## Evaluation Problems

### Problem: Solution evaluator returns null scores

**Symptoms**:
```json
{
  "overall_score": null,
  "recommendation": "cannot-evaluate",
  "error": {
    "type": "file_access_error"
  }
}
```

**Solutions**:

**File access errors**:
```bash
# Check files exist
ls path/to/solution/files

# Check permissions
chmod +r path/to/files

# Verify paths are correct (absolute vs relative)
pwd  # Check current directory
```

**Test execution failures**:
```bash
# Run tests manually to diagnose
pytest path/to/tests -v

# Check for:
# - Missing dependencies
# - Incorrect test paths
# - Test environment issues
```

**Quick fix**: Use partial evaluation
```json
{
  "overall_score": 0.5,  # Partial score
  "scores": {
    "correctness": null,     # Tests didn't run
    "completeness": 0.6,     # Can assess from code
    "quality": 0.7,          # Can assess from code
    "testability": 0.3       # Can assess from code
  }
}
```

---

### Problem: Scores seem inconsistent

**Symptoms**:
- Similar solutions get very different scores
- Scores don't match your intuition

**Debugging**:

1. **Check evaluation criteria**:
   - Review `context/scoring-rubrics.md`
   - Ensure evaluator has access to requirements
   - Verify success criteria are clear

2. **Compare detailed feedback**:
   ```json
   {
     "weaknesses": [
       {
         "issue": "Missing null validation",
         "location": "auth.py:23",
         "severity": "high"
       }
     ]
   }
   ```

3. **Calibrate expectations**:
   ```
   0.9-1.0: Perfect (rare)
   0.7-0.9: Good (most production code)
   0.5-0.7: Acceptable (needs work)
   0.3-0.5: Poor (major issues)
   0.0-0.3: Unacceptable
   ```

**If scores still seem off**:
- Manually review the solution
- Check if evaluator has all context
- Consider if requirements were clear

---

## Iteration Not Converging

### Problem: Scores plateau before reaching 0.9

**Symptoms**:
```
Iteration 1: 0.60
Iteration 2: 0.75
Iteration 3: 0.82
Iteration 4: 0.82
Iteration 5: 0.82  ← Stuck
```

**Causes**:
1. Approach is fundamentally flawed
2. Task is harder than estimated
3. Requirements are contradictory
4. Reaching limits of what's possible

**Solutions**:

**1. Try different approach**:
```
Current approach: Nested conditionals
New approach: Strategy pattern
```

**2. Decompose the task**:
```
Original: "Implement caching with TTL and invalidation"
Decomposed:
  - Subtask 1: Basic caching (get/set)
  - Subtask 2: Add TTL support
  - Subtask 3: Add invalidation
```

**3. Accept "good enough"**:
- 0.82 is "good" (0.7-0.9 range)
- Consider shipping and iterating later
- Perfect (0.9+) may not be necessary

**4. Get human review**:
- Present current solution to user
- Ask if 0.82 quality is acceptable
- Get specific feedback on what to improve

---

### Problem: Max iterations reached with low score

**Symptoms**:
```
Iteration 5: Score 0.55
Status: max_iterations_reached
```

**This means**: Task is too complex for iterative approach

**Solutions**:

**1. Decompose into subtasks**:
```python
# Instead of: "Build authentication system"
subtasks = [
    "Implement JWT token generation",
    "Implement token validation",
    "Implement refresh token logic",
    "Add token storage/retrieval"
]
# Solve each with iteration
```

**2. Simplify requirements**:
```
Original: "Add caching with TTL, invalidation, warming, metrics"
Simplified: "Add basic caching with TTL only"
# Add other features later
```

**3. Use ensemble for complex design decisions**:
```
If stuck on: "How should authentication work?"
Use ensemble to get multiple perspectives
Then implement the consensus approach
```

---

## Ensemble Issues

### Problem: No consensus (all strategies different)

**Symptoms**:
```json
{
  "consensus_groups": [
    {"solution_id": "A", "vote_count": 1},
    {"solution_id": "B", "vote_count": 1},
    {"solution_id": "C", "vote_count": 1},
    {"solution_id": "D", "vote_count": 1},
    {"solution_id": "E", "vote_count": 1}
  ],
  "recommendation": {
    "confidence": 0.2
  }
}
```

**This means**: Problem has many valid approaches OR requirements are unclear

**Solutions**:

**1. Clarify requirements**:
```
Vague: "Design authentication"
Clear: "Design JWT-based authentication with Redis session store"
```

**2. Present top options to user**:
```
"5 strategies produced different solutions:
- Option A: JWT + Redis (fastest)
- Option B: OAuth2 + DB (most secure)
- Option C: Stateless JWT (simplest)

Which aligns best with your priorities?"
```

**3. Use quality scores as tiebreaker**:
```python
# If no consensus, pick highest quality
best_solution = max(solutions, key=lambda x: x['quality_score'])
```

---

### Problem: Some ensemble strategies fail

**Symptoms**:
```json
{
  "strategies_tried": 5,
  "strategies_succeeded": 2,
  "strategies_failed": 3
}
```

**Causes**:
1. Timeout (strategies take too long)
2. Resource limits
3. Task too complex for some configurations

**Solutions**:

**If timeouts**:
```
# Increase timeout per strategy
timeout: 60s → 120s

# Or reduce strategy count
strategies: 5 → 3

# Or simplify task
```

**If resource limits**:
```bash
# Check resource usage
top  # CPU/memory
df -h  # Disk space

# Reduce concurrent strategies
# Run sequentially if needed
```

**If partial success (≥2 succeeded)**:
- Use successful strategies
- Note reduced confidence
- Consider rerunning failed strategies with more resources

**If complete failure (all failed)**:
- Task is too complex
- Decompose into smaller decisions
- Consider single-pass approach instead

---

## Performance Problems

### Problem: Iteration takes too long

**Symptoms**:
- Each iteration takes >5 minutes
- Total workflow exceeds 30 minutes

**Solutions**:

**1. Profile where time is spent**:
```
Typical breakdown:
- Generation: 20-30% (LLM call)
- Execution: 30-40% (running tests)
- Evaluation: 30-40% (LLM call)
```

**2. Optimize slow parts**:

**If test execution is slow**:
```bash
# Run only fast unit tests, skip integration
pytest tests/unit/ --fast

# Use parallel test execution
pytest -n auto
```

**If evaluation is slow**:
```
# Use simpler evaluation criteria
# Skip comprehensive analysis for quick iterations
```

**3. Reduce iteration count**:
```
max_iterations: 5 → 3
# Quality may be slightly lower (0.85 vs 0.92)
# But much faster
```

**4. Use early termination**:
```python
if score >= 0.85:  # Instead of 0.9
    return "Good enough for now"
```

---

### Problem: Ensemble is too expensive

**Symptoms**:
- High token usage (>50k tokens)
- Long wall-clock time (>10 minutes)
- High API costs

**Solutions**:

**1. Reduce strategy count**:
```
strategies: 5 → 3
# Still gets useful consensus
# 40% cheaper and faster
```

**2. Use ensemble sparingly**:
```
Only for:
- Critical architecture decisions
- High-stakes choices
- When single approach has failed

NOT for:
- Routine tasks
- Time-sensitive work
- Budget constraints
```

**3. Consider alternatives**:
```
Instead of ensemble:
- Use iterative-refinement (one strategy, multiple attempts)
- Use single-pass-with-review (faster)
- Decompose and parallelize subtasks
```

---

## Integration Issues

### Problem: Agents not found or can't load

**Symptoms**:
```
Error: Agent not found: @metacognition:agents/complexity-assessor.md
```

**Solutions**:

**1. Verify installation**:
```bash
amplifier collection list
# Should show: metacognition

amplifier collection show metacognition
# Should list all 4 agents
```

**2. Reinstall if needed**:
```bash
amplifier collection remove metacognition
amplifier collection add git+https://github.com/microsoft/amplifier-collection-metacognition@main
```

**3. Check file paths**:
```bash
# Agents should be in:
ls ~/.amplifier/collections/metacognition/agents/
# Should show: complexity-assessor.md, ensemble-coordinator.md, etc.
```

---

### Problem: Profile not activating correctly

**Symptoms**:
- Metacognitive agents not available
- Profile shows different agents

**Solutions**:

**1. Activate profile**:
```bash
amplifier profile use metacognitive
amplifier profile show  # Verify active profile
```

**2. Check profile configuration**:
```bash
# Profile should inherit from 'dev' and include metacognitive agents
cat ~/.amplifier/collections/metacognition/profiles/metacognitive.md
```

**3. Reload Amplifier**:
```bash
# Restart Amplifier session
# Profile should auto-load on start
```

---

## Getting More Help

### Diagnosis Checklist

Run through this checklist when troubleshooting:

- [ ] Are all collection files present?
- [ ] Is the correct profile active?
- [ ] Are file paths correct (absolute vs relative)?
- [ ] Do tests run independently?
- [ ] Are requirements clear and specific?
- [ ] Is there enough context for agents?
- [ ] Are resource limits being hit (time, tokens)?
- [ ] Have you tried simplifying the task?

### Enable Debug Mode

```bash
# Set environment variable for verbose output
export AMPLIFIER_DEBUG=1

# Run your command
amplifier run "your task"

# Check debug logs
tail -f ~/.amplifier/logs/debug.log
```

### Collect Information for Bug Reports

When reporting issues, include:

1. **Task description**: Exact task given to agents
2. **Agent output**: Full JSON responses
3. **Error messages**: Complete error text
4. **Environment**: Amplifier version, OS, Python version
5. **Collection version**: `amplifier collection show metacognition`
6. **Steps to reproduce**: Minimal example that demonstrates issue

### Community Support

- **GitHub Issues**: https://github.com/microsoft/amplifier-collection-metacognition/issues
- **Discussions**: https://github.com/microsoft/amplifier-collection-metacognition/discussions
- **Documentation**: See README.md and context/ files

---

## Common Patterns

### Quick Reference: Error → Solution

| Error | Solution |
|-------|----------|
| null complexity_score | Clarify requirements, provide context |
| Low confidence (<0.5) | Answer clarifying questions |
| Evaluation fails | Check file access, run tests manually |
| Score plateau | Try different approach or decompose |
| Max iterations reached | Decompose task or simplify |
| No ensemble consensus | Clarify requirements or present options |
| Ensemble failures | Reduce strategies or increase timeout |
| Slow iterations | Optimize tests or reduce iteration count |
| Agent not found | Reinstall collection, check profile |

### Quick Reference: When to Use What

| Situation | Use This |
|-----------|----------|
| Assessment unclear | Ask user for clarification |
| Score < 0.5 | Consider different approach |
| Score plateaus at 0.7-0.8 | Accept as "good enough" or decompose |
| Max iterations with low score | Decompose into subtasks |
| No consensus in ensemble | Present top 2-3 options to user |
| Partial ensemble failure (≥2 success) | Use successful results |
| Complete ensemble failure | Decompose or use simpler approach |
| Iteration too slow | Reduce iteration count or simplify |
| Ensemble too expensive | Use iterative-refinement instead |

---

**Last Updated**: 2025-01-08
**Collection Version**: 0.1.0
