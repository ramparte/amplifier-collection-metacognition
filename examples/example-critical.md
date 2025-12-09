# Example: Critical Decision (Ensemble Consensus)

This example shows ensemble-coordinator handling a high-stakes architectural decision.

## Task

"Design the authentication architecture for our microservices platform. We need something secure, scalable, and maintainable."

## Coordinator Flow

### Step 1: Assess Complexity

```
Coordinator: This is a critical architectural decision. Let me assess carefully.

[Delegates to complexity-assessor]

complexity-assessor analyzes:
  - Scope: Very large (affects entire platform)
  - Novelty: Novel architecture for our system
  - Integration: Touches all microservices
  - Success Criteria: Subjective (security, scalability, maintainability)
  - Context: Need to understand all services, data flows, requirements
  - Risk: CRITICAL (authentication is security-critical)

Output:
{
  "complexity_score": 9.0,
  "confidence": 0.9,
  "recommendation": "ensemble",
  "reasoning": "Architectural decision affecting entire platform. Security-critical 
               with high long-term impact. Multiple valid approaches exist. 
               Consensus from multiple perspectives will reduce risk and bias.",
  "suggested_strategy": {
    "approach": "ensemble-consensus",
    "num_strategies": 5,
    "diversity": ["agents", "temperatures", "mental_models"],
    "delegate_to": "ensemble-coordinator"
  }
}

Coordinator: Score 9.0 with "ensemble" recommendation. This is indeed critical.
             Delegating to ensemble-coordinator for parallel strategy exploration.
```

### Step 2: Ensemble Coordination

```
[Delegates to ensemble-coordinator]

ensemble-coordinator: Running 5 parallel strategies with diversity.
```

#### Strategy 1: zen-architect (temp=0.3, security-first)

```
Agent: zen-architect
Config: temperature=0.3 (conservative), "security-first approach"
Approach: "What's the most secure, simple authentication?"

Analysis:
- Microservices need centralized identity
- JWT tokens for stateless auth
- Redis for session tracking (logout, refresh)
- API gateway validates tokens before routing
- Short-lived access tokens (15 min)
- Long-lived refresh tokens (7 days, rotatable)

Design:
┌─────────────┐
│ API Gateway │ ← Validates JWT, routes to services
└──────┬──────┘
       │
   ┌───┴────┐
   │ Redis  │ ← Session store (blacklist, refresh tokens)
   └────────┘

Service flow:
1. User logs in → Auth Service
2. Auth Service → JWT + Refresh Token
3. Store session in Redis
4. Client uses JWT for API calls
5. Gateway validates JWT → route to service
6. Services trust gateway (no re-validation)

Recommendation: JWT + Redis + Gateway validation
```

#### Strategy 2: modular-builder (temp=0.5, simplicity-first)

```
Agent: modular-builder
Config: temperature=0.5 (balanced), "simplicity-first"
Approach: "What's the simplest auth that could work?"

Analysis:
- Microservices need shared authentication
- Avoid complexity of OAuth2 if not needed
- JWT for tokens (stateless, standard)
- Redis for session state
- Each service validates JWT independently (avoid gateway bottleneck)

Design:
┌─────────┐  ┌─────────┐  ┌─────────┐
│Service A│  │Service B│  │Service C│
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
            ┌─────┴──────┐
            │Auth Library│ ← Shared JWT validation
            └─────┬──────┘
                  │
              ┌───┴────┐
              │ Redis  │ ← Revocation list, sessions
              └────────┘

Service flow:
1. User logs in → Auth Service → JWT
2. Client includes JWT in all requests
3. Each service validates JWT independently
4. Services check Redis for revocation
5. Distributed validation (no single point of failure)

Recommendation: JWT + Redis + Distributed validation
```

#### Strategy 3: modular-builder (temp=0.7, flexibility-first)

```
Agent: modular-builder  
Config: temperature=0.7 (exploratory), "flexibility for future"
Approach: "What gives us most flexibility?"

Analysis:
- Might need OAuth2 for third-party integrations later
- Different services have different security needs
- Some services need fine-grained permissions
- Consider service-to-service auth too

Design:
┌──────────────┐
│ Auth Service │ ← Central OAuth2-compatible server
└──────┬───────┘
       │
   ┌───┴───────────┐
   │   │           │
   JWT │        OAuth2
       │         Tokens
       ├───────────┤
       │
  ┌────┴─────┐
  │  Redis   │ ← Sessions, permissions, token metadata
  └──────────┘

Hybrid approach:
- JWT for service-to-service (simple)
- OAuth2 for user auth (flexible)
- RBAC stored in Redis
- Gateway + service-level validation

Recommendation: Hybrid JWT + OAuth2 with RBAC
```

#### Strategy 4: bug-hunter (temp=0.3, reliability-first)

```
Agent: bug-hunter
Config: temperature=0.3 (conservative), "what could go wrong?"
Approach: "Design for failure modes and attacks"

Analysis:
- JWT vulnerabilities: alg=none attacks, weak secrets
- Session fixation attacks
- Token theft/replay attacks
- Distributed systems: clock skew issues
- Service compromise: blast radius

Design:
Enhanced JWT + Redis with security hardening:
- JWT signed with RS256 (asymmetric), not HS256
- Short expiry (5 min access tokens)
- Refresh tokens in secure Redis (encrypted)
- Token binding (IP + User-Agent validation)
- Audit logging for all auth events
- Rate limiting on auth endpoints
- Automatic session rotation

Flow with security layers:
1. Login → MFA verification
2. Generate JWT (RS256, 5min) + Refresh (encrypted in Redis)
3. Client uses JWT
4. Gateway validates + checks Redis blacklist
5. Logs all auth events
6. Auto-rotate sessions every 24h
7. Anomaly detection (impossible travel, etc.)

Recommendation: Hardened JWT + Redis + Audit + MFA
```

#### Strategy 5: zen-architect (temp=0.7, innovative)

```
Agent: zen-architect
Config: temperature=0.7 (exploratory), "think differently"
Approach: "Challenge assumptions - do we need sessions at all?"

Analysis:
- Sessions add complexity and state
- Redis is another dependency to manage
- JWT can be truly stateless
- Revocation can be handled with short expiry
- Service mesh could handle auth

Design:
Stateless JWT with service mesh:
- Pure stateless JWT (no Redis sessions)
- Very short expiry (1 minute access tokens)
- Refresh handled by client-side logic
- Service mesh (Istio) validates JWTs
- No central session store
- Auth service only issues tokens

Extreme simplicity:
┌────────────────┐
│  Auth Service  │ ← Only issues JWTs
└────────────────┘

┌─────────────────┐
│  Service Mesh   │ ← Validates all JWTs at proxy layer
│  (Istio/Envoy)  │
└─────────────────┘

Services are completely auth-agnostic!

Recommendation: Stateless JWT + Service Mesh
```

### Step 3: Consensus Analysis

```
ensemble-coordinator: Collecting and grouping solutions.

Grouping by similarity:
Group A: JWT + Redis + Gateway/Distributed validation
  - Strategy 1 (zen-architect temp=0.3): JWT + Redis + Gateway
  - Strategy 2 (modular-builder temp=0.5): JWT + Redis + Distributed
  - Strategy 4 (bug-hunter temp=0.3): JWT + Redis + Security hardening
  Vote count: 3

Group B: Hybrid OAuth2 + JWT
  - Strategy 3 (modular-builder temp=0.7): OAuth2 + JWT hybrid
  Vote count: 1

Group C: Stateless JWT + Service Mesh
  - Strategy 5 (zen-architect temp=0.7): Pure stateless + Istio
  Vote count: 1

Consensus: Group A (60% of strategies converged here)

Detailed analysis of Group A:
All three strategies agreed on:
✓ JWT tokens (stateless benefits)
✓ Redis for session management
✓ Centralized vs distributed validation (both work)
✓ Short-lived access tokens

Variations:
- Strategy 1: Gateway validation (single point)
- Strategy 2: Distributed validation (no bottleneck)
- Strategy 4: Enhanced security (MFA, audit, hardening)

Best of Group A: Combine best elements
- JWT + Redis (consensus)
- Distributed validation (from Strategy 2 - no bottleneck)
- Security hardening (from Strategy 4 - critical for auth)
```

### Step 4: Final Recommendation

```
ensemble-coordinator returns:
{
  "strategies_tried": 5,
  "solutions_generated": 5,
  "consensus_groups": [
    {
      "solution_id": "A",
      "vote_count": 3,
      "agents": [
        "zen-architect (temp=0.3)",
        "modular-builder (temp=0.5)",
        "bug-hunter (temp=0.3)"
      ],
      "quality_score": 0.88,
      "solution_summary": "JWT + Redis with distributed validation and security hardening"
    },
    {
      "solution_id": "B",
      "vote_count": 1,
      "agents": ["modular-builder (temp=0.7)"],
      "quality_score": 0.75,
      "solution_summary": "Hybrid OAuth2 + JWT"
    },
    {
      "solution_id": "C",
      "vote_count": 1,
      "agents": ["zen-architect (temp=0.7)"],
      "quality_score": 0.70,
      "solution_summary": "Stateless JWT + Service Mesh"
    }
  ],
  "recommendation": {
    "selected_solution": "A",
    "confidence": 0.9,
    "reasoning": "3 out of 5 strategies independently converged on JWT + Redis 
                 approach, representing 60% consensus. Includes both conservative 
                 (temp=0.3) and balanced (temp=0.5) agents, suggesting robust choice.
                 
                 Security-focused agent (bug-hunter) also chose this approach with
                 important hardening recommendations.
                 
                 The two outliers represent valid alternatives:
                 - OAuth2 hybrid for future third-party integration needs
                 - Service mesh for extreme simplicity
                 
                 But consensus suggests JWT + Redis is the proven, balanced approach
                 for our current needs."
  },
  "synthesis": {
    "recommended_design": {
      "core": "JWT tokens with RS256 signing",
      "session_store": "Redis for refresh tokens and revocation",
      "validation": "Distributed (each service validates independently)",
      "security": {
        "token_expiry": "5 min access, 7 day refresh",
        "signing": "RS256 asymmetric keys",
        "additional": ["MFA support", "Audit logging", "Rate limiting"]
      },
      "architecture": "Shared auth library + Redis cluster"
    },
    "alternatives_considered": {
      "oauth2_hybrid": "Keep in mind if we need third-party integrations",
      "service_mesh": "Consider if we adopt Istio/service mesh later"
    },
    "implementation_priority": [
      "Phase 1: Basic JWT + Redis + distributed validation",
      "Phase 2: Security hardening (MFA, audit, rate limiting)",
      "Phase 3: Evaluate OAuth2 if third-party integrations needed"
    ]
  }
}

Coordinator: Strong consensus (60%) on JWT + Redis architecture with distributed 
             validation and security hardening. High confidence (0.9) in recommendation.
```

## Consensus Visualization

```
5 Parallel Strategies:
                                ┌─→ Group A (60%) ←─┐
                                │   JWT + Redis      │ CONSENSUS
Strategy 1 (zen/0.3)     ───────┘                    │
Strategy 2 (builder/0.5) ─────────────────────────── │ High
Strategy 4 (bug/0.3)     ─────────────────────────── │ Confidence
                                                      │
Strategy 3 (builder/0.7) ───────→ Group B (20%)     │
                                   OAuth2 Hybrid     │
                                                      │
Strategy 5 (zen/0.7)     ───────→ Group C (20%)     │
                                   Service Mesh      │
                                                      │
Result: Select Group A ←──────────────────────────────┘
```

## Key Insights

1. **Consensus = Confidence**: 60% agreement on critical decision provides high confidence
2. **Diversity uncovered alternatives**: Exploratory strategies (temp=0.7) found valid alternatives to consider
3. **Conservative + balanced agree**: Both conservative (0.3) and balanced (0.5) agents chose same approach
4. **Security expert validated**: bug-hunter's choice strengthens confidence
5. **Outliers inform future**: OAuth2 and service mesh options noted for future consideration

## Cost vs Value

**Cost**:
- 5 parallel LLM calls (~30 seconds wall-clock time)
- Higher token usage (~5x single pass)
- Ensemble coordination overhead

**Value**:
- High confidence in critical decision
- Multiple perspectives reduce blind spots
- Alternatives documented for future
- Security implications considered
- Risk mitigation through consensus

**Verdict**: For authentication architecture (critical, high-impact, long-term), cost is justified.

## Without Ensemble

Single-pass decision:
- One agent's perspective (potential bias)
- Miss alternative approaches
- Lower confidence
- Higher risk of suboptimal choice

Risk: Ship architecture that's not optimal, discover later, expensive to change.

## When NOT to Use Ensemble

Don't use ensemble for:
- Non-critical decisions
- Well-established patterns (CRUD endpoints)
- Time-sensitive tasks
- Low-stakes experiments

Use ensemble for:
- Critical architecture decisions ✓
- Security-sensitive designs ✓
- High-impact, long-term choices ✓
- When multiple valid approaches exist ✓

## Coordinator Decision Tree

```
Task: "Design authentication architecture"
  ↓
complexity-assessor: Score 9.0, "critical decision"
  ↓
Is critical + high-stakes + multiple valid approaches?
  YES ↓
ensemble-coordinator: Run 5 parallel strategies
  ↓
Vote: 60% consensus on JWT + Redis
  ↓
Confidence: HIGH (0.9)
  ↓
Recommendation: Implement Group A solution
```

## Result

**Decision**: JWT + Redis with distributed validation and security hardening

**Confidence**: 0.9 (very high)

**Basis**: 60% consensus from independent strategies, including security expert validation

**Time to Decision**: ~2 minutes (parallel execution)

**Value**: High-confidence critical decision with documented alternatives

This is metacognition at its best: multiple perspectives, measured consensus, high confidence in critical choices.
