#!/usr/bin/env python3
"""
Convert .md files to .mdx with frontmatter
"""

import os
import re
import glob

def convert_md_to_mdx(md_file):
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Extract title from filename or first H1
    title = os.path.basename(md_file).replace('.md', '').replace('_', ' ').replace('-', ' ').title()
    
    # Look for H1 in content
    h1_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        # Remove the H1 from content
        content = re.sub(r'^#\s+.+\n?', '', content, count=1, flags=re.MULTILINE)
    
    # Extract description
    description = 'Jupyter notebook example for Pixeltable'
    lines = content.split('\n')
    for line in lines:
        clean_line = line.strip()
        if clean_line and not clean_line.startswith('#') and len(clean_line) > 30:
            description = re.sub(r'[*_`]', '', clean_line)
            if len(description) > 150:
                description = description[:147] + '...'
            break
    
    # Clean for YAML
    title = title.replace('"', '\\"')
    description = description.replace('"', '\\"')
    
    # Create frontmatter
    frontmatter = f'''---
title: "{title}"
description: "{description}"
---

'''
    
    # Clean content for MDX
    content = re.sub(r'!\[png\]\([^)]+\)', ':::note\n📊 Chart/image output (rendered in notebook)\n:::', content)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    
    # Write as .mdx file
    mdx_file = md_file.replace('.md', '.mdx')
    with open(mdx_file, 'w') as f:
        f.write(frontmatter + content)
    
    # Remove original .md file
    os.remove(md_file)
    print(f'Converted {os.path.basename(md_file)} to {os.path.basename(mdx_file)}')

if __name__ == "__main__":
    # Process all .md files
    for md_file in glob.glob('docs3/docs/examples/**/*.md', recursive=True):
        convert_md_to_mdx(md_file)
