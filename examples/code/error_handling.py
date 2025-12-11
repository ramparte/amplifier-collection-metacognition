#!/usr/bin/env python3
"""
Error handling example: Demonstrating error recovery patterns.

This example shows:
- Handling assessment failures
- Recovering from evaluation errors
- Dealing with partial results
- Graceful degradation
"""

from typing import Dict, Any, Optional
from enum import Enum


class ErrorType(Enum):
    """Types of errors that can occur."""
    ASSESSMENT_UNCLEAR = "assessment_unclear"
    EVALUATION_FAILED = "evaluation_failed"
    TIMEOUT = "timeout"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    FILE_ACCESS = "file_access"


class ErrorHandler:
    """Handles errors from metacognition agents."""
    
    @staticmethod
    def handle_complexity_assessment_error(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle errors from complexity-assessor.
        
        Args:
            response: Response from complexity-assessor (may contain errors)
        
        Returns:
            Recovery strategy
        """
        # Check for null score (error indicator)
        if response.get("complexity_score") is None:
            recommendation = response.get("recommendation", "unknown")
            
            if recommendation == "clarify-requirements":
                return {
                    "action": "ask_user",
                    "questions": response.get("questions", []),
                    "message": "Task is ambiguous. Need clarification."
                }
            
            elif recommendation == "cannot-assess":
                return {
                    "action": "provide_context",
                    "required_context": response.get("required_context", []),
                    "message": "Missing required context files."
                }
            
            else:
                return {
                    "action": "use_best_judgment",
                    "message": "Assessment failed. Proceeding with medium complexity assumption.",
                    "fallback_score": 5.0
                }
        
        # Check for low confidence
        if response.get("confidence", 1.0) < 0.5:
            return {
                "action": "warn_user",
                "message": f"Low confidence assessment ({response['confidence']}). Results may be unreliable.",
                "proceed": True
            }
        
        # No error
        return {"action": "proceed", "message": "Assessment successful"}
    
    @staticmethod
    def handle_evaluation_error(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle errors from solution-evaluator.
        
        Args:
            response: Response from solution-evaluator (may contain errors)
        
        Returns:
            Recovery strategy
        """
        error = response.get("error", {})
        error_type = error.get("type")
        
        if error_type == "test_execution_error":
            # Tests failed to run - use partial evaluation
            return {
                "action": "use_partial_evaluation",
                "message": "Tests failed to execute. Using code review only.",
                "partial_scores": response.get("scores", {}),
                "suggestion": error.get("suggestion", "Fix test execution")
            }
        
        elif error_type == "file_access_error":
            # Can't access files
            return {
                "action": "abort_evaluation",
                "message": "Cannot access solution files.",
                "missing_files": error.get("missing_files", []),
                "suggestion": "Verify file paths and permissions"
            }
        
        elif response.get("overall_score") is None:
            # Complete evaluation failure
            return {
                "action": "skip_evaluation",
                "message": "Evaluation failed completely. Proceeding without validation.",
                "warning": "HIGH RISK - solution not validated"
            }
        
        # No critical error, but check for warnings
        if response.get("note"):
            return {
                "action": "proceed_with_warning",
                "message": response["note"],
                "score": response.get("overall_score")
            }
        
        return {"action": "proceed", "message": "Evaluation successful"}
    
    @staticmethod
    def handle_iteration_timeout(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle timeout during iterative refinement.
        
        Args:
            response: Response from iterative-refiner (timeout status)
        
        Returns:
            Recovery strategy
        """
        status = response.get("status")
        
        if status == "budget_exhausted":
            return {
                "action": "return_best_attempt",
                "message": f"Time/resource budget exhausted at iteration {response['iteration']}",
                "best_score": response.get("self_score"),
                "recommendation": "Consider: 1) Decompose task, 2) Allocate more resources, or 3) Accept current quality"
            }
        
        elif status == "max_iterations_reached":
            best_score = response.get("self_score", 0)
            if best_score >= 0.7:
                return {
                    "action": "accept_good_enough",
                    "message": f"Reached max iterations with score {best_score}",
                    "recommendation": "Score is acceptable (≥0.7). Consider shipping."
                }
            else:
                return {
                    "action": "suggest_decomposition",
                    "message": f"Max iterations reached with low score ({best_score})",
                    "recommendation": "Task may be too complex. Consider decomposition."
                }
        
        elif status == "plateau_detected":
            return {
                "action": "try_different_approach",
                "message": "Score plateaued. Current approach not yielding improvements.",
                "recommendation": "Try fundamentally different implementation strategy"
            }
        
        return {"action": "proceed", "message": "Iteration completed normally"}


def demonstrate_error_handling():
    """Demonstrate error handling patterns."""
    print("=== Metacognition Collection: Error Handling ===\n")
    
    handler = ErrorHandler()
    
    # Example 1: Assessment unclear
    print("Example 1: Unclear complexity assessment")
    print("-" * 50)
    unclear_response = {
        "complexity_score": None,
        "confidence": 0.3,
        "recommendation": "clarify-requirements",
        "questions": [
            "Which modules should be affected?",
            "What are the success criteria?"
        ]
    }
    recovery = handler.handle_complexity_assessment_error(unclear_response)
    print(f"Action: {recovery['action']}")
    print(f"Message: {recovery['message']}")
    if recovery.get("questions"):
        print("Questions:")
        for q in recovery["questions"]:
            print(f"  - {q}")
    
    print("\n" + "="*70 + "\n")
    
    # Example 2: Evaluation failure with partial results
    print("Example 2: Evaluation with test execution failure")
    print("-" * 50)
    partial_eval = {
        "overall_score": 0.5,
        "scores": {
            "correctness": None,  # Tests didn't run
            "completeness": 0.6,
            "quality": 0.7,
            "testability": 0.3
        },
        "error": {
            "type": "test_execution_error",
            "message": "Tests timed out after 30s",
            "suggestion": "Fix timeout in authentication tests"
        }
    }
    recovery = handler.handle_evaluation_error(partial_eval)
    print(f"Action: {recovery['action']}")
    print(f"Message: {recovery['message']}")
    print(f"Partial scores: {recovery['partial_scores']}")
    print(f"Suggestion: {recovery['suggestion']}")
    
    print("\n" + "="*70 + "\n")
    
    # Example 3: Iteration timeout
    print("Example 3: Iteration budget exhausted")
    print("-" * 50)
    timeout_response = {
        "iteration": 3,
        "solution": "... best attempt ...",
        "self_score": 0.78,
        "status": "budget_exhausted"
    }
    recovery = handler.handle_iteration_timeout(timeout_response)
    print(f"Action: {recovery['action']}")
    print(f"Message: {recovery['message']}")
    print(f"Best score: {recovery['best_score']}")
    print(f"Recommendation: {recovery['recommendation']}")
    
    print("\n" + "="*70 + "\n")
    
    # Example 4: Graceful degradation
    print("Example 4: Graceful degradation strategy")
    print("-" * 50)
    print("When all else fails:")
    print("  1. Return partial results (better than nothing)")
    print("  2. Explain what went wrong")
    print("  3. Suggest alternative approaches")
    print("  4. Warn about reduced confidence")
    print("\nExample response:")
    degraded_response = {
        "result": "partial_solution",
        "confidence": 0.3,
        "warnings": [
            "Evaluation incomplete - tests failed",
            "Only 2/5 ensemble strategies succeeded",
            "Iteration stopped early due to timeout"
        ],
        "recommendation": "Review manually before using in production",
        "alternatives": [
            "Decompose task into smaller pieces",
            "Allocate more time/resources",
            "Simplify requirements"
        ]
    }
    print(json.dumps(degraded_response, indent=2))


if __name__ == "__main__":
    import json
    demonstrate_error_handling()
