#!/usr/bin/env python3
"""
Clean HTML/MDX issues in converted notebooks
"""

import re
import glob
from pathlib import Path

def fix_html_tags(content):
    """Fix common HTML tag issues for MDX compatibility"""
    
    # Remove or fix unclosed HTML tags that break MDX
    # Common problematic tags from notebook outputs
    problematic_patterns = [
        r'<ul[^>]*>(?![^<]*</ul>)',  # Unclosed ul tags
        r'<ol[^>]*>(?![^<]*</ol>)',  # Unclosed ol tags  
        r'<li[^>]*>(?![^<]*</li>)',  # Unclosed li tags
        r'<div[^>]*>(?![^<]*</div>)', # Unclosed div tags
        r'<span[^>]*>(?![^<]*</span>)', # Unclosed span tags
        r'<p[^>]*>(?![^<]*</p>)',    # Unclosed p tags
    ]
    
    for pattern in problematic_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove HTML tables that often have formatting issues
    content = re.sub(r'<table[^>]*>.*?</table>', ':::note\nTable output (view in original notebook)\n:::', content, flags=re.DOTALL)
    
    # Remove style attributes that break MDX
    content = re.sub(r'<([^>]+)\s+style="[^"]*"([^>]*)>', r'<\1\2>', content)
    
    # Remove other problematic attributes
    content = re.sub(r'<([^>]+)\s+class="[^"]*"([^>]*)>', r'<\1\2>', content)
    
    # Convert self-closing tags to proper format
    content = re.sub(r'<(br|hr|img)([^>]*)(?<!/)>', r'<\1\2 />', content)
    
    return content

def clean_mdx_file(file_path):
    """Clean a single MDX file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Cleaning: {file_path}")
    
    # Fix HTML tags
    content = fix_html_tags(content)
    
    # Fix other MDX issues
    # Escape curly braces outside of code blocks
    def escape_braces_outside_code(text):
        parts = []
        in_code_block = False
        in_inline_code = False
        
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                parts.append(line)
            elif in_code_block:
                parts.append(line)
            else:
                # Handle inline code
                new_line = ""
                i = 0
                while i < len(line):
                    if line[i] == '`':
                        in_inline_code = not in_inline_code
                        new_line += line[i]
                    elif not in_inline_code and line[i] == '{':
                        new_line += '\\{'
                    elif not in_inline_code and line[i] == '}':
                        new_line += '\\}'
                    else:
                        new_line += line[i]
                    i += 1
                parts.append(new_line)
        
        return '\n'.join(parts)
    
    content = escape_braces_outside_code(content)
    
    # Remove very long lines that might cause parsing issues
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        if len(line) > 2000:
            cleaned_lines.append('<!-- Very long line truncated for documentation -->')
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Cleaned")

def main():
    """Clean all MDX files in the examples directory"""
    
    pattern = "docs3/docs/examples/**/*.mdx"
    mdx_files = glob.glob(pattern, recursive=True)
    
    # Skip index files
    mdx_files = [f for f in mdx_files if not f.endswith('index.mdx')]
    
    print(f"🧹 Cleaning {len(mdx_files)} MDX files...")
    
    for file_path in mdx_files:
        clean_mdx_file(file_path)
    
    print("✅ All files cleaned!")

if __name__ == "__main__":
    main()
