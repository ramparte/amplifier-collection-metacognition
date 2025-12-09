# Scoring Rubrics for Solution Evaluation

Detailed rubrics for evaluating solutions across multiple dimensions.

## Overview

All scores use 0.0-1.0 scale where:
- **1.0**: Perfect, no improvements needed
- **0.8-0.9**: Excellent, minor polish only
- **0.6-0.8**: Good, some improvements needed
- **0.4-0.6**: Acceptable, significant improvements needed
- **0.2-0.4**: Poor, major rework required
- **0.0-0.2**: Unacceptable, start over

## Dimension 1: Correctness

**Definition**: Does the solution solve the stated problem without bugs?

### Scoring Rubric

**1.0 - Perfect**:
- ✅ Solves problem completely
- ✅ All test cases pass (if applicable)
- ✅ No bugs or logical errors
- ✅ Handles all edge cases correctly
- ✅ Produces correct output in all scenarios

**0.8 - Excellent**:
- ✅ Solves problem for all main cases
- ✅ 95%+ test cases pass
- ⚠️ Minor edge case issues (e.g., null handling)
- ✅ Core logic is sound

**0.6 - Good**:
- ✅ Solves problem for typical cases
- ⚠️ 80-90% test cases pass
- ⚠️ Some edge cases fail
- ⚠️ Minor bugs in non-critical paths

**0.4 - Acceptable**:
- ⚠️ Solves problem partially
- ⚠️ 50-80% test cases pass
- ❌ Significant bugs in edge cases
- ⚠️ Core logic mostly works

**0.2 - Poor**:
- ❌ Barely works
- ❌ <50% test cases pass
- ❌ Fundamental logic errors
- ❌ Fails for common cases

**0.0 - Unacceptable**:
- ❌ Doesn't solve the problem
- ❌ Critical bugs prevent functionality
- ❌ Fundamentally wrong approach

### Evaluation Questions

1. Does it produce correct output for main use cases?
2. Do all tests pass?
3. Are edge cases handled?
4. Are there any bugs or errors?
5. Would this work in production?

## Dimension 2: Completeness

**Definition**: Are all requirements addressed?

### Scoring Rubric

**1.0 - Perfect**:
- ✅ All stated requirements met
- ✅ All implied requirements addressed
- ✅ Documentation complete
- ✅ Tests comprehensive
- ✅ Nothing missing

**0.8 - Excellent**:
- ✅ All explicit requirements met
- ✅ Most implied requirements addressed
- ⚠️ Minor documentation gaps
- ✅ Tests cover main scenarios

**0.6 - Good**:
- ✅ Core requirements met
- ⚠️ Some features missing
- ⚠️ Documentation incomplete
- ⚠️ Test coverage gaps

**0.4 - Acceptable**:
- ⚠️ Major requirements met
- ❌ Several features missing
- ❌ Minimal documentation
- ❌ Limited test coverage

**0.2 - Poor**:
- ❌ Many requirements unmet
- ❌ Significant functionality missing
- ❌ No documentation
- ❌ No tests

**0.0 - Unacceptable**:
- ❌ Most requirements ignored
- ❌ Core functionality missing
- ❌ Unusable incomplete state

### Evaluation Questions

1. Are all explicit requirements addressed?
2. Are implied requirements handled?
3. Is documentation present and adequate?
4. Is test coverage sufficient?
5. Is anything obviously missing?

## Dimension 3: Quality

**Definition**: Does it follow best practices and philosophy?

### Scoring Rubric

**1.0 - Perfect**:
- ✅ Ruthlessly simple
- ✅ Clean, readable code
- ✅ Proper error handling
- ✅ No unnecessary abstractions
- ✅ Well-structured and organized
- ✅ Follows all coding standards

**0.8 - Excellent**:
- ✅ Simple and clear
- ✅ Readable with minor issues
- ✅ Good error handling
- ⚠️ Minor abstractions that could be removed
- ✅ Well-organized

**0.6 - Good**:
- ⚠️ Somewhat complex but manageable
- ⚠️ Readable with some confusion points
- ⚠️ Basic error handling present
- ⚠️ Some unnecessary abstractions
- ✅ Reasonably organized

**0.4 - Acceptable**:
- ⚠️ More complex than needed
- ❌ Hard to read in places
- ❌ Inconsistent error handling
- ❌ Several unnecessary layers
- ⚠️ Organization could improve

**0.2 - Poor**:
- ❌ Overly complex
- ❌ Hard to understand
- ❌ Poor error handling
- ❌ Over-engineered
- ❌ Poorly structured

**0.0 - Unacceptable**:
- ❌ Unmaintainably complex
- ❌ Completely unclear
- ❌ No error handling
- ❌ Terrible structure
- ❌ Violates all principles

### Quality Checklist

**Simplicity**:
- [ ] No unnecessary abstractions
- [ ] Direct, obvious solutions
- [ ] Minimal layers
- [ ] Clear dependencies

**Readability**:
- [ ] Clear variable/function names
- [ ] Logical organization
- [ ] Appropriate comments (not excessive)
- [ ] Consistent style

**Error Handling**:
- [ ] Expected errors caught
- [ ] Clear error messages
- [ ] Fails gracefully
- [ ] Logs useful information

**Structure**:
- [ ] Logical file organization
- [ ] Clear module boundaries
- [ ] Separation of concerns
- [ ] No circular dependencies

### Philosophy Alignment

Check against Amplifier's philosophy:

**Ruthless Simplicity**:
- ❌ "Could this be simpler?"
- ❌ "Do we need this abstraction?"
- ❌ "Are we solving problems we don't have?"

**Present-Moment Focus**:
- ❌ "Is this solving current needs?"
- ❌ "Are we future-proofing unnecessarily?"

**Clarity Over Cleverness**:
- ❌ "Is this code obvious?"
- ❌ "Could a junior dev understand this?"

## Dimension 4: Testability

**Definition**: Can it be tested easily?

### Scoring Rubric

**1.0 - Perfect**:
- ✅ Easy to test
- ✅ Pure functions where possible
- ✅ Dependencies injectable
- ✅ Comprehensive test suite
- ✅ All tests pass
- ✅ Fast test execution

**0.8 - Excellent**:
- ✅ Mostly easy to test
- ✅ Good test coverage (>80%)
- ✅ Tests pass
- ⚠️ Minor mocking complexity

**0.6 - Good**:
- ⚠️ Requires some test setup
- ⚠️ Decent coverage (60-80%)
- ✅ Tests pass
- ⚠️ Some complex mocking

**0.4 - Acceptable**:
- ⚠️ Difficult to test
- ❌ Limited coverage (<60%)
- ⚠️ Most tests pass
- ❌ Heavy mocking required

**0.2 - Poor**:
- ❌ Very hard to test
- ❌ Minimal coverage (<30%)
- ❌ Many tests fail
- ❌ Tightly coupled code

**0.0 - Unacceptable**:
- ❌ Untestable
- ❌ No tests
- ❌ Would require major refactoring to test

### Evaluation Questions

1. How easy is it to write tests?
2. What's the test coverage?
3. Do all tests pass?
4. How much mocking is needed?
5. Are tests fast and reliable?

## Combined Scoring

**Overall Score = Average of dimension scores**

Or weighted if priorities differ:
```
Overall = (Correctness × 0.4) + 
          (Completeness × 0.3) + 
          (Quality × 0.2) + 
          (Testability × 0.1)
```

## Recommendation Matrix

Based on overall score:

| Score | Recommendation | Action |
|-------|---------------|--------|
| 0.9-1.0 | **accept** | Production-ready, ship it |
| 0.7-0.9 | **iterate-minor** | 1 refinement iteration |
| 0.5-0.7 | **iterate** | 2-3 iterations needed |
| 0.3-0.5 | **major-refactor** | Significant rework |
| 0.0-0.3 | **reject** | Start over with new approach |

## Example Evaluations

### Example 1: Authentication Module

```json
{
  "correctness": 0.85,
  "reasoning": "Handles main flows correctly, minor edge case with expired tokens",
  
  "completeness": 0.80,
  "reasoning": "All features present, but documentation could be better",
  
  "quality": 0.90,
  "reasoning": "Clean code, good error handling, follows principles",
  
  "testability": 0.75,
  "reasoning": "Good test coverage, but some mocking complexity",
  
  "overall": 0.825,
  "recommendation": "iterate-minor",
  "action": "Fix expired token edge case, improve docs"
}
```

### Example 2: Caching Layer

```json
{
  "correctness": 0.60,
  "reasoning": "Basic caching works, but race conditions in concurrent access",
  
  "completeness": 0.65,
  "reasoning": "Core features present, missing TTL and invalidation",
  
  "quality": 0.55,
  "reasoning": "Overly complex, could be much simpler",
  
  "testability": 0.70,
  "reasoning": "Tests exist but integration tests fragile",
  
  "overall": 0.625,
  "recommendation": "iterate",
  "action": "Simplify design, add TTL, fix race conditions, improve tests"
}
```

## Feedback Best Practices

**Be Specific**:
- ❌ "Code quality could be better"
- ✅ "Lines 45-67: Nested conditionals reduce readability. Extract to validateInput()"

**Reference Locations**:
- ❌ "Missing error handling"
- ✅ "Function parseToken() at auth.py:23 needs try-catch for JSON.parse"

**Provide Solutions**:
- ❌ "This is wrong"
- ✅ "This has race condition. Consider using lock or atomic operations"

**Quantify Impact**:
- ❌ "Performance issue"
- ✅ "O(n²) loop causes 5s delay for 1000 items. Use hash map for O(n)"

**Prioritize**:
- High severity: Correctness, security issues
- Medium severity: Completeness gaps, quality issues
- Low severity: Documentation, minor refactoring

## Calibration Examples

To maintain consistency, here are calibration examples:

**Score 0.9+**: Production-ready code from senior engineer
**Score 0.7-0.9**: Good PR that needs minor revisions
**Score 0.5-0.7**: Decent attempt but needs significant work
**Score 0.3-0.5**: Wrong approach but salvageable
**Score 0.0-0.3**: Fundamentally flawed

Be honest, be specific, be constructive.
