#!/usr/bin/env python3
"""
Basic usage example: Using complexity-assessor to evaluate task complexity.

This example demonstrates:
- Loading a metacognition agent
- Invoking the agent with a task
- Parsing and using the response
"""

import json
from typing import Dict, Any


def assess_task_complexity(task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Assess complexity of a given task.
    
    Args:
        task: Task description string
        context: Optional context (files, systems, etc.)
    
    Returns:
        Complexity assessment with score and recommendation
    """
    # NOTE: This is conceptual - actual Amplifier API may differ
    # See Amplifier documentation for current API
    
    # Example invocation (conceptual)
    # agent = Agent.load("@metacognition:agents/complexity-assessor.md")
    # result = await agent.invoke({
    #     "task": task,
    #     "context": context or {}
    # })
    
    # For this example, simulate a response
    result = {
        "complexity_score": 7.0,
        "confidence": 0.85,
        "recommendation": "iterative-refinement",
        "reasoning": "Task involves novel architecture design with multiple integration points",
        "suggested_strategy": {
            "approach": "decompose-then-iterate",
            "substeps": [
                "Design high-level architecture",
                "Implement core module",
                "Integrate with existing system",
                "Iterate based on test results"
            ],
            "estimated_iterations": 3,
            "delegate_to": "zen-architect"
        }
    }
    
    return result


def route_based_on_complexity(assessment: Dict[str, Any]) -> str:
    """
    Route to appropriate strategy based on complexity assessment.
    
    Args:
        assessment: Result from complexity-assessor
    
    Returns:
        Strategy to use
    """
    recommendation = assessment["recommendation"]
    confidence = assessment["confidence"]
    
    # Check confidence
    if confidence < 0.5:
        print(f"⚠️  Low confidence ({confidence}). Consider asking for clarification.")
        return "clarify-with-user"
    
    # Route based on recommendation
    strategies = {
        "solve-directly": "execute_immediately",
        "single-pass-with-review": "implement_and_review",
        "iterative-refinement": "use_iterative_refiner",
        "ensemble": "use_ensemble_coordinator",
        "decompose": "break_into_subtasks"
    }
    
    return strategies.get(recommendation, "unknown")


def main():
    """Example usage."""
    print("=== Metacognition Collection: Basic Usage ===\n")
    
    # Example 1: Simple task
    print("Example 1: Simple task")
    task1 = "Fix typo in README.md line 42"
    assessment1 = assess_task_complexity(task1)
    print(f"Task: {task1}")
    print(f"Complexity: {assessment1['complexity_score']}")
    print(f"Recommendation: {assessment1['recommendation']}")
    print(f"Strategy: {route_based_on_complexity(assessment1)}\n")
    
    # Example 2: Complex task
    print("Example 2: Complex task")
    task2 = "Design and implement caching layer with TTL and invalidation"
    assessment2 = assess_task_complexity(task2, context={
        "files_affected": "estimate 5-10",
        "existing_patterns": "none",
        "critical": False
    })
    print(f"Task: {task2}")
    print(f"Complexity: {assessment2['complexity_score']}")
    print(f"Recommendation: {assessment2['recommendation']}")
    print(f"Reasoning: {assessment2['reasoning']}")
    print(f"Strategy: {route_based_on_complexity(assessment2)}\n")
    
    # Example 3: Handle low confidence
    print("Example 3: Low confidence assessment")
    assessment3 = {
        "complexity_score": None,
        "confidence": 0.3,
        "recommendation": "clarify-requirements",
        "reasoning": "Task is too ambiguous to assess accurately",
        "questions": [
            "Which modules should this affect?",
            "What are the specific success criteria?",
            "Are there existing patterns to follow?"
        ]
    }
    print(f"Confidence: {assessment3['confidence']}")
    print(f"Action: {route_based_on_complexity(assessment3)}")
    print(f"Questions to ask:")
    for q in assessment3["questions"]:
        print(f"  - {q}")


if __name__ == "__main__":
    main()
