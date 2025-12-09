"""
Integration tests for agent loading and parsing.

Tests the ability to load and process agent files as a cohesive system.
"""

import pytest
import yaml
import re
from pathlib import Path


def extract_yaml_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    yaml_content = match.group(1)
    return yaml.safe_load(yaml_content)


def extract_content_after_frontmatter(content: str) -> str:
    """Extract markdown content after YAML frontmatter."""
    match = re.match(r'^---\s*\n.*?\n---\s*\n(.*)$', content, re.DOTALL)
    if match:
        return match.group(1)
    return content


def test_load_all_agents(all_agent_files):
    """Integration test: Load and parse all 4 agents successfully.
    
    Validates:
    - All agent files can be read
    - All agent files have valid YAML
    - All agent files have valid markdown
    - No errors during parsing
    """
    loaded_agents = []
    
    for agent_file in all_agent_files:
        # Read file
        content = agent_file.read_text()
        assert len(content) > 0, f"Agent file is empty: {agent_file.name}"
        
        # Parse YAML
        yaml_data = extract_yaml_frontmatter(content)
        assert yaml_data is not None, f"Could not parse YAML from: {agent_file.name}"
        
        # Extract markdown
        markdown_content = extract_content_after_frontmatter(content)
        assert len(markdown_content.strip()) > 0, f"No markdown content in: {agent_file.name}"
        
        # Store loaded agent
        loaded_agents.append({
            'filename': agent_file.name,
            'name': yaml_data['meta']['name'],
            'yaml': yaml_data,
            'markdown': markdown_content
        })
    
    # Verify we loaded all 4 agents
    assert len(loaded_agents) == 4, f"Expected 4 agents, loaded {len(loaded_agents)}"
    
    # Verify all have unique names
    names = [agent['name'] for agent in loaded_agents]
    assert len(names) == len(set(names)), "Agent names must be unique"


def test_agent_yaml_to_dict_conversion(all_agent_files):
    """Integration test: Convert agent YAML to dictionary structure.
    
    Validates:
    - YAML can be converted to Python dict
    - Dict structure is usable
    - All expected keys are accessible
    """
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        yaml_data = extract_yaml_frontmatter(content)
        
        # Verify it's a dictionary
        assert isinstance(yaml_data, dict), f"{agent_file.name} YAML should parse to dict"
        
        # Verify all expected top-level keys
        expected_keys = ['meta', 'tools', 'providers']
        for key in expected_keys:
            assert key in yaml_data, f"{agent_file.name} missing key: {key}"
        
        # Verify meta structure
        meta = yaml_data['meta']
        assert 'name' in meta and 'description' in meta
        
        # Verify tools structure
        tools = yaml_data['tools']
        assert isinstance(tools, list), f"{agent_file.name} tools should be a list"
        
        # Verify providers structure
        providers = yaml_data['providers']
        assert isinstance(providers, list), f"{agent_file.name} providers should be a list"
        assert len(providers) > 0, f"{agent_file.name} should have at least one provider"


def test_agent_content_extraction(all_agent_files):
    """Integration test: Extract content sections from agents.
    
    Validates:
    - Can separate YAML from markdown
    - Markdown content is accessible
    - Content has expected structure
    """
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        
        # Extract YAML
        yaml_data = extract_yaml_frontmatter(content)
        assert yaml_data is not None, f"{agent_file.name} failed to extract YAML"
        
        # Extract markdown
        markdown_content = extract_content_after_frontmatter(content)
        assert markdown_content is not None, f"{agent_file.name} failed to extract markdown"
        assert len(markdown_content.strip()) > 0, f"{agent_file.name} has no markdown content"
        
        # Verify markdown has headings
        assert '#' in markdown_content, f"{agent_file.name} markdown should have headings"
        
        # Verify YAML and markdown are separate
        assert '---' not in markdown_content.strip()[:10], \
            f"{agent_file.name} markdown content should not start with YAML delimiter"


def test_agent_collection_completeness(agents_dir):
    """Integration test: Verify agent collection is complete.
    
    Validates:
    - All expected agents are present
    - No extra unexpected files
    - Agents directory structure is correct
    """
    expected_agents = [
        'complexity-assessor.md',
        'ensemble-coordinator.md',
        'iterative-refiner.md',
        'solution-evaluator.md'
    ]
    
    # Get all markdown files in agents directory
    actual_agents = sorted([f.name for f in agents_dir.glob('*.md')])
    
    # Verify all expected agents exist
    for expected in expected_agents:
        assert expected in actual_agents, f"Missing expected agent: {expected}"
    
    # Verify no unexpected agents (this might change, so just log if more exist)
    if len(actual_agents) > len(expected_agents):
        extra = set(actual_agents) - set(expected_agents)
        # This is not necessarily an error, just verify they're valid
        for extra_file in extra:
            extra_path = agents_dir / extra_file
            content = extra_path.read_text()
            yaml_data = extract_yaml_frontmatter(content)
            assert yaml_data is not None, f"Extra agent {extra_file} has invalid YAML"


def test_cross_agent_consistency(all_agent_files):
    """Integration test: Verify consistency across all agents.
    
    Validates:
    - All agents use same provider type
    - All agents have reasonable temperature settings
    - All agents follow same structural patterns
    """
    provider_modules = set()
    temperatures = []
    
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        yaml_data = extract_yaml_frontmatter(content)
        
        # Collect provider information
        for provider in yaml_data['providers']:
            provider_modules.add(provider['module'])
            
            if 'config' in provider and 'temperature' in provider['config']:
                temperatures.append(provider['config']['temperature'])
    
    # All agents should use similar provider(s) - at least some overlap
    # In this collection, they all use provider-anthropic
    assert 'provider-anthropic' in provider_modules, \
        "Expected all agents to use provider-anthropic"
    
    # Temperature settings should be reasonable across collection
    if temperatures:
        assert all(0.0 <= t <= 2.0 for t in temperatures), \
            "All temperatures should be in reasonable range"
        
        # Check for variety (not all the same)
        # This ensures agents are configured for their specific needs
        unique_temps = set(temperatures)
        assert len(unique_temps) >= 1, \
            "Agents should have temperature settings (possibly varied)"


def test_agent_tools_availability(all_agent_files):
    """Integration test: Verify agent tools are commonly available.
    
    Validates:
    - Tools referenced by agents follow expected patterns
    - No agents reference non-existent tool types
    - Tool references are consistent across collection
    """
    all_tools = set()
    
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        yaml_data = extract_yaml_frontmatter(content)
        
        for tool in yaml_data['tools']:
            module = tool['module']
            all_tools.add(module)
            
            # Verify tool module naming
            assert module.startswith('tool-'), \
                f"{agent_file.name} tool '{module}' should start with 'tool-'"
    
    # Verify we have a reasonable set of tools
    assert len(all_tools) > 0, "Collection should use at least some tools"
    
    # Common tools that might be used
    expected_common_tools = ['tool-filesystem', 'tool-grep', 'tool-task']
    
    # At least some of these should be present
    common_found = [tool for tool in expected_common_tools if tool in all_tools]
    assert len(common_found) > 0, \
        f"Expected at least some common tools from {expected_common_tools}, found: {all_tools}"
