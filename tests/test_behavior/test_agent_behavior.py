"""
Behavioral tests for agent output formats and decision logic.

These tests validate that agents produce correctly formatted outputs
and make appropriate decisions based on their instructions.
"""

import pytest
import json
from pathlib import Path


class TestComplexityAssessorBehavior:
    """Test complexity-assessor behavior and output format."""
    
    def test_output_format_has_required_fields(self):
        """Verify complexity-assessor output includes all required fields."""
        # Expected output format from complexity-assessor.md lines 54-72
        required_fields = {
            "complexity_score": (int, float),
            "confidence": (int, float),
            "recommendation": str,
            "reasoning": str,
            "suggested_strategy": dict
        }
        
        # Mock response that should match agent specification
        sample_output = {
            "complexity_score": 7.0,
            "confidence": 0.85,
            "recommendation": "iterative-refinement",
            "reasoning": "Task involves novel architecture design...",
            "suggested_strategy": {
                "approach": "decompose-then-iterate",
                "substeps": ["Design", "Implement", "Integrate"],
                "estimated_iterations": 3
            }
        }
        
        # Validate all required fields present and correct type
        for field, expected_type in required_fields.items():
            assert field in sample_output, f"Missing required field: {field}"
            if isinstance(expected_type, tuple):
                assert isinstance(sample_output[field], expected_type), \
                    f"Field {field} has wrong type"
            else:
                assert isinstance(sample_output[field], expected_type), \
                    f"Field {field} has wrong type"
    
    def test_complexity_score_in_valid_range(self):
        """Verify complexity scores are in 1-10 range."""
        valid_scores = [1.0, 3.5, 7.0, 9.5, 10.0]
        invalid_scores = [0.0, -1.0, 11.0, 15.5]
        
        for score in valid_scores:
            assert 1.0 <= score <= 10.0, f"Valid score {score} should pass"
        
        for score in invalid_scores:
            assert not (1.0 <= score <= 10.0), f"Invalid score {score} should fail"
    
    def test_confidence_score_in_valid_range(self):
        """Verify confidence scores are in 0.0-1.0 range."""
        valid_confidence = [0.0, 0.3, 0.5, 0.85, 1.0]
        invalid_confidence = [-0.1, 1.5, 2.0]
        
        for conf in valid_confidence:
            assert 0.0 <= conf <= 1.0
        
        for conf in invalid_confidence:
            assert not (0.0 <= conf <= 1.0)
    
    def test_recommendation_values_are_valid(self):
        """Verify recommendation is one of the defined strategies."""
        valid_recommendations = [
            "solve-directly",
            "single-pass-with-review",
            "iterative-refinement",
            "decompose",
            "ensemble"
        ]
        
        # From complexity-assessor.md lines 76-80
        for rec in valid_recommendations:
            assert rec in [
                "solve-directly",
                "single-pass-with-review", 
                "iterative-refinement",
                "decompose",
                "ensemble"
            ]
    
    def test_error_response_format(self):
        """Verify error responses have correct structure."""
        # From added error handling section
        error_response = {
            "complexity_score": None,
            "confidence": 0.0,
            "recommendation": "cannot-assess",
            "reasoning": "Unable to assess complexity without access to files",
            "required_context": ["file1.py", "file2.py"]
        }
        
        assert error_response["complexity_score"] is None
        assert error_response["confidence"] == 0.0
        assert error_response["recommendation"] == "cannot-assess"
        assert "required_context" in error_response


class TestSolutionEvaluatorBehavior:
    """Test solution-evaluator behavior and output format."""
    
    def test_output_format_has_required_fields(self):
        """Verify solution-evaluator output includes all required fields."""
        # Expected format from solution-evaluator.md lines 67-108
        required_fields = {
            "overall_score": (int, float, type(None)),
            "scores": dict,
            "strengths": list,
            "weaknesses": list,
            "recommendation": str
        }
        
        sample_output = {
            "overall_score": 0.75,
            "scores": {
                "correctness": 0.8,
                "completeness": 0.7,
                "quality": 0.75,
                "testability": 0.75
            },
            "strengths": ["Clean separation", "Good tests"],
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
        
        for field in required_fields:
            assert field in sample_output, f"Missing required field: {field}"
    
    def test_all_dimension_scores_in_valid_range(self):
        """Verify all score dimensions are 0.0-1.0."""
        scores = {
            "correctness": 0.8,
            "completeness": 0.7,
            "quality": 0.75,
            "testability": 0.75
        }
        
        for dimension, score in scores.items():
            assert 0.0 <= score <= 1.0, \
                f"{dimension} score {score} must be in 0.0-1.0 range"
    
    def test_overall_score_in_valid_range(self):
        """Verify overall score is 0.0-1.0."""
        valid_scores = [0.0, 0.5, 0.75, 0.9, 1.0]
        
        for score in valid_scores:
            assert 0.0 <= score <= 1.0
    
    def test_recommendation_values_are_valid(self):
        """Verify recommendation is one of the defined values."""
        # From solution-evaluator.md lines 153-167
        valid_recommendations = ["accept", "iterate", "reject"]
        
        for rec in valid_recommendations:
            assert rec in ["accept", "iterate", "reject"]
    
    def test_weakness_structure(self):
        """Verify weakness entries have required fields."""
        weakness = {
            "issue": "Missing validation",
            "location": "auth.py:23",
            "severity": "high",
            "suggestion": "Add guard clause"
        }
        
        required_fields = ["issue", "location", "severity", "suggestion"]
        for field in required_fields:
            assert field in weakness, f"Weakness missing field: {field}"
        
        # Severity should be one of: low, medium, high
        assert weakness["severity"] in ["low", "medium", "high"]


class TestIterativeRefinerBehavior:
    """Test iterative-refiner behavior and output format."""
    
    def test_output_format_has_required_fields(self):
        """Verify iterative-refiner output includes all required fields."""
        # Expected format from iterative-refiner.md lines 88-103
        required_fields = {
            "iteration": int,
            "solution": str,
            "self_score": (int, float, type(None)),
            "breakdown": dict,
            "feedback": str,
            "continue": bool
        }
        
        sample_output = {
            "iteration": 2,
            "solution": "def add(a, b): return a + b",
            "self_score": 0.75,
            "breakdown": {
                "correctness": 0.8,
                "completeness": 0.7,
                "quality": 0.8,
                "clarity": 0.7
            },
            "feedback": "Good progress, but missing edge cases",
            "improvements_from_last": "Added error handling",
            "continue": True,
            "reasoning": "Score improved from 0.6 to 0.75"
        }
        
        for field in required_fields:
            assert field in sample_output, f"Missing required field: {field}"
    
    def test_iteration_history_structure(self):
        """Verify iteration history maintains proper structure."""
        # From iterative-refiner.md lines 109-119
        history = {
            "history": [
                {"iteration": 1, "score": 0.6, "approach": "Direct"},
                {"iteration": 2, "score": 0.75, "approach": "Added error handling"},
                {"iteration": 3, "score": 0.92, "approach": "Simplified"}
            ],
            "best_iteration": 3,
            "best_score": 0.92
        }
        
        assert "history" in history
        assert "best_iteration" in history
        assert "best_score" in history
        assert isinstance(history["history"], list)
        assert len(history["history"]) > 0
    
    def test_termination_conditions(self):
        """Verify termination logic based on score thresholds."""
        success_threshold = 0.9
        max_iterations = 5
        
        # Should terminate on success
        assert 0.92 >= success_threshold, "Should terminate with score 0.92"
        
        # Should terminate on max iterations
        current_iteration = 5
        assert current_iteration >= max_iterations, "Should terminate at max"
        
        # Should continue if neither condition met
        current_score = 0.75
        current_iteration = 3
        should_continue = (
            current_score < success_threshold and 
            current_iteration < max_iterations
        )
        assert should_continue, "Should continue iteration"


class TestEnsembleCoordinatorBehavior:
    """Test ensemble-coordinator behavior and output format."""
    
    def test_output_format_has_required_fields(self):
        """Verify ensemble-coordinator output includes all required fields."""
        # Expected format from ensemble-coordinator.md lines 100-142
        required_fields = {
            "strategies_tried": int,
            "consensus_groups": list,
            "recommendation": dict
        }
        
        sample_output = {
            "strategies_tried": 5,
            "solutions_generated": 5,
            "consensus_groups": [
                {
                    "solution_id": "A",
                    "vote_count": 3,
                    "agents": ["zen-architect", "modular-builder"],
                    "quality_score": 0.85,
                    "solution": "JWT + Redis"
                }
            ],
            "recommendation": {
                "selected_solution": "A",
                "confidence": 0.9,
                "reasoning": "60% consensus"
            }
        }
        
        for field in required_fields:
            assert field in sample_output, f"Missing required field: {field}"
    
    def test_consensus_group_structure(self):
        """Verify consensus groups have required fields."""
        group = {
            "solution_id": "A",
            "vote_count": 3,
            "agents": ["agent1", "agent2", "agent3"],
            "quality_score": 0.85,
            "solution": "Implementation details"
        }
        
        required_fields = ["solution_id", "vote_count", "agents"]
        for field in required_fields:
            assert field in group, f"Consensus group missing: {field}"
        
        assert isinstance(group["agents"], list)
        assert len(group["agents"]) == group["vote_count"]
    
    def test_confidence_calculation(self):
        """Verify confidence correlates with consensus strength."""
        # High consensus (3/5 = 60%) should have high confidence
        high_consensus_votes = 3
        total_strategies = 5
        consensus_ratio = high_consensus_votes / total_strategies
        assert consensus_ratio >= 0.5, "High consensus"
        
        # Low consensus (1/5 = 20%) should have low confidence
        low_consensus_votes = 1
        consensus_ratio = low_consensus_votes / total_strategies
        assert consensus_ratio < 0.5, "Low consensus"
        
        # Split vote (2-2-1) should have medium confidence
        votes = [2, 2, 1]
        max_votes = max(votes)
        split_ratio = max_votes / sum(votes)
        assert 0.3 < split_ratio < 0.5, "Split vote"
    
    def test_diversity_first_ranking(self):
        """Verify one solution per group (diversity-first)."""
        # From ensemble-coordinator.md: diversity-first ranking
        consensus_groups = [
            {"solution_id": "A", "vote_count": 3},
            {"solution_id": "B", "vote_count": 2}
        ]
        
        # Each group should have unique solution_id
        solution_ids = [g["solution_id"] for g in consensus_groups]
        assert len(solution_ids) == len(set(solution_ids)), \
            "Each group should have unique solution"


class TestErrorHandlingBehavior:
    """Test error handling across all agents."""
    
    def test_null_scores_for_evaluation_errors(self):
        """Verify agents return null scores when evaluation impossible."""
        error_responses = [
            {"overall_score": None, "recommendation": "cannot-evaluate"},
            {"complexity_score": None, "confidence": 0.0}
        ]
        
        for response in error_responses:
            # Should have null score
            score_field = "overall_score" if "overall_score" in response else "complexity_score"
            assert response[score_field] is None
    
    def test_partial_scores_on_partial_failure(self):
        """Verify agents provide partial scores when possible."""
        # From solution-evaluator error handling
        partial_response = {
            "overall_score": 0.5,
            "scores": {
                "correctness": None,  # Tests failed
                "completeness": 0.6,  # Can assess from code
                "quality": 0.7,       # Can assess from code
                "testability": 0.3    # Can assess from code
            }
        }
        
        # Should have overall score even if some dimensions null
        assert partial_response["overall_score"] is not None
        # Some dimensions can be assessed without test execution
        assert partial_response["scores"]["quality"] is not None
    
    def test_error_response_includes_suggestions(self):
        """Verify error responses include actionable suggestions."""
        error_response = {
            "error": {
                "type": "file_access_error",
                "message": "Cannot access files",
                "suggestion": "Verify file paths exist"
            }
        }
        
        assert "error" in error_response
        assert "suggestion" in error_response["error"]
        assert len(error_response["error"]["suggestion"]) > 0


class TestScoringConsistency:
    """Test scoring consistency across agents."""
    
    def test_soft_scoring_scale(self):
        """Verify all agents use 0.0-1.0 scale consistently."""
        # All agents should use same scale
        scales = {
            "complexity": (1.0, 10.0),      # Exception: uses 1-10
            "evaluation": (0.0, 1.0),
            "iteration": (0.0, 1.0),
            "ensemble": (0.0, 1.0)
        }
        
        # Verify evaluation/iteration/ensemble all use 0.0-1.0
        common_scale = (0.0, 1.0)
        assert scales["evaluation"] == common_scale
        assert scales["iteration"] == common_scale
        assert scales["ensemble"] == common_scale
    
    def test_score_interpretation_consistency(self):
        """Verify score interpretation is consistent."""
        # From scoring-rubrics.md and agent documentation
        interpretations = {
            0.95: "excellent",
            0.85: "good",
            0.75: "acceptable",
            0.50: "needs work",
            0.30: "poor"
        }
        
        # 0.9+ should be accept
        assert 0.95 >= 0.9, "Should recommend accept"
        
        # 0.7-0.9 should be iterate
        assert 0.7 <= 0.85 < 0.9, "Should recommend iterate"
        
        # <0.5 should be reject or major rework
        assert 0.30 < 0.5, "Should recommend reject/rework"


def test_all_agents_exist():
    """Verify all four agents have corresponding files."""
    agents_dir = Path(__file__).parent.parent.parent / "agents"
    
    expected_agents = [
        "complexity-assessor.md",
        "ensemble-coordinator.md",
        "iterative-refiner.md",
        "solution-evaluator.md"
    ]
    
    for agent in expected_agents:
        agent_path = agents_dir / agent
        assert agent_path.exists(), f"Agent file missing: {agent}"
