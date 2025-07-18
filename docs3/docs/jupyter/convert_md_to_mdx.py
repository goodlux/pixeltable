#!/usr/bin/env python3
"""
Convert CommonMark .md files to Docusaurus-compatible .mdx files.
Makes minimal changes to ensure compatibility.
"""

import os
import re
import glob
from pathlib import Path

def convert_md_to_mdx(md_file_path):
    """Convert a single .md file to .mdx format."""
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Minimal changes for Docusaurus MDX compatibility:
    
    # 1. Fix any HTML comments that might interfere with JSX
    content = re.sub(r'<!--\s*(.+?)\s*-->', r'{/* \1 */}', content, flags=re.DOTALL)
    
    # 2. Handle base64 data URLs - wrap them in JSX to prevent parsing issues
    def wrap_data_url(match):
        alt_text = match.group(1)
        data_url = match.group(2)
        return f'<img alt="{alt_text}" src="{data_url}" />'
    
    # Convert markdown image syntax with data URLs to JSX img tags
    content = re.sub(r'!\[([^\]]*)\]\((data:image/[^)]+)\)', wrap_data_url, content)
    
    # 3. Escape any standalone < or > that aren't part of HTML tags or data URLs
    # This prevents JSX parsing issues
    content = re.sub(r'(?<!<)(?<!</)(?<!=")(?<!:)(<)(?![a-zA-Z/!])', r'&lt;', content)
    content = re.sub(r'(?<![a-zA-Z/])(?<!")(?<!/)(?<!;)>(?!>)', r'&gt;', content)
    
    # 3. Fix any self-closing tags to be JSX compliant (add space before />)
    content = re.sub(r'<(\w+)([^>]*[^/\s])(/?)>', r'<\1\2 \3>', content)
    content = re.sub(r'<(\w+)([^>]*)/>', r'<\1\2 />', content)
    
    # 4. Add frontmatter if it doesn't exist (Docusaurus likes this)
    if not content.startswith('---'):
        # Extract title from first heading if available
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else Path(md_file_path).stem
        
        frontmatter = f"""---
title: {title}
---

"""
        content = frontmatter + content
    
    # Create .mdx filename
    mdx_file_path = md_file_path.replace('.md', '.mdx')
    
    # Write the converted content
    with open(mdx_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return mdx_file_path

def main():
    """Convert all .md files in the current directory to .mdx."""
    
    # Find all .md files in current directory
    md_files = glob.glob('*.md')
    
    if not md_files:
        print("No .md files found in current directory.")
        return
    
    print(f"Found {len(md_files)} .md files to convert:")
    
    converted_files = []
    for md_file in md_files:
        print(f"Converting: {md_file}")
        try:
            mdx_file = convert_md_to_mdx(md_file)
            converted_files.append(mdx_file)
            print(f"  → Created: {mdx_file}")
        except Exception as e:
            print(f"  ✗ Error converting {md_file}: {e}")
    
    print(f"\nConversion complete! Created {len(converted_files)} .mdx files:")
    for mdx_file in converted_files:
        print(f"  {mdx_file}")
    
    print("\nNote: Original .md files are preserved.")
    print("You can now use the .mdx files in your Docusaurus project.")

if __name__ == "__main__":
    main()
