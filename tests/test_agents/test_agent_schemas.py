"""
Test agent YAML schema validation.

Validates that all agent files have correct YAML frontmatter with required fields.
"""

import pytest
import yaml
import re
from pathlib import Path


def extract_yaml_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown file."""
    # Match content between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    
    yaml_content = match.group(1)
    return yaml.safe_load(yaml_content)


def test_all_agents_have_valid_yaml(all_agent_files):
    """Test that all agent files have parseable YAML frontmatter.
    
    Validates:
    - YAML frontmatter exists
    - YAML is valid and parseable
    - No syntax errors
    """
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        
        # Check for YAML delimiters
        assert content.startswith('---\n'), f"{agent_file.name} missing YAML frontmatter opening delimiter"
        
        # Extract and parse YAML
        yaml_data = extract_yaml_frontmatter(content)
        assert yaml_data is not None, f"{agent_file.name} has invalid YAML frontmatter"
        assert isinstance(yaml_data, dict), f"{agent_file.name} YAML must be a dictionary"


def test_agent_has_required_fields(agent_file):
    """Test that agent has all required YAML fields.
    
    Parametrized test checking:
    - meta.name exists
    - meta.description exists
    - tools list exists
    - providers list exists
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    assert yaml_data is not None, f"{agent_file.name} missing YAML frontmatter"
    
    # Check meta section
    assert 'meta' in yaml_data, f"{agent_file.name} missing 'meta' section"
    assert isinstance(yaml_data['meta'], dict), f"{agent_file.name} 'meta' must be a dictionary"
    
    # Check meta.name
    assert 'name' in yaml_data['meta'], f"{agent_file.name} missing 'meta.name'"
    assert isinstance(yaml_data['meta']['name'], str), f"{agent_file.name} 'meta.name' must be a string"
    assert len(yaml_data['meta']['name']) > 0, f"{agent_file.name} 'meta.name' cannot be empty"
    
    # Check meta.description
    assert 'description' in yaml_data['meta'], f"{agent_file.name} missing 'meta.description'"
    assert isinstance(yaml_data['meta']['description'], str), f"{agent_file.name} 'meta.description' must be a string"
    assert len(yaml_data['meta']['description']) > 0, f"{agent_file.name} 'meta.description' cannot be empty"
    
    # Check tools
    assert 'tools' in yaml_data, f"{agent_file.name} missing 'tools' section"
    assert isinstance(yaml_data['tools'], list), f"{agent_file.name} 'tools' must be a list"
    
    # Check providers
    assert 'providers' in yaml_data, f"{agent_file.name} missing 'providers' section"
    assert isinstance(yaml_data['providers'], list), f"{agent_file.name} 'providers' must be a list"


def test_agent_meta_name_matches_filename(agent_file):
    """Test that agent meta.name matches filename.
    
    Parametrized test ensuring consistency:
    - complexity-assessor.md → meta.name: complexity-assessor
    - ensemble-coordinator.md → meta.name: ensemble-coordinator
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    expected_name = agent_file.stem  # filename without extension
    actual_name = yaml_data['meta']['name']
    
    assert actual_name == expected_name, \
        f"{agent_file.name} meta.name '{actual_name}' should match filename '{expected_name}'"


def test_agent_providers_structure(agent_file):
    """Test that providers list has correct structure.
    
    Parametrized test validating:
    - Each provider has 'module' field
    - Each provider has 'config' field (optional but common)
    - Config contains model and temperature if present
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    providers = yaml_data['providers']
    assert len(providers) > 0, f"{agent_file.name} must have at least one provider"
    
    for i, provider in enumerate(providers):
        assert isinstance(provider, dict), \
            f"{agent_file.name} provider {i} must be a dictionary"
        
        assert 'module' in provider, \
            f"{agent_file.name} provider {i} missing 'module' field"
        
        assert isinstance(provider['module'], str), \
            f"{agent_file.name} provider {i} 'module' must be a string"
        
        # If config exists, validate its structure
        if 'config' in provider:
            config = provider['config']
            assert isinstance(config, dict), \
                f"{agent_file.name} provider {i} 'config' must be a dictionary"
            
            # Common fields in config
            if 'model' in config:
                assert isinstance(config['model'], str), \
                    f"{agent_file.name} provider {i} config.model must be a string"
            
            if 'temperature' in config:
                temp = config['temperature']
                assert isinstance(temp, (int, float)), \
                    f"{agent_file.name} provider {i} config.temperature must be numeric"


def test_agent_tools_structure(agent_file):
    """Test that tools list has correct structure.
    
    Parametrized test validating:
    - Each tool has 'module' field
    - Module names follow expected pattern (tool-*)
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    tools = yaml_data['tools']
    # Tools can be empty, but if present must be valid
    
    for i, tool in enumerate(tools):
        assert isinstance(tool, dict), \
            f"{agent_file.name} tool {i} must be a dictionary"
        
        assert 'module' in tool, \
            f"{agent_file.name} tool {i} missing 'module' field"
        
        assert isinstance(tool['module'], str), \
            f"{agent_file.name} tool {i} 'module' must be a string"
        
        # Tool modules typically start with 'tool-'
        module_name = tool['module']
        assert module_name.startswith('tool-'), \
            f"{agent_file.name} tool {i} module '{module_name}' should start with 'tool-'"


def test_agent_yaml_frontmatter_delimiter(agent_file):
    """Test that YAML frontmatter has correct delimiters.
    
    Parametrized test ensuring:
    - File starts with '---'
    - YAML ends with '---'
    - Delimiters are on their own lines
    """
    content = agent_file.read_text()
    lines = content.split('\n')
    
    # Check opening delimiter
    assert lines[0] == '---', \
        f"{agent_file.name} must start with '---' on first line"
    
    # Find closing delimiter
    closing_delimiter_found = False
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            closing_delimiter_found = True
            # Check there's content after closing delimiter
            remaining_content = '\n'.join(lines[i+1:]).strip()
            assert len(remaining_content) > 0, \
                f"{agent_file.name} must have content after YAML frontmatter"
            break
    
    assert closing_delimiter_found, \
        f"{agent_file.name} missing closing '---' delimiter for YAML frontmatter"
