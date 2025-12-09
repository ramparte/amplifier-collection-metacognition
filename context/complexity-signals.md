# Complexity Signals for Task Assessment

Guide for assessing task complexity and recommending appropriate strategies.

## Complexity Dimensions

### 1. Scope Clarity

**Low Complexity (Clear Scope)**:
- Explicit requirements: "Add logging to auth.py lines 45-60"
- Specific location: "Fix typo in README.md line 23"
- Bounded changes: "Rename function `foo` to `bar`"

**High Complexity (Ambiguous Scope)**:
- Vague requirements: "Improve the authentication system"
- Undefined boundaries: "Optimize performance"
- Open-ended: "Design a better architecture"

### 2. Novelty

**Low Complexity (Familiar)**:
- Repetitive patterns: "Add another API endpoint like the existing ones"
- Well-known solutions: "Add standard CRUD operations"
- Copy-paste with modifications: "Create similar component to X"

**High Complexity (Novel)**:
- New patterns: "Design novel caching strategy for our use case"
- Unexplored territory: "Integrate with new third-party API"
- Creative work: "Architect system for 10x scale"

### 3. Integration Points

**Low Complexity (Isolated)**:
- Single file changes: "Update helper function in utils.py"
- No dependencies: "Add standalone utility class"
- Self-contained: "Create new independent module"

**High Complexity (Interconnected)**:
- Multi-system: "Integrate payment processing across 5 services"
- Many dependencies: "Refactor core module used by 20+ files"
- Cross-cutting: "Add feature touching database, API, and UI"

### 4. Success Criteria

**Low Complexity (Measurable)**:
- Clear definition: "Function returns true for valid emails"
- Testable: "All unit tests pass"
- Binary: "Bug fixed when error no longer appears"

**High Complexity (Subjective)**:
- Qualitative: "Code is more maintainable"
- Ambiguous: "System is more scalable"
- Requires judgment: "Architecture is better"

### 5. Context Requirements

**Low Complexity (Small Context)**:
- Few files: 1-3 files to understand
- Small codebase: <500 lines relevant code
- Shallow depth: No deep call chains

**High Complexity (Large Context)**:
- Many files: 10+ files to understand
- Large codebase: >2000 lines relevant code
- Deep dependencies: Multiple layers to trace

### 6. Risk Level

**Low Complexity (Low Risk)**:
- Non-critical: Documentation, comments, minor refactoring
- Easily reversible: Changes can be undone
- Safe: No production impact

**High Complexity (High Risk)**:
- Critical: Authentication, payment, data integrity
- Hard to reverse: Database migrations, API breaking changes
- Production impact: Direct effect on users

## Scoring Framework

**Complexity Score = Average of dimension scores (1-10)**

### Dimension Scoring

**Scope Clarity** (reverse scored):
- 1-3: Crystal clear, specific location/requirement
- 4-6: Somewhat clear, some interpretation needed
- 7-10: Vague, significant ambiguity

**Novelty**:
- 1-3: Highly familiar, done before
- 4-6: Some new elements, mostly familiar
- 7-10: Novel, uncharted territory

**Integration Points**:
- 1-3: Isolated, single file
- 4-6: Few dependencies, 2-5 files
- 7-10: Highly interconnected, 10+ files

**Success Criteria** (reverse scored):
- 1-3: Clear, measurable, testable
- 4-6: Somewhat clear, partially measurable
- 7-10: Vague, subjective, hard to verify

**Context Requirements**:
- 1-3: Small context, <5 files
- 4-6: Moderate context, 5-15 files
- 7-10: Large context, >15 files

**Risk Level**:
- 1-3: Low risk, easily reversible
- 4-6: Moderate risk, some impact
- 7-10: High risk, critical systems

## Examples with Scoring

### Example 1: "Fix typo in README.md line 42"

```
Scope Clarity: 1 (crystal clear)
Novelty: 1 (trivial)
Integration: 1 (isolated)
Success Criteria: 1 (binary - typo fixed)
Context: 1 (single file)
Risk: 1 (zero risk)

Average: 1.0
Complexity: VERY LOW
Recommendation: solve-directly
```

### Example 2: "Add logging to authentication module"

```
Scope Clarity: 3 (clear - add logging, but where exactly?)
Novelty: 2 (familiar - standard logging)
Integration: 4 (affects auth module, needs to fit existing pattern)
Success Criteria: 4 (somewhat clear - "adequate logging")
Context: 3 (auth module + logging setup)
Risk: 5 (moderate - auth is critical)

Average: 3.5
Complexity: LOW-MEDIUM
Recommendation: single-pass-with-review
```

### Example 3: "Design and implement caching layer"

```
Scope Clarity: 6 (somewhat vague - what to cache? where?)
Novelty: 7 (novel design for our system)
Integration: 7 (touches multiple services)
Success Criteria: 6 (performance improvement - subjective)
Context: 8 (need to understand entire data flow)
Risk: 7 (performance critical)

Average: 6.8
Complexity: HIGH
Recommendation: iterative-refinement
```

### Example 4: "Design authentication architecture for microservices"

```
Scope Clarity: 8 (very vague, many decisions)
Novelty: 9 (novel architecture design)
Integration: 9 (affects all microservices)
Success Criteria: 8 (architecture "quality" - subjective)
Context: 10 (entire system understanding needed)
Risk: 10 (authentication is critical)

Average: 9.0
Complexity: VERY HIGH
Recommendation: ensemble (critical decision) or decompose
```

## Strategy Recommendations by Score

**Score 1.0-3.0 (Low Complexity)**:
- **Strategy**: `solve-directly`
- **Reasoning**: Straightforward, bounded, familiar
- **Approach**: Execute immediately, no special handling
- **Expected Success**: 95%+

**Score 3.0-5.0 (Medium-Low Complexity)**:
- **Strategy**: `single-pass-with-review`
- **Reasoning**: Mostly clear, some complexity
- **Approach**: One attempt, then evaluate and refine
- **Expected Success**: 80-90%

**Score 5.0-7.0 (Medium-High Complexity)**:
- **Strategy**: `iterative-refinement`
- **Reasoning**: Novel or complex, needs iteration
- **Approach**: Multiple attempts with feedback (2-3 iterations)
- **Expected Success**: 70-80% after iteration

**Score 7.0-8.5 (High Complexity)**:
- **Strategy**: `decompose` or `iterative-refinement`
- **Reasoning**: Large scope, multiple concerns
- **Approach**: Break into subtasks OR iterate extensively (3-5 iterations)
- **Expected Success**: 60-70% after decomposition/iteration

**Score 8.5-10.0 (Very High Complexity)**:
- **Strategy**: `ensemble` for critical, `decompose` for large scope
- **Reasoning**: Critical decisions need consensus, large scope needs breakdown
- **Approach**: Parallel strategies with voting OR systematic decomposition
- **Expected Success**: 50-60%, but high confidence if consensus

## Red Flags (Automatic High Complexity)

These signals automatically suggest high complexity:

1. **"Design architecture for..."** → Likely 8+
2. **Multiple concerns in one task** → Add +2 to score
3. **Affects critical systems** (auth, payment, data integrity) → Add +2 to risk
4. **No clear acceptance criteria** → Add +2 to scope clarity
5. **"Improve" or "optimize" without metrics** → Add +2 to success criteria
6. **>10 files affected** → Add +2 to integration
7. **Never done before in this codebase** → Add +2 to novelty

## Confidence Assessment

Also assess confidence in your complexity estimate:

**High Confidence (0.8-1.0)**:
- Task is very similar to past tasks
- Requirements are explicit
- Scope is clearly bounded

**Medium Confidence (0.5-0.8)**:
- Some ambiguity in requirements
- Moderately familiar territory
- Scope is somewhat defined

**Low Confidence (0.0-0.5)**:
- Significant ambiguity
- Unfamiliar territory
- Unclear boundaries

When confidence is low, recommend asking clarifying questions before proceeding.

## Practical Tips

1. **Ask clarifying questions** if scope clarity < 5
2. **Start with simplest viable approach** (prefer lower complexity interpretation)
3. **Reassess after initial exploration** (complexity can change)
4. **Consider human expertise** (some tasks are harder for AI than humans)
5. **Factor in time constraints** (urgent tasks may need simpler approach)

## Mental Model

Think of complexity assessment like estimating mountain climbing difficulty:

- **Class 1-2** (Low): Hiking trail, can do in sneakers → solve-directly
- **Class 3** (Medium): Scrambling, need hands occasionally → single-pass-with-review
- **Class 4** (High): Easy climbing, rope recommended → iterative-refinement
- **Class 5** (Very High): Technical climbing, need equipment → decompose or ensemble

Don't send someone up a Class 5 climb with sneakers and no plan!
