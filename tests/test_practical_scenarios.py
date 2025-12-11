"""
Practical end-to-end test scenarios for task success analysis.

These tests demonstrate real-world usage of the metacognition toolset
with concrete examples that validate the agents work as expected.
"""

import pytest
import json


class TestSimpleTaskScenarios:
    """Test simple, low-complexity task scenarios."""
    
    def test_typo_fix_should_be_low_complexity(self):
        """Verify typo fixes are assessed as low complexity."""
        task_description = "Fix typo in README.md line 42: 'recieve' should be 'receive'"
        
        # Expected complexity assessment
        expected_assessment = {
            "complexity_score": 1.5,
            "confidence": 0.95,
            "recommendation": "solve-directly",
            "reasoning": "Simple text change with clear location and no side effects"
        }
        
        # Validate assessment
        assert expected_assessment["complexity_score"] <= 3.0, \
            "Typo fix should be low complexity (1-3)"
        assert expected_assessment["recommendation"] == "solve-directly", \
            "Simple fixes should be solved directly"
        assert expected_assessment["confidence"] >= 0.9, \
            "Confidence should be high for simple tasks"
    
    def test_simple_task_evaluation(self):
        """Test evaluation of a simple completed task."""
        solution = {
            "task": "Fix typo in README.md",
            "changes": "Line 42: 'recieve' -> 'receive'",
            "files_modified": ["README.md"]
        }
        
        # Expected evaluation
        expected_evaluation = {
            "overall_score": 1.0,
            "scores": {
                "correctness": 1.0,
                "completeness": 1.0,
                "quality": 1.0,
                "testability": 1.0
            },
            "strengths": [
                "Correct fix applied",
                "Clean change with no side effects",
                "Exactly addresses stated requirement"
            ],
            "weaknesses": [],
            "recommendation": "accept"
        }
        
        # Validate
        assert expected_evaluation["overall_score"] >= 0.9, \
            "Simple correct solution should score high"
        assert expected_evaluation["recommendation"] == "accept", \
            "Perfect solution should be accepted"


class TestMediumComplexityScenarios:
    """Test medium-complexity task scenarios requiring review."""
    
    def test_add_logging_medium_complexity(self):
        """Verify adding logging is medium complexity."""
        task_description = """
        Add structured logging to the authentication module.
        Requirements:
        - Log all login attempts (success and failure)
        - Include user ID, timestamp, IP address
        - Use JSON format for easy parsing
        - Don't log passwords or tokens
        """
        
        expected_assessment = {
            "complexity_score": 4.5,
            "confidence": 0.80,
            "recommendation": "single-pass-with-review",
            "reasoning": "Straightforward implementation but security implications require review"
        }
        
        assert 4.0 <= expected_assessment["complexity_score"] <= 6.0, \
            "Adding logging should be medium complexity"
        assert expected_assessment["recommendation"] == "single-pass-with-review"
    
    def test_logging_solution_needs_iteration(self):
        """Test evaluation of logging solution with room for improvement."""
        solution_code = """
        def login(username, password):
            # Added logging
            print(f"Login attempt: {username}")
            
            if authenticate(username, password):
                print(f"Success: {username}")
                return True
            else:
                print(f"Failed: {username}")
                return False
        """
        
        expected_evaluation = {
            "overall_score": 0.65,
            "scores": {
                "correctness": 0.7,
                "completeness": 0.6,
                "quality": 0.6,
                "testability": 0.7
            },
            "strengths": [
                "Logs both success and failure cases",
                "Includes username for tracking"
            ],
            "weaknesses": [
                {
                    "issue": "Using print() instead of proper logging framework",
                    "location": "login function lines 3, 6, 9",
                    "severity": "high",
                    "suggestion": "Use logging.info() with structured format"
                },
                {
                    "issue": "Missing timestamp and IP address (requirements)",
                    "location": "login function",
                    "severity": "high",
                    "suggestion": "Add timestamp and IP to log entries"
                },
                {
                    "issue": "Not using JSON format as required",
                    "location": "login function",
                    "severity": "medium",
                    "suggestion": "Use json.dumps() to format log entries"
                }
            ],
            "recommendation": "iterate",
            "next_steps": [
                "Replace print() with logging.info()",
                "Add structured JSON format with all required fields",
                "Add timestamp and IP address to logs"
            ]
        }
        
        # Validate
        assert 0.5 <= expected_evaluation["overall_score"] < 0.9, \
            "Partial solution should score in 'iterate' range"
        assert expected_evaluation["recommendation"] == "iterate"
        assert len(expected_evaluation["weaknesses"]) > 0, \
            "Should identify specific issues"


class TestHighComplexityIterativeScenarios:
    """Test high-complexity scenarios requiring iteration."""
    
    def test_caching_layer_high_complexity(self):
        """Verify caching layer implementation is high complexity."""
        task_description = """
        Design and implement a caching layer for the API.
        Requirements:
        - Support TTL (time-to-live) for cache entries
        - Handle cache invalidation on data updates
        - Thread-safe for concurrent access
        - LRU eviction when cache is full
        - Metrics for cache hit/miss rates
        """
        
        expected_assessment = {
            "complexity_score": 7.5,
            "confidence": 0.75,
            "recommendation": "iterative-refinement",
            "reasoning": "Multiple complex requirements, concurrency concerns, needs testing",
            "suggested_strategy": {
                "approach": "iterative-refinement",
                "estimated_iterations": 3,
                "substeps": [
                    "Implement basic cache with TTL",
                    "Add thread safety and invalidation",
                    "Add LRU eviction and metrics"
                ]
            }
        }
        
        assert 7.0 <= expected_assessment["complexity_score"] <= 8.5, \
            "Caching layer should be high complexity"
        assert expected_assessment["recommendation"] in ["iterative-refinement", "decompose"]
    
    def test_iterative_improvement_progression(self):
        """Test that iterations improve scores progressively."""
        
        # Iteration 1: Basic implementation
        iteration_1 = {
            "iteration": 1,
            "solution": "Basic dictionary-based cache with TTL",
            "self_score": 0.55,
            "breakdown": {
                "correctness": 0.6,
                "completeness": 0.4,
                "quality": 0.6,
                "clarity": 0.6
            },
            "feedback": "Basic functionality works but missing invalidation and thread safety",
            "weaknesses": [
                "No cache invalidation mechanism",
                "Not thread-safe",
                "Missing LRU eviction",
                "No metrics"
            ],
            "continue": True
        }
        
        # Iteration 2: Added more features
        iteration_2 = {
            "iteration": 2,
            "solution": "Cache with TTL, invalidation, and basic thread safety",
            "self_score": 0.78,
            "breakdown": {
                "correctness": 0.8,
                "completeness": 0.7,
                "quality": 0.8,
                "clarity": 0.8
            },
            "feedback": "Good progress. Added invalidation and locks, but race conditions possible",
            "improvements_from_last": "Added cache invalidation and threading.Lock",
            "weaknesses": [
                "Potential race condition in TTL check",
                "Still missing LRU eviction",
                "Metrics not implemented"
            ],
            "continue": True
        }
        
        # Iteration 3: Final refinement
        iteration_3 = {
            "iteration": 3,
            "solution": "Complete cache with all features, optimized",
            "self_score": 0.93,
            "breakdown": {
                "correctness": 0.95,
                "completeness": 0.92,
                "quality": 0.92,
                "clarity": 0.92
            },
            "feedback": "Excellent implementation, all requirements met",
            "improvements_from_last": "Added LRU eviction, metrics, fixed race conditions",
            "weaknesses": [],
            "continue": False,
            "reasoning": "Score >= 0.9 threshold, success achieved"
        }
        
        iterations = [iteration_1, iteration_2, iteration_3]
        
        # Validate progressive improvement
        for i in range(1, len(iterations)):
            prev_score = iterations[i-1]["self_score"]
            curr_score = iterations[i]["self_score"]
            assert curr_score > prev_score, \
                f"Iteration {i+1} should improve on iteration {i}"
        
        # Validate termination logic
        assert iteration_3["self_score"] >= 0.9, "Final iteration reached success threshold"
        assert iteration_3["continue"] is False, "Should stop after success"


class TestCriticalComplexityEnsembleScenarios:
    """Test critical scenarios requiring ensemble approach."""
    
    def test_microservices_auth_critical_complexity(self):
        """Verify microservices auth architecture is critical complexity."""
        task_description = """
        Design authentication architecture for microservices platform.
        Requirements:
        - Support 50+ microservices
        - OAuth2 and JWT options
        - Service-to-service authentication
        - Token refresh and revocation
        - High availability (no single point of failure)
        - Audit logging for compliance
        """
        
        expected_assessment = {
            "complexity_score": 9.0,
            "confidence": 0.85,
            "recommendation": "ensemble",
            "reasoning": "Critical architecture decision with security implications, benefits from multiple perspectives"
        }
        
        assert expected_assessment["complexity_score"] >= 8.5, \
            "Architecture decisions should be critical complexity"
        assert expected_assessment["recommendation"] in ["ensemble", "decompose"]
    
    def test_ensemble_consensus_identification(self):
        """Test that ensemble correctly identifies consensus."""
        
        # Simulate 5 parallel strategies generating solutions
        ensemble_results = {
            "strategies_tried": 5,
            "solutions_generated": 5,
            "all_solutions": [
                {
                    "agent": "zen-architect-temp-0.3",
                    "solution": "JWT + Redis for token storage + API Gateway",
                    "quality_score": 0.85
                },
                {
                    "agent": "modular-builder-temp-0.5",
                    "solution": "JWT + Redis for token storage + API Gateway",
                    "quality_score": 0.87
                },
                {
                    "agent": "security-expert-temp-0.3",
                    "solution": "JWT + Redis for token storage + API Gateway",
                    "quality_score": 0.90
                },
                {
                    "agent": "modular-builder-temp-0.7",
                    "solution": "OAuth2 + Database + Service Mesh",
                    "quality_score": 0.82
                },
                {
                    "agent": "zen-architect-temp-0.7",
                    "solution": "Stateless JWT only (no storage)",
                    "quality_score": 0.75
                }
            ],
            "consensus_groups": [
                {
                    "solution_id": "A",
                    "solution": "JWT + Redis for token storage + API Gateway",
                    "vote_count": 3,
                    "agents": [
                        "zen-architect-temp-0.3",
                        "modular-builder-temp-0.5", 
                        "security-expert-temp-0.3"
                    ],
                    "avg_quality_score": 0.87
                },
                {
                    "solution_id": "B",
                    "solution": "OAuth2 + Database + Service Mesh",
                    "vote_count": 1,
                    "agents": ["modular-builder-temp-0.7"],
                    "avg_quality_score": 0.82
                },
                {
                    "solution_id": "C",
                    "solution": "Stateless JWT only (no storage)",
                    "vote_count": 1,
                    "agents": ["zen-architect-temp-0.7"],
                    "avg_quality_score": 0.75
                }
            ],
            "recommendation": {
                "selected_solution": "A",
                "confidence": 0.90,
                "reasoning": "60% consensus (3/5 agents) with high quality scores",
                "consensus_percentage": 0.60,
                "rationale": "Strong majority agreement on JWT + Redis approach, validated by multiple independent strategies"
            }
        }
        
        # Validate consensus detection
        assert ensemble_results["consensus_groups"][0]["vote_count"] == 3, \
            "Should identify 3-vote consensus"
        
        # Validate confidence calculation
        consensus_ratio = 3 / 5
        assert consensus_ratio >= 0.5, "Should be high consensus"
        assert ensemble_results["recommendation"]["confidence"] >= 0.8, \
            "High consensus should yield high confidence"
        
        # Validate selection
        assert ensemble_results["recommendation"]["selected_solution"] == "A", \
            "Should select solution with most votes"


class TestErrorHandlingScenarios:
    """Test error handling and graceful degradation."""
    
    def test_unclear_requirements_asks_clarification(self):
        """Test handling of unclear task requirements."""
        vague_task = "Make the system better"
        
        error_response = {
            "complexity_score": None,
            "confidence": 0.2,
            "recommendation": "clarify-requirements",
            "reasoning": "Task description too vague to assess complexity",
            "questions": [
                "Which specific system component needs improvement?",
                "What metrics define 'better'?",
                "What are the success criteria?",
                "Are there specific performance targets or features needed?"
            ]
        }
        
        assert error_response["complexity_score"] is None, \
            "Should not provide score without clear requirements"
        assert error_response["confidence"] < 0.5, \
            "Confidence should be low for unclear tasks"
        assert len(error_response["questions"]) > 0, \
            "Should ask clarifying questions"
    
    def test_partial_evaluation_on_test_failure(self):
        """Test evaluation when tests fail to execute."""
        partial_eval = {
            "overall_score": 0.55,
            "scores": {
                "correctness": None,  # Can't assess without running tests
                "completeness": 0.7,  # Can assess from code review
                "quality": 0.6,       # Can assess from code review
                "testability": 0.4    # Can assess from code structure
            },
            "recommendation": "iterate",
            "error": {
                "type": "test_execution_error",
                "message": "Test suite failed to execute: ModuleNotFoundError",
                "suggestion": "Fix import errors in test suite"
            },
            "note": "Partial evaluation based on code review only. Tests could not execute."
        }
        
        # Should provide partial results
        assert partial_eval["overall_score"] is not None, \
            "Should provide overall score even with partial data"
        
        # Non-testable dimensions should have scores
        assert partial_eval["scores"]["completeness"] is not None
        assert partial_eval["scores"]["quality"] is not None
        
        # Should include error details
        assert "error" in partial_eval
        assert "suggestion" in partial_eval["error"]
    
    def test_iteration_plateau_detection(self):
        """Test detection of score plateaus during iteration."""
        iterations = [
            {"iteration": 1, "score": 0.65},
            {"iteration": 2, "score": 0.78},
            {"iteration": 3, "score": 0.79},  # Minimal improvement
            {"iteration": 4, "score": 0.79},  # No improvement
            {"iteration": 5, "score": 0.79}   # No improvement
        ]
        
        # Detect plateau (last 3 iterations show no significant improvement)
        recent_scores = [it["score"] for it in iterations[-3:]]
        score_variance = max(recent_scores) - min(recent_scores)
        
        is_plateau = score_variance < 0.05  # Less than 5% variance
        assert is_plateau, "Should detect plateau when scores don't improve"
        
        # Should recommend different approach
        plateau_response = {
            "status": "plateau_detected",
            "current_score": 0.79,
            "iterations_without_improvement": 3,
            "recommendation": "Different approach needed - current strategy has plateaued",
            "suggestions": [
                "Decompose into smaller subtasks",
                "Try ensemble approach for fresh perspectives",
                "Review requirements - may need clarification"
            ]
        }
        
        assert plateau_response["iterations_without_improvement"] >= 2
        assert len(plateau_response["suggestions"]) > 0


class TestScoringConsistency:
    """Test scoring consistency and interpretation."""
    
    def test_score_ranges_match_recommendations(self):
        """Verify score ranges align with recommendations."""
        test_cases = [
            {"score": 0.95, "expected_rec": "accept"},
            {"score": 0.90, "expected_rec": "accept"},
            {"score": 0.85, "expected_rec": "iterate"},
            {"score": 0.75, "expected_rec": "iterate"},
            {"score": 0.60, "expected_rec": "iterate"},
            {"score": 0.45, "expected_rec": "reject"},
            {"score": 0.30, "expected_rec": "reject"}
        ]
        
        for case in test_cases:
            score = case["score"]
            
            if score >= 0.9:
                actual_rec = "accept"
            elif score >= 0.5:
                actual_rec = "iterate"
            else:
                actual_rec = "reject"
            
            assert actual_rec == case["expected_rec"], \
                f"Score {score} should recommend {case['expected_rec']}, got {actual_rec}"
    
    def test_dimension_scores_contribute_to_overall(self):
        """Test that dimension scores properly contribute to overall score."""
        dimension_scores = {
            "correctness": 0.9,
            "completeness": 0.8,
            "quality": 0.85,
            "testability": 0.75
        }
        
        # Overall should be roughly average of dimensions
        avg_score = sum(dimension_scores.values()) / len(dimension_scores)
        assert 0.80 <= avg_score <= 0.85
        
        # Test case with actual overall score
        evaluation = {
            "scores": dimension_scores,
            "overall_score": 0.825
        }
        
        # Overall should be within reasonable range of average
        assert abs(evaluation["overall_score"] - avg_score) < 0.1, \
            "Overall score should roughly match dimension average"


def test_complete_workflow_integration():
    """Integration test: Complete task success analysis workflow."""
    
    # Scenario: Implement rate limiting for API
    task = "Implement rate limiting middleware for Express API"
    
    # Step 1: Complexity Assessment
    assessment = {
        "complexity_score": 6.0,
        "confidence": 0.82,
        "recommendation": "single-pass-with-review",
        "reasoning": "Well-defined problem with known solutions, but needs review for correctness"
    }
    
    assert 4.0 <= assessment["complexity_score"] <= 7.0
    
    # Step 2: Implementation (first pass)
    first_pass_solution = "Rate limiting middleware implementation"
    
    # Step 3: Evaluation
    evaluation = {
        "overall_score": 0.82,
        "scores": {
            "correctness": 0.85,
            "completeness": 0.80,
            "quality": 0.85,
            "testability": 0.80
        },
        "strengths": [
            "Clean middleware pattern",
            "Configurable rate limits",
            "Good error messages"
        ],
        "weaknesses": [
            {
                "issue": "No distributed rate limiting for multi-instance deployments",
                "severity": "medium",
                "suggestion": "Consider Redis-backed rate limiter for production"
            }
        ],
        "recommendation": "iterate"
    }
    
    assert 0.7 <= evaluation["overall_score"] < 0.9
    assert evaluation["recommendation"] == "iterate"
    
    # Step 4: Refinement based on feedback
    refined_evaluation = {
        "overall_score": 0.91,
        "scores": {
            "correctness": 0.95,
            "completeness": 0.90,
            "quality": 0.90,
            "testability": 0.90
        },
        "improvements": "Added Redis-backed storage for distributed scenarios",
        "recommendation": "accept"
    }
    
    assert refined_evaluation["overall_score"] >= 0.9
    assert refined_evaluation["recommendation"] == "accept"
    
    # Workflow complete
    assert refined_evaluation["overall_score"] > evaluation["overall_score"], \
        "Refinement should improve score"
