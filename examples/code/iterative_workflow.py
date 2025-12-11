#!/usr/bin/env python3
"""
Iterative workflow example: Using iterative-refiner for complex tasks.

This example demonstrates:
- Delegating to iterative-refiner
- Monitoring iteration progress
- Handling termination conditions
- Using feedback for improvement
"""

import json
from typing import Dict, Any, List


class IterativeRefinerClient:
    """Client for interacting with iterative-refiner agent."""
    
    def __init__(self, max_iterations: int = 5, success_threshold: float = 0.9):
        self.max_iterations = max_iterations
        self.success_threshold = success_threshold
        self.history: List[Dict[str, Any]] = []
    
    def refine(self, task: str) -> Dict[str, Any]:
        """
        Execute iterative refinement on a task.
        
        Args:
            task: Task to solve
        
        Returns:
            Best solution with score and history
        """
        print(f"Starting iterative refinement (max {self.max_iterations} iterations)")
        print(f"Success threshold: {self.success_threshold}\n")
        
        # Simulate iterations
        # In reality, this would delegate to iterative-refiner agent
        for iteration in range(1, self.max_iterations + 1):
            print(f"--- Iteration {iteration}/{self.max_iterations} ---")
            
            # Simulate iteration result
            result = self._execute_iteration(iteration, task)
            self.history.append(result)
            
            print(f"Score: {result['score']}")
            print(f"Feedback: {result['feedback']}")
            
            # Check termination conditions
            if result['score'] >= self.success_threshold:
                print(f"\n✅ Success! Score {result['score']} >= {self.success_threshold}")
                return self._build_final_result(iteration, result)
            
            # Check for plateau
            if self._is_plateau():
                print(f"\n⚠️  Plateau detected. Score not improving.")
                return self._build_final_result(iteration, result)
            
            print()
        
        # Max iterations reached
        print(f"\n⏱️  Max iterations reached. Returning best attempt.")
        best_result = max(self.history, key=lambda x: x['score'])
        return self._build_final_result(self.max_iterations, best_result)
    
    def _execute_iteration(self, iteration: int, task: str) -> Dict[str, Any]:
        """Simulate executing one iteration."""
        # In reality, this would:
        # 1. Generate solution (or refine previous)
        # 2. Delegate to solution-evaluator
        # 3. Incorporate feedback
        
        # Simulate progressive improvement
        scores = [0.60, 0.75, 0.88, 0.92, 0.94]
        feedbacks = [
            "Missing error handling and edge cases",
            "Good progress, but complex nested logic",
            "Almost there, minor performance issues",
            "Excellent! Minor documentation gaps",
            "Perfect implementation"
        ]
        
        idx = min(iteration - 1, len(scores) - 1)
        
        return {
            "iteration": iteration,
            "score": scores[idx],
            "feedback": feedbacks[idx],
            "solution": f"Solution attempt {iteration}..."
        }
    
    def _is_plateau(self) -> bool:
        """Check if scores have plateaued."""
        if len(self.history) < 3:
            return False
        
        recent_scores = [h['score'] for h in self.history[-3:]]
        # Plateau if all recent scores are same
        return len(set(recent_scores)) == 1
    
    def _build_final_result(self, final_iteration: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """Build final result with history."""
        return {
            "iteration": final_iteration,
            "solution": result['solution'],
            "score": result['score'],
            "history": self.history.copy(),
            "best_iteration": max(self.history, key=lambda x: x['score'])['iteration']
        }


def main():
    """Example usage."""
    print("=== Metacognition Collection: Iterative Workflow ===\n")
    
    # Example 1: Successful iteration
    print("Example 1: Task that succeeds in 4 iterations")
    print("-" * 50)
    refiner = IterativeRefinerClient(max_iterations=5, success_threshold=0.9)
    result = refiner.refine("Implement rate limiting for API")
    
    print(f"\nFinal Result:")
    print(f"  Iterations used: {result['iteration']}")
    print(f"  Final score: {result['score']}")
    print(f"  Best iteration: {result['best_iteration']}")
    
    print("\n" + "="*70 + "\n")
    
    # Example 2: Iteration with plateau
    print("Example 2: Task that plateaus")
    print("-" * 50)
    
    # Simulate plateau by modifying client behavior
    class PlateauSimulator(IterativeRefinerClient):
        def _execute_iteration(self, iteration, task):
            # Simulate plateau at score 0.82
            scores = [0.70, 0.82, 0.82, 0.82, 0.82]
            feedbacks = [
                "Initial implementation",
                "Improved error handling",
                "No significant improvement",
                "Still no improvement",
                "Plateau detected"
            ]
            
            idx = min(iteration - 1, len(scores) - 1)
            return {
                "iteration": iteration,
                "score": scores[idx],
                "feedback": feedbacks[idx],
                "solution": f"Solution attempt {iteration}..."
            }
    
    refiner2 = PlateauSimulator(max_iterations=5, success_threshold=0.9)
    result2 = refiner2.refine("Optimize database query performance")
    
    print(f"\nFinal Result:")
    print(f"  Iterations used: {result2['iteration']}")
    print(f"  Final score: {result2['score']}")
    print(f"  Status: Plateau - consider decomposition or different approach")
    
    print("\n" + "="*70 + "\n")
    
    # Example 3: Using feedback for improvement
    print("Example 3: Feedback-driven improvement")
    print("-" * 50)
    
    # Simulate detailed feedback incorporation
    iteration_details = [
        {
            "iteration": 1,
            "score": 0.60,
            "weaknesses": ["Missing null checks", "No test coverage"],
            "action": "Add null validation and basic tests"
        },
        {
            "iteration": 2,
            "score": 0.78,
            "weaknesses": ["Complex nested conditionals"],
            "action": "Refactor with guard clauses"
        },
        {
            "iteration": 3,
            "score": 0.93,
            "weaknesses": ["Minor: Add code comments"],
            "action": "Add documentation"
        }
    ]
    
    for detail in iteration_details:
        print(f"\nIteration {detail['iteration']}:")
        print(f"  Score: {detail['score']}")
        print(f"  Issues found: {', '.join(detail['weaknesses'])}")
        print(f"  Next action: {detail['action']}")
    
    print(f"\n✅ Final score: 0.93 - Success!")


if __name__ == "__main__":
    main()
