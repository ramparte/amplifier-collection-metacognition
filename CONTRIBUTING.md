# Contributing to Metacognition Collection

Thank you for your interest in contributing to the metacognition collection! This document provides guidelines for contributing agents, context files, tests, and documentation.

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## What We're Looking For

### New Agents
- Agents that extend metacognitive capabilities
- Agents that fill gaps in the current workflow
- Agents that implement proven patterns from research

### Context Files
- Educational content on metacognitive patterns
- Rubrics and scoring frameworks
- Best practices and mental models

### Examples
- Real-world usage scenarios
- Integration patterns with other tools
- Performance optimization techniques

### Tests
- Behavioral tests for agent outputs
- Integration tests for workflows
- Error handling scenarios

## Standards and Requirements

### Agent Contributions

When adding or modifying agents, follow these standards:

#### 1. Agent File Structure

```markdown
---
meta:
  name: agent-name
  description: "Clear, concise description of agent's purpose"

tools:
  - module: tool-filesystem
  - module: tool-bash

providers:
  - module: provider-anthropic
    config:
      model: claude-sonnet-4-5
      temperature: 0.3-0.7  # Choose based on agent needs
---

@metacognition:context/relevant-context.md

# Agent Name

Brief introduction (1-2 sentences).

## Your Role

Clear description of what this agent does.

## Your Approach

Step-by-step methodology.

## Output Format

JSON specification with example.

## Error Handling

How to handle common errors.
```

#### 2. Agent Design Principles

**Single Responsibility**:
- Each agent should do ONE thing well
- No overlap with existing agents
- Clear separation between assessment, execution, and evaluation

**Delegation Over Implementation**:
- Agents should delegate to other agents when appropriate
- Avoid duplicating functionality that exists elsewhere
- Use the task tool to spawn other agents

**Clear Communication**:
- Output formats must be well-specified
- JSON outputs should have consistent structure
- Error messages should be actionable

#### 3. Temperature Guidelines

Choose temperature based on agent purpose:
- **0.2-0.3**: Evaluation, scoring, objective assessment
- **0.3-0.4**: Coordination, routing decisions
- **0.5-0.6**: Generation, implementation, creative work
- **0.7+**: Exploratory work, brainstorming (rare)

### Context File Contributions

Context files provide educational content to agents. Follow these standards:

#### Structure
```markdown
# Title

Brief overview (what this context provides).

## Section 1: Core Concepts

Explain key ideas with examples.

## Section 2: Frameworks

Provide decision frameworks, rubrics, or mental models.

## Section 3: Examples

Show concrete examples with explanations.

## References

Link to source material, papers, or implementations.
```

#### Quality Standards
- **Actionable**: Provide frameworks agents can use
- **Specific**: Give concrete examples, not vague guidelines
- **Well-researched**: Cite sources for patterns and practices
- **Comprehensive**: Cover edge cases and error conditions

### Test Contributions

We need tests at three levels:

#### 1. Structural Tests (test_agents/)
Tests for YAML parsing, schema validation, configuration correctness.

```python
def test_agent_has_required_fields(agent_file):
    """Verify agent YAML has all required fields."""
    # Test implementation
```

#### 2. Behavioral Tests (test_behavior/)
Tests for agent output formats and decision logic.

```python
def test_complexity_assessor_output_format():
    """Verify complexity-assessor returns valid JSON."""
    # Mock LLM response
    # Validate output structure
```

#### 3. Integration Tests (test_integration/)
Tests for complete workflows and agent interactions.

```python
def test_complexity_to_iteration_workflow():
    """Test: complexity assessment → iterative refinement."""
    # Test end-to-end workflow
```

#### Test Requirements
- All tests must pass before merge
- New agents require corresponding tests
- Behavioral changes require updated tests
- Tests should use pytest conventions

### Documentation Standards

#### README Updates
When adding features, update:
- **Quick Start** section if setup changes
- **Agent Details** section for new agents
- **Examples** for new usage patterns
- **Best Practices** for new guidance

#### Example Format
Examples should follow this progression:
1. **Simple** (complexity 1-3): Basic usage
2. **Medium** (complexity 4-6): Single-pass with review
3. **Complex** (complexity 7-8): Iterative refinement
4. **Critical** (complexity 9-10): Ensemble coordination

## Coding Standards

### Markdown Formatting
- Use ATX-style headers (`#` not `===`)
- One blank line between sections
- Code blocks with language specification
- Lists with consistent indentation

### YAML Formatting
```yaml
# Comments explain non-obvious choices
meta:
  name: lowercase-with-hyphens
  description: "Quoted strings for descriptions"

tools:
  - module: tool-name
  # More tools

providers:
  - module: provider-name
    config:
      model: model-name
      temperature: 0.5  # Explain why this value
```

### Python Style
- Follow PEP 8
- Use type hints where applicable
- Docstrings for all test functions
- Descriptive test names

## Testing Your Changes

### Run All Tests
```bash
cd amplifier-collection-metacognition
pytest
```

### Run Specific Test Categories
```bash
# Structural tests
pytest tests/test_agents/

# Behavioral tests
pytest tests/test_behavior/

# Integration tests
pytest tests/test_integration/
```

### Test Coverage
```bash
pytest --cov=. --cov-report=html
```

## Pull Request Process

### Before Submitting

1. **Run all tests**: `pytest`
2. **Check agent YAML**: Validate with YAML parser
3. **Update documentation**: README, examples, context files
4. **Add tests**: For new features or behavior changes
5. **Check links**: Ensure all markdown links work

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New agent
- [ ] Agent modification
- [ ] Context file addition/update
- [ ] Test addition
- [ ] Documentation update
- [ ] Bug fix

## Checklist
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation
- [ ] Followed agent design principles
- [ ] No broken links in markdown

## Testing
Describe how you tested these changes.

## Related Issues
Link to related issues or discussions.
```

### Review Criteria

PRs will be reviewed for:
1. **Alignment with principles**: Ruthless simplicity, clear separation
2. **Test coverage**: Appropriate tests for changes
3. **Documentation quality**: Clear, actionable, comprehensive
4. **Code quality**: Follows standards, no breaking changes
5. **Performance**: No significant regression

## Design Philosophy

Contributions should align with these principles:

### Ruthless Simplicity
- Agents are markdown files, not code
- No complex orchestration logic
- Direct, obvious solutions

### Measurement Over Prediction
- Use soft scoring (0.0-1.0) to track progress
- Provide specific, measurable feedback
- Don't guess outcomes, measure them

### Present-Moment Focus
- Solve current problems, not future hypotheticals
- No premature optimization
- Clear about what works now

### Code for Structure, AI for Intelligence
- Code orchestrates, LLM thinks
- Configuration over computation
- Let agents make decisions

## Getting Help

### Questions?
- Open a GitHub Discussion for general questions
- Open an Issue for bugs or feature requests
- Review existing examples and documentation

### Need Clarification?
- Check the [README](README.md) for overview
- Review [context files](context/) for patterns
- Look at [examples](examples/) for usage

### Want to Propose Major Changes?
1. Open an Issue first to discuss
2. Explain the problem you're solving
3. Propose your approach
4. Get feedback before implementing

## Recognition

Contributors will be recognized in:
- Git commit history
- Release notes for significant contributions
- Documentation acknowledgments

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

### Our Standards

**Positive behaviors**:
- Respectful and inclusive language
- Welcoming diverse perspectives
- Gracefully accepting constructive criticism
- Focusing on what's best for the community

**Unacceptable behaviors**:
- Harassment or discriminatory language
- Personal attacks
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Maintainers will:
1. Provide clear feedback on unacceptable behavior
2. Remove inappropriate comments or contributions
3. Ban repeat offenders from the project

Report violations to project maintainers.

---

**Thank you for contributing to the metacognition collection!**

Your contributions help advance metacognitive AI patterns and improve adaptive problem-solving.
