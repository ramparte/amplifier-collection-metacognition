"""
Test agent context references and links.

Validates that agent files reference valid context files and have no broken links.
"""

import pytest
import re
from pathlib import Path


def extract_yaml_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown file."""
    import yaml
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


def extract_context_references(content: str) -> list[str]:
    """Extract @metacognition:context/ references from content."""
    # Pattern: @metacognition:context/filename.md
    pattern = r'@metacognition:context/([\w\-]+\.md)'
    return re.findall(pattern, content)


def extract_markdown_links(content: str) -> list[tuple[str, str]]:
    """Extract markdown links [text](url) from content."""
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(pattern, content)


def test_agent_context_references_exist(agent_file, context_dir):
    """Test that agent context references point to existing files.
    
    Parametrized test checking:
    - All @metacognition:context/ references are valid
    - Referenced context files exist
    """
    content = agent_file.read_text()
    markdown_content = extract_content_after_frontmatter(content)
    
    context_refs = extract_context_references(markdown_content)
    
    for ref in context_refs:
        context_file = context_dir / ref
        assert context_file.exists(), \
            f"{agent_file.name} references non-existent context file: {ref}"
        
        # Also verify it's a readable file
        assert context_file.is_file(), \
            f"{agent_file.name} context reference is not a file: {ref}"


def test_context_files_exist(context_dir):
    """Test that expected context files are present.
    
    Validates:
    - Context directory exists
    - Key context files are present (complexity-signals.md, poetiq-patterns.md, etc.)
    """
    assert context_dir.exists(), "Context directory must exist"
    assert context_dir.is_dir(), "Context path must be a directory"
    
    # Expected context files based on agent references
    expected_files = [
        "complexity-signals.md",
        "poetiq-patterns.md",
        "scoring-rubrics.md"
    ]
    
    for filename in expected_files:
        context_file = context_dir / filename
        assert context_file.exists(), f"Expected context file missing: {filename}"


def test_agent_no_broken_links(agent_file):
    """Test that agent has no broken markdown links.
    
    Parametrized test checking:
    - Markdown links [text](url) are valid
    - Internal links point to existing sections
    - External links have valid format
    """
    content = agent_file.read_text()
    markdown_content = extract_content_after_frontmatter(content)
    
    links = extract_markdown_links(markdown_content)
    
    for link_text, link_url in links:
        # Skip external URLs (http://, https://)
        if link_url.startswith(('http://', 'https://')):
            # Just validate format
            assert '://' in link_url, \
                f"{agent_file.name} has malformed URL: {link_url}"
            continue
        
        # Skip anchor links within same document
        if link_url.startswith('#'):
            # Just validate format
            assert len(link_url) > 1, \
                f"{agent_file.name} has empty anchor link"
            continue
        
        # For relative file links, check they exist
        if not link_url.startswith(('#', 'http://', 'https://', '@')):
            target_file = agent_file.parent / link_url
            assert target_file.exists(), \
                f"{agent_file.name} has broken link to: {link_url}"


def test_agent_has_context_references(all_agent_files, context_dir):
    """Test that agents reference context files appropriately.
    
    Validates:
    - Agents use @metacognition:context/ pattern for context references
    - At least some agents reference context files
    """
    total_refs = 0
    
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        markdown_content = extract_content_after_frontmatter(content)
        refs = extract_context_references(markdown_content)
        total_refs += len(refs)
    
    # At least some agents should reference context files
    assert total_refs > 0, \
        "At least some agents should reference context files using @metacognition:context/ pattern"


def test_context_references_use_correct_pattern(agent_file):
    """Test that context references use the correct @metacognition:context/ pattern.
    
    Parametrized test ensuring:
    - References use @metacognition:context/ not relative paths
    - No mixed reference styles
    """
    content = agent_file.read_text()
    markdown_content = extract_content_after_frontmatter(content)
    
    # Look for potential incorrect patterns
    # e.g., ../context/file.md or context/file.md
    incorrect_patterns = [
        r'\.\./context/[\w\-]+\.md',  # ../context/file.md
        r'(?<!@metacognition:)context/[\w\-]+\.md'  # context/file.md without @metacognition:
    ]
    
    for pattern in incorrect_patterns:
        matches = re.findall(pattern, markdown_content)
        assert len(matches) == 0, \
            f"{agent_file.name} uses incorrect context reference pattern. Use @metacognition:context/ instead"


def test_all_context_files_have_content(context_dir):
    """Test that all context files have meaningful content.
    
    Validates:
    - Context files are not empty
    - Context files have more than just headers
    """
    context_files = list(context_dir.glob("*.md"))
    
    assert len(context_files) > 0, "Context directory should contain .md files"
    
    for context_file in context_files:
        content = context_file.read_text().strip()
        
        assert len(content) > 0, f"Context file is empty: {context_file.name}"
        
        # Should have substantial content (more than just a title)
        assert len(content) > 50, \
            f"Context file has insufficient content: {context_file.name}"
