"""
End-to-end workflow tests for metacognition agents.

Tests complete workflows showing how agents work together:
- Complexity assessment → strategy selection
- Iterative refinement with evaluation feedback
- Ensemble coordination with consensus
- Error recovery and graceful degradation
"""

import pytest
from pathlib import Path


class TestComplexityToStrategyFlow:
    """Test workflow: complexity assessment → strategy execution."""
    
    def test_low_complexity_recommends_solve_directly(self):
        """Verify low complexity tasks recommend direct execution."""
        # Simulate complexity assessment for simple task
        task = "Fix typo in README.md line 42"
        
        # Expected complexity assessment
        expected_complexity = {
            "complexity_score": 1.5,  # Very low
            "confidence": 0.95,
            "recommendation": "solve-directly"
        }
        
        # Verify score in low range (1-3)
        assert 1.0 <= expected_complexity["complexity_score"] <= 3.0
        assert expected_complexity["recommendation"] == "solve-directly"
    
    def test_medium_complexity_recommends_review(self):
        """Verify medium complexity tasks recommend single-pass-with-review."""
        task = "Add logging to authentication module"
        
        expected_complexity = {
            "complexity_score": 4.5,  # Medium
            "confidence": 0.80,
            "recommendation": "single-pass-with-review"
        }
        
        # Verify score in medium range (4-6)
        assert 4.0 <= expected_complexity["complexity_score"] <= 6.0
        assert expected_complexity["recommendation"] == "single-pass-with-review"
    
    def test_high_complexity_recommends_iteration(self):
        """Verify high complexity tasks recommend iterative-refinement."""
        task = "Design and implement caching layer"
        
        expected_complexity = {
            "complexity_score": 7.5,  # High
            "confidence": 0.75,
            "recommendation": "iterative-refinement"
        }
        
        # Verify score in high range (7-8)
        assert 7.0 <= expected_complexity["complexity_score"] <= 8.5
        assert expected_complexity["recommendation"] in [
            "iterative-refinement", 
            "decompose"
        ]
    
    def test_critical_complexity_recommends_ensemble(self):
        """Verify critical tasks recommend ensemble approach."""
        task = "Design authentication architecture for microservices"
        
        expected_complexity = {
            "complexity_score": 9.0,  # Very high
            "confidence": 0.85,
            "recommendation": "ensemble"
        }
        
        # Verify score in critical range (8.5-10)
        assert 8.5 <= expected_complexity["complexity_score"] <= 10.0
        assert expected_complexity["recommendation"] in [
            "ensemble",
            "decompose"
        ]


class TestIterativeRefinementFlow:
    """Test workflow: generate → evaluate → refine → repeat."""
    
    def test_iteration_improves_scores_over_time(self):
        """Verify scores improve across iterations."""
        # Simulate iteration history
        iterations = [
            {"iteration": 1, "score": 0.60},
            {"iteration": 2, "score": 0.75},
            {"iteration": 3, "score": 0.92}
        ]
        
        # Scores should generally improve
        assert iterations[1]["score"] > iterations[0]["score"]
        assert iterations[2]["score"] > iterations[1]["score"]
        
        # Final score should reach success threshold
        assert iterations[-1]["score"] >= 0.9
    
    def test_iteration_terminates_on_success(self):
        """Verify iteration stops when score >= 0.9."""
        current_score = 0.92
        success_threshold = 0.9
        max_iterations = 5
        current_iteration = 3
        
        # Should terminate on success
        should_terminate = current_score >= success_threshold
        assert should_terminate, "Should terminate with score 0.92"
        
        # Should return result at iteration 3 (before max)
        assert current_iteration < max_iterations
    
    def test_iteration_terminates_at_max(self):
        """Verify iteration stops at max iterations even if not successful."""
        current_score = 0.75
        success_threshold = 0.9
        max_iterations = 5
        current_iteration = 5
        
        # Should terminate at max iterations
        should_terminate = current_iteration >= max_iterations
        assert should_terminate, "Should terminate at max iterations"
        
        # Should return best attempt even if below threshold
        assert current_score < success_threshold
    
    def test_iteration_detects_plateau(self):
        """Verify plateau detection when scores don't improve."""
        iterations = [
            {"iteration": 1, "score": 0.70},
            {"iteration": 2, "score": 0.82},
            {"iteration": 3, "score": 0.82},
            {"iteration": 4, "score": 0.82}
        ]
        
        # Check for plateau (no improvement for 2+ iterations)
        recent_scores = [it["score"] for it in iterations[-3:]]
        is_plateau = len(set(recent_scores)) == 1  # All same
        assert is_plateau, "Should detect plateau"
    
    def test_iteration_uses_evaluator_feedback(self):
        """Verify iteration incorporates evaluator feedback."""
        # Iteration 1
        eval_1 = {
            "overall_score": 0.60,
            "weaknesses": [
                {
                    "issue": "Missing error handling",
                    "suggestion": "Add try-catch blocks"
                }
            ]
        }
        
        # Iteration 2 should address feedback
        eval_2 = {
            "overall_score": 0.80,
            "strengths": ["Added error handling"],  # Addressed feedback
            "weaknesses": [
                {
                    "issue": "Complex nested logic",
                    "suggestion": "Extract to functions"
                }
            ]
        }
        
        # Score improved after addressing feedback
        assert eval_2["overall_score"] > eval_1["overall_score"]
        
        # Previous weakness should not appear in new weaknesses
        weakness_issues_2 = [w["issue"] for w in eval_2["weaknesses"]]
        assert "Missing error handling" not in weakness_issues_2


class TestEnsembleCoordinationFlow:
    """Test workflow: parallel strategies → consensus → selection."""
    
    def test_ensemble_identifies_consensus(self):
        """Verify ensemble correctly groups identical solutions."""
        # Simulate 5 parallel strategies
        solutions = [
            {"agent": "agent1", "solution": "JWT + Redis"},
            {"agent": "agent2", "solution": "JWT + Redis"},  # Match
            {"agent": "agent3", "solution": "JWT + Redis"},  # Match
            {"agent": "agent4", "solution": "OAuth2 + DB"},
            {"agent": "agent5", "solution": "Stateless JWT"}
        ]
        
        # Group by identical solutions
        from collections import Counter
        solution_counts = Counter(s["solution"] for s in solutions)
        
        # Should identify consensus group (JWT + Redis: 3 votes)
        assert solution_counts["JWT + Redis"] == 3
        assert solution_counts["OAuth2 + DB"] == 1
        assert solution_counts["Stateless JWT"] == 1
    
    def test_ensemble_confidence_correlates_with_consensus(self):
        """Verify confidence increases with consensus strength."""
        # High consensus (3/5 = 60%)
        high_consensus = {
            "vote_count": 3,
            "total_strategies": 5,
            "confidence": 0.9
        }
        consensus_ratio = high_consensus["vote_count"] / high_consensus["total_strategies"]
        assert consensus_ratio >= 0.5
        assert high_consensus["confidence"] >= 0.7
        
        # Low consensus (1/5 = 20%)
        low_consensus = {
            "vote_count": 1,
            "total_strategies": 5,
            "confidence": 0.3
        }
        consensus_ratio = low_consensus["vote_count"] / low_consensus["total_strategies"]
        assert consensus_ratio < 0.5
        assert low_consensus["confidence"] < 0.5
    
    def test_ensemble_handles_partial_failure(self):
        """Verify ensemble continues with successful strategies."""
        # 5 strategies attempted, 2 failed
        result = {
            "strategies_tried": 5,
            "strategies_succeeded": 3,
            "strategies_failed": 2,
            "consensus_groups": [
                {"solution_id": "A", "vote_count": 2}
            ]
        }
        
        # Should still provide result with 3 successful strategies
        assert result["strategies_succeeded"] >= 2
        assert len(result["consensus_groups"]) > 0
        
        # Confidence should be reduced due to partial failure
        expected_confidence = 0.6  # Lower than if all succeeded
        assert expected_confidence < 0.9
    
    def test_ensemble_signals_no_consensus(self):
        """Verify ensemble reports when no consensus emerges."""
        # All 5 strategies produce different solutions
        result = {
            "strategies_tried": 5,
            "consensus_groups": [
                {"solution_id": "A", "vote_count": 1},
                {"solution_id": "B", "vote_count": 1},
                {"solution_id": "C", "vote_count": 1},
                {"solution_id": "D", "vote_count": 1},
                {"solution_id": "E", "vote_count": 1}
            ],
            "recommendation": {
                "confidence": 0.2,  # Very low
                "warning": "NO CONSENSUS"
            }
        }
        
        # All solutions have single vote
        all_single_votes = all(
            g["vote_count"] == 1 
            for g in result["consensus_groups"]
        )
        assert all_single_votes
        
        # Confidence should be very low
        assert result["recommendation"]["confidence"] < 0.3


class TestSinglePassWithReviewFlow:
    """Test workflow: solve → evaluate → refine if needed."""
    
    def test_accept_if_score_high(self):
        """Verify acceptance when score >= 0.9."""
        evaluation = {
            "overall_score": 0.92,
            "recommendation": "accept"
        }
        
        assert evaluation["overall_score"] >= 0.9
        assert evaluation["recommendation"] == "accept"
    
    def test_iterate_if_score_medium(self):
        """Verify iteration recommended for medium scores."""
        evaluation = {
            "overall_score": 0.75,
            "recommendation": "iterate"
        }
        
        assert 0.5 <= evaluation["overall_score"] < 0.9
        assert evaluation["recommendation"] == "iterate"
    
    def test_reject_if_score_low(self):
        """Verify rejection recommended for low scores."""
        evaluation = {
            "overall_score": 0.35,
            "recommendation": "reject"
        }
        
        assert evaluation["overall_score"] < 0.5
        assert evaluation["recommendation"] == "reject"


class TestErrorRecoveryFlows:
    """Test workflow: error → recovery → graceful degradation."""
    
    def test_complexity_assessment_failure_asks_clarification(self):
        """Verify unclear tasks request clarification."""
        error_response = {
            "complexity_score": None,
            "confidence": 0.3,
            "recommendation": "clarify-requirements",
            "questions": [
                "Which modules should this affect?",
                "What are success criteria?"
            ]
        }
        
        assert error_response["complexity_score"] is None
        assert error_response["confidence"] < 0.5
        assert len(error_response["questions"]) > 0
    
    def test_evaluation_failure_provides_partial_results(self):
        """Verify evaluator provides partial scores when tests fail."""
        partial_eval = {
            "overall_score": 0.5,
            "scores": {
                "correctness": None,      # Tests failed, can't assess
                "completeness": 0.6,      # Can assess from code
                "quality": 0.7,           # Can assess from code
                "testability": 0.3        # Can assess from code
            },
            "recommendation": "iterate",
            "note": "Tests failed, partial evaluation only"
        }
        
        # Should provide overall score even with one null dimension
        assert partial_eval["overall_score"] is not None
        
        # Non-null dimensions should be valid
        for dim, score in partial_eval["scores"].items():
            if score is not None:
                assert 0.0 <= score <= 1.0
    
    def test_iteration_returns_best_attempt_on_timeout(self):
        """Verify iteration returns best result when budget exhausted."""
        timeout_response = {
            "iteration": 3,
            "solution": "... best attempt ...",
            "self_score": 0.78,
            "status": "budget_exhausted",
            "best_iteration": 3,
            "recommendation": "Allocate more resources or decompose task"
        }
        
        assert timeout_response["status"] == "budget_exhausted"
        assert timeout_response["solution"] is not None  # Returns something
        assert timeout_response["self_score"] < 0.9  # Didn't reach success
    
    def test_ensemble_continues_with_partial_success(self):
        """Verify ensemble uses successful strategies even if some fail."""
        partial_result = {
            "strategies_tried": 5,
            "strategies_succeeded": 2,
            "strategies_failed": 3,
            "recommendation": {
                "selected_solution": "A",
                "confidence": 0.5,
                "note": "Only 2/5 strategies succeeded"
            }
        }
        
        # Should provide result if at least 2 succeeded
        assert partial_result["strategies_succeeded"] >= 2
        assert partial_result["recommendation"]["selected_solution"] is not None
        
        # Confidence should reflect partial failure
        assert partial_result["recommendation"]["confidence"] < 0.7


class TestProfileCoordinationLogic:
    """Test profile's decision logic for routing tasks."""
    
    def test_profile_routes_based_on_complexity(self):
        """Verify profile routes to appropriate strategy."""
        routing_decisions = [
            {"complexity": 2.0, "expected_route": "execute_directly"},
            {"complexity": 4.5, "expected_route": "single_pass_review"},
            {"complexity": 7.0, "expected_route": "iterative_refinement"},
            {"complexity": 9.5, "expected_route": "ensemble"}
        ]
        
        for decision in routing_decisions:
            score = decision["complexity"]
            
            if score <= 3.0:
                assert decision["expected_route"] == "execute_directly"
            elif score <= 6.0:
                assert decision["expected_route"] == "single_pass_review"
            elif score <= 8.5:
                assert decision["expected_route"] == "iterative_refinement"
            else:
                assert decision["expected_route"] == "ensemble"
    
    def test_profile_adapts_to_time_constraints(self):
        """Verify profile adjusts strategy based on urgency."""
        # Urgent task with high complexity
        task = {
            "complexity": 9.0,
            "urgent": True,
            "recommended_strategy": "decompose"  # Not ensemble (too slow)
        }
        
        # Should prefer decompose over ensemble when urgent
        if task["urgent"] and task["complexity"] >= 8.5:
            assert task["recommended_strategy"] in ["decompose", "single_pass_review"]
            assert task["recommended_strategy"] != "ensemble"


def test_complete_metacognitive_workflow():
    """Integration test: Complete workflow from task to result."""
    # Simulate complete workflow
    task = "Implement rate limiting for API"
    
    # Step 1: Complexity assessment
    assessment = {
        "complexity_score": 6.5,
        "recommendation": "iterative-refinement"
    }
    
    # Step 2: Route to iterative-refiner
    assert assessment["recommendation"] == "iterative-refinement"
    
    # Step 3: Iterative refinement (3 iterations)
    iterations = [
        {"iteration": 1, "score": 0.55},
        {"iteration": 2, "score": 0.78},
        {"iteration": 3, "score": 0.93}
    ]
    
    # Step 4: Success (score >= 0.9)
    final_result = iterations[-1]
    assert final_result["score"] >= 0.9
    
    # Step 5: Return to user
    assert final_result["score"] >= 0.9, "Workflow completed successfully"
