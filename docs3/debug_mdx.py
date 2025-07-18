#!/usr/bin/env python3
"""Debug MDX parsing issues by examining specific lines."""

import sys

def check_line(filename, line_number):
    """Check a specific line and surrounding context for MDX issues."""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Show context around the problematic line
    start = max(0, line_number - 6)
    end = min(len(lines), line_number + 5)
    
    print(f"Examining {filename} around line {line_number}:")
    print("=" * 60)
    
    for i in range(start, end):
        marker = ">>> " if i == line_number - 1 else "    "
        print(f"{marker}{i+1:3d}: {lines[i].rstrip()}")
    
    # Check for common MDX issues in the problematic area
    problem_line = lines[line_number - 1] if line_number <= len(lines) else ""
    
    print("\n" + "=" * 60)
    print("ANALYSIS:")
    
    # Check for unescaped curly braces
    if '{' in problem_line or '}' in problem_line:
        print("⚠️  Found curly braces - these need to be escaped in MDX")
        print(f"   Line content: {problem_line.strip()}")
        
        # Show where the braces are
        for i, char in enumerate(problem_line):
            if char in '{}':
                print(f"   Curly brace '{char}' at position {i+1}")
    
    # Check for other common issues
    if 'data:image' in problem_line:
        print("⚠️  Found data URL - these can cause parsing issues")
    
    if problem_line.strip().startswith('```') or problem_line.strip().endswith('```'):
        print("⚠️  Found code block delimiter - check for proper escaping")
    
    return problem_line

if __name__ == "__main__":
    filename = "/Users/rob/repos/pixeltable/docs3/docs/jupyter/audio-transcriptions.mdx"
    line_number = 323
    
    check_line(filename, line_number)
