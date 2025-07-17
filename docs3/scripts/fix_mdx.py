#!/usr/bin/env python3
"""
Fix MDX parsing issues by cleaning problematic content
"""

import re
import sys

def fix_mdx_file(file_path):
    """Fix common MDX parsing issues"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Original file size: {len(content):,} characters")
    
    # Split into lines to find the problematic area
    lines = content.split('\n')
    print(f"Total lines: {len(lines)}")
    
    if len(lines) > 127:
        print(f"Line 127: {lines[126][:100]}...")
    
    # Remove problematic outputs that break MDX
    
    # 1. Remove very long code blocks (likely data dumps)
    def limit_code_blocks(match):
        block_content = match.group(1)
        if len(block_content) > 5000:  # Very long blocks
            return "```\n# Large output truncated for documentation\n```"
        return match.group(0)
    
    content = re.sub(r'```(?:python|text|bash)?\n(.*?)\n```', limit_code_blocks, content, flags=re.DOTALL)
    
    # 2. Fix unescaped curly braces (breaks MDX)
    content = re.sub(r'(?<!`){(?!{)', '\\{', content)
    content = re.sub(r'(?<!`)(?<!{)}(?!})', '\\}', content) 
    
    # 3. Fix unescaped angle brackets
    content = re.sub(r'<(?![a-zA-Z/!])', '&lt;', content)
    content = re.sub(r'(?<![a-zA-Z])>(?![a-zA-Z])', '&gt;', content)
    
    # 4. Remove HTML style blocks that break MDX
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    
    # 5. Fix bare URLs that might confuse parser
    content = re.sub(r'(?<!\[)(?<!\()https?://[^\s<>"\[\]]+', lambda m: f'<{m.group()}>', content)
    
    # 6. Remove very long lines that might cause issues
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        if len(line) > 1000:
            cleaned_lines.append(line[:500] + '... (truncated)')
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    print(f"Cleaned file size: {len(content):,} characters")
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {file_path}")

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "docs3/docs/examples/pixeltable-basics.mdx"
    fix_mdx_file(file_path)
