"""
Pytest fixtures for metacognition collection tests.

Provides common fixtures for testing agent files, YAML parsing, and context references.
"""

import pytest
from pathlib import Path


@pytest.fixture
def agents_dir():
    """Return path to agents directory."""
    return Path(__file__).parent.parent / "agents"


@pytest.fixture
def context_dir():
    """Return path to context directory."""
    return Path(__file__).parent.parent / "context"


@pytest.fixture
def sample_agent_yaml():
    """Sample valid agent YAML frontmatter."""
    return """---
meta:
  name: test-agent
  description: "A test agent for validation"

tools:
  - module: tool-filesystem
  - module: tool-grep

providers:
  - module: provider-anthropic
    config:
      model: claude-sonnet-4-5
      temperature: 0.3
---

# Test Agent

This is a test agent.
"""


@pytest.fixture
def invalid_agent_yaml():
    """Sample invalid agent YAML (missing required fields)."""
    return """---
meta:
  name: invalid-agent
---

# Invalid Agent
"""


@pytest.fixture
def all_agent_files(agents_dir):
    """Return list of all agent markdown files."""
    return sorted(agents_dir.glob("*.md"))


@pytest.fixture(params=[
    "complexity-assessor.md",
    "ensemble-coordinator.md",
    "iterative-refiner.md",
    "solution-evaluator.md"
])
def agent_file(request, agents_dir):
    """Parametrized fixture for each agent file."""
    return agents_dir / request.param
