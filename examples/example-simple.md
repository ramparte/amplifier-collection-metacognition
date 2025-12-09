# Example: Simple Task (Low Complexity)

This example shows how the coordinator handles a simple task that doesn't need metacognitive agents.

## Task

"Fix typo in README.md line 42 - change 'teh' to 'the'"

## Coordinator Flow

```
Step 1: Assess complexity
User request is very specific and bounded.
Decision: Too simple to delegate to complexity-assessor
Action: Execute directly

Step 2: Fix typo
Read README.md
Find line 42: "This is teh main function"
Change to: "This is the main function"
Write back to file

Step 3: Verify
Read line 42 again: "This is the main function" ✓

Result: Fixed in <1 second
```

## When to Skip Metacognition

For tasks like this:
- Explicit location (line 42)
- Single atomic change (one typo)
- Clear success criteria (word corrected)
- Zero risk

**Rule of thumb**: If you can complete it in 5 seconds, just do it.

## Coordinator Reasoning

```
Complexity signals:
- Scope: Crystal clear (1/10)
- Novelty: None (1/10)
- Integration: Single file (1/10)
- Risk: Zero (1/10)

Estimated complexity: 1.0 → VERY LOW

Decision: solve-directly without delegation
```

This is the ideal case - metacognitive capabilities available but not needed for simple work.
