# Example: Medium Task (Single-Pass with Review)

This example shows how complexity-assessor and solution-evaluator work together for medium complexity tasks.

## Task

"Add structured logging to the authentication module (auth.py)"

## Coordinator Flow

### Step 1: Assess Complexity

```
Coordinator: Let me delegate to complexity-assessor to understand this task.

[Delegates to complexity-assessor]

Input: 
  Task: "Add structured logging to authentication module"
  Context: auth.py exists, currently uses print statements

complexity-assessor analyzes:
  - Scope: Clear (add logging) but needs decisions (what to log, format)
  - Novelty: Familiar (standard logging pattern)
  - Integration: Affects one module, needs to fit existing patterns
  - Success Criteria: Somewhat clear ("adequate logging")
  - Context: Need to read auth.py structure
  - Risk: Moderate (auth is critical)

Output:
{
  "complexity_score": 4.5,
  "confidence": 0.8,
  "recommendation": "single-pass-with-review",
  "reasoning": "Task is well-defined but requires judgment on what to log. 
               Authentication is critical so needs review. Familiar pattern 
               but module-specific decisions needed.",
  "suggested_strategy": {
    "approach": "implement-then-evaluate",
    "steps": [
      "Read existing auth.py structure",
      "Identify key decision points to log",
      "Implement structured logging with context",
      "Get evaluation from solution-evaluator",
      "Refine based on feedback if needed"
    ]
  }
}
```

### Step 2: Implementation

```
Coordinator: Following the single-pass-with-review strategy.

[Reads auth.py]
Structure identified:
- login(username, password)
- validate_token(token)
- refresh_token(token)
- logout(session_id)

[Implements logging]
Added structured logging at:
- Function entry (with sanitized parameters)
- Success paths (with session info)
- Error paths (with error details)
- Performance timing

Used Python's structlog for:
- JSON output
- Correlation IDs
- Context propagation
- PII sanitization (passwords masked)
```

### Step 3: Evaluation

```
Coordinator: Implementation complete. Now delegating to solution-evaluator.

[Delegates to solution-evaluator]

Input:
  Solution: Modified auth.py with logging
  Requirements: Structured logging for authentication

solution-evaluator analyzes:

Correctness (0.85):
  ✓ All functions have logging
  ✓ Error cases logged
  ✓ No crashes or syntax errors
  ⚠️ Missing logging for token refresh path

Completeness (0.80):
  ✓ Entry/exit logging present
  ✓ Error logging comprehensive
  ⚠️ Missing performance metrics in some paths
  ⚠️ No log level configuration

Quality (0.90):
  ✓ Clean implementation
  ✓ PII properly sanitized
  ✓ Correlation IDs propagate
  ✓ Good structure

Testability (0.75):
  ✓ Can test log output
  ⚠️ No tests added yet
  ⚠️ Mock setup could be cleaner

Output:
{
  "overall_score": 0.825,
  "scores": {...},
  "strengths": [
    "Proper PII sanitization (passwords never logged)",
    "Good use of correlation IDs for tracing",
    "Clean structured format with JSON output"
  ],
  "weaknesses": [
    {
      "issue": "Missing logging in refresh_token() function",
      "location": "auth.py:67 (refresh_token function)",
      "severity": "medium",
      "suggestion": "Add entry/exit logs with session_id context"
    },
    {
      "issue": "No configuration for log levels",
      "location": "auth.py:top",
      "severity": "low",
      "suggestion": "Add config param or env var for log level control"
    }
  ],
  "recommendation": "iterate",
  "next_steps": [
    "Add logging to refresh_token()",
    "Add log level configuration",
    "Add tests for log output"
  ]
}
```

### Step 4: Refinement

```
Coordinator: Score is 0.825 (good but needs refinement). 
             Implementing suggested improvements.

[Makes changes]
1. Added logging to refresh_token()
2. Added LOG_LEVEL config via environment variable
3. Added basic test asserting log entries

[Re-evaluates]
New score: 0.92

solution-evaluator:
{
  "overall_score": 0.92,
  "recommendation": "accept",
  "reasoning": "All major issues addressed. Production-ready."
}
```

### Step 5: Result

```
Coordinator: Structured logging successfully added with score 0.92.

Summary:
- Initial implementation: 0.825 (good)
- Refinement based on feedback
- Final score: 0.92 (excellent)
- Total iterations: 2
```

## Key Takeaways

1. **complexity-assessor saves time**: Immediately identified this as "implement-then-evaluate"
2. **solution-evaluator provides specifics**: Not just "needs improvement" but exact locations and suggestions
3. **Score guides iteration**: 0.825 clearly meant "iterate once", not "ship it" or "start over"
4. **Two iterations sufficient**: From working to excellent in one refinement cycle

## Without Metacognition

Without these agents:
- Might over-engineer (thinking it's more complex than it is)
- Might under-deliver (not getting objective feedback)
- Less clear when "good enough"
- No structured improvement process

## Coordinator Decision Logic

```python
if complexity_score < 3:
    solve_directly()
elif complexity_score < 6:
    implement_then_evaluate()  # This case
elif complexity_score < 8:
    use_iterative_refinement()
else:
    use_ensemble_or_decompose()
```

This medium complexity hit the sweet spot: one implementation pass + evaluation + refinement = excellent result.
