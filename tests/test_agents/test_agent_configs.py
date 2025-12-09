"""
Test agent configuration and documentation.

Validates agent configuration settings and documentation quality.
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


def test_agent_has_description_section(agent_file):
    """Test that agent has a description section in markdown content.
    
    Parametrized test checking:
    - Markdown content exists after frontmatter
    - Agent has a title/heading
    - Agent has descriptive content
    """
    content = agent_file.read_text()
    markdown_content = extract_content_after_frontmatter(content).strip()
    
    assert len(markdown_content) > 0, \
        f"{agent_file.name} has no content after YAML frontmatter"
    
    # Should have at least one heading
    assert '#' in markdown_content, \
        f"{agent_file.name} should have at least one markdown heading"
    
    # Should have substantial content (more than just headings)
    # Remove markdown headings and check remaining content
    content_without_headings = re.sub(r'^#+\s+.*$', '', markdown_content, flags=re.MULTILINE)
    content_without_headings = content_without_headings.strip()
    
    assert len(content_without_headings) > 100, \
        f"{agent_file.name} should have substantial descriptive content (not just headings)"


def test_agent_provider_config_valid(agent_file):
    """Test that agent provider configuration is valid.
    
    Parametrized test validating:
    - Provider module names are valid
    - Config has expected structure
    - Model names follow conventions
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    providers = yaml_data['providers']
    
    for i, provider in enumerate(providers):
        module = provider['module']
        
        # Module should follow naming convention (provider-*)
        assert module.startswith('provider-'), \
            f"{agent_file.name} provider {i} module '{module}' should start with 'provider-'"
        
        # If config exists, validate it
        if 'config' in provider:
            config = provider['config']
            
            # If model is specified, check it's a string
            if 'model' in config:
                model = config['model']
                assert isinstance(model, str), \
                    f"{agent_file.name} provider {i} model must be a string"
                assert len(model) > 0, \
                    f"{agent_file.name} provider {i} model cannot be empty"
                
                # Model should be a reasonable value (not placeholder)
                assert model != "MODEL_NAME", \
                    f"{agent_file.name} provider {i} model appears to be a placeholder"


def test_agent_temperature_in_range(agent_file):
    """Test that agent temperature settings are in valid range.
    
    Parametrized test checking:
    - Temperature is between 0.0 and 2.0
    - Temperature is numeric (int or float)
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    providers = yaml_data['providers']
    
    for i, provider in enumerate(providers):
        if 'config' in provider and 'temperature' in provider['config']:
            temp = provider['config']['temperature']
            
            # Temperature must be numeric
            assert isinstance(temp, (int, float)), \
                f"{agent_file.name} provider {i} temperature must be numeric"
            
            # Temperature should be in reasonable range (0.0 to 2.0 for most LLMs)
            assert 0.0 <= temp <= 2.0, \
                f"{agent_file.name} provider {i} temperature {temp} should be between 0.0 and 2.0"


def test_all_agents_documented(all_agent_files):
    """Test that all agents have clear purpose documentation.
    
    Validates:
    - Each agent has a description in meta
    - Each agent has markdown documentation
    - Descriptions are meaningful (not placeholders)
    """
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        yaml_data = extract_yaml_frontmatter(content)
        
        # Check meta.description
        description = yaml_data['meta']['description']
        assert len(description) > 10, \
            f"{agent_file.name} description is too short: '{description}'"
        
        # Check for placeholder text
        placeholder_words = ['TODO', 'TBD', 'placeholder', 'example']
        description_lower = description.lower()
        for word in placeholder_words:
            assert word not in description_lower, \
                f"{agent_file.name} description contains placeholder text: '{word}'"
        
        # Check markdown content
        markdown_content = extract_content_after_frontmatter(content)
        assert len(markdown_content.strip()) > 50, \
            f"{agent_file.name} has insufficient markdown documentation"


def test_agent_has_valid_tools(agent_file):
    """Test that agent tools configuration is valid.
    
    Parametrized test checking:
    - Tools list is properly formatted
    - Tool modules follow naming convention
    - No duplicate tools
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    tools = yaml_data['tools']
    tool_modules = []
    
    for i, tool in enumerate(tools):
        module = tool['module']
        
        # Check naming convention
        assert module.startswith('tool-'), \
            f"{agent_file.name} tool {i} module '{module}' should start with 'tool-'"
        
        # Check for duplicates
        assert module not in tool_modules, \
            f"{agent_file.name} has duplicate tool: {module}"
        
        tool_modules.append(module)


def test_agent_meta_fields_quality(agent_file):
    """Test quality of agent meta fields.
    
    Parametrized test ensuring:
    - Name uses kebab-case
    - Description is a sentence with proper capitalization
    - No trailing whitespace
    """
    content = agent_file.read_text()
    yaml_data = extract_yaml_frontmatter(content)
    
    meta = yaml_data['meta']
    name = meta['name']
    description = meta['description']
    
    # Name should be kebab-case (lowercase with hyphens)
    assert name == name.lower(), \
        f"{agent_file.name} meta.name should be lowercase"
    
    assert '-' in name or name.isalnum(), \
        f"{agent_file.name} meta.name should use kebab-case (lowercase-with-hyphens)"
    
    # Description should not have leading/trailing whitespace
    assert description == description.strip(), \
        f"{agent_file.name} meta.description has leading/trailing whitespace"
    
    # Description should be properly capitalized or quoted
    if not description.startswith('"'):
        # If not quoted, first word should be capitalized
        first_word = description.split()[0] if description.split() else ""
        # Allow lowercase if it's a technical term
        if first_word and not first_word[0].isupper() and first_word not in ['agent', 'tool', 'module']:
            pytest.fail(f"{agent_file.name} meta.description should start with capital letter or be quoted")


def test_agent_has_coherent_role_description(agent_file):
    """Test that agent has a coherent role description.
    
    Parametrized test checking:
    - Agent describes its role or purpose
    - Common section headers are present (Your Role, Your Approach, etc.)
    """
    content = agent_file.read_text()
    markdown_content = extract_content_after_frontmatter(content).lower()
    
    # Look for role/purpose indicators
    role_indicators = [
        'your role',
        'your approach',
        'your task',
        'you analyze',
        'you implement',
        'you coordinate'
    ]
    
    has_role_description = any(indicator in markdown_content for indicator in role_indicators)
    
    assert has_role_description, \
        f"{agent_file.name} should clearly describe the agent's role or approach"
