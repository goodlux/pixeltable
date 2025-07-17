#!/usr/bin/env python3
"""
Convert .md files to .md with frontmatter (skip MDX entirely)
"""

import os
import re
import glob

def add_frontmatter_to_md(md_file):
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Extract title from filename or first H1
    title = os.path.basename(md_file).replace('.md', '').replace('_', ' ').replace('-', ' ').title()
    
    # Look for H1 in content
    h1_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        # Remove the H1 from content since it'll be in frontmatter
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
    
    # Write back as .md (not .mdx)
    with open(md_file, 'w') as f:
        f.write(frontmatter + content)
    
    print(f'✅ Added frontmatter to {os.path.basename(md_file)}')

if __name__ == "__main__":
    # Process all .md files
    for md_file in glob.glob('docs3/docs/examples/**/*.md', recursive=True):
        add_frontmatter_to_md(md_file)
