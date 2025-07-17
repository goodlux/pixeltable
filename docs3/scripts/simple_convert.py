#!/usr/bin/env python3
"""
Simple fallback converter using nbformat
"""

import json
import os
import sys

def convert_notebook_simple(notebook_path, output_path):
    """Simple notebook to markdown conversion"""
    
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Extract title
    title = os.path.basename(notebook_path).replace('.ipynb', '').replace('_', ' ').title()
    
    # Start with frontmatter
    content = f"""---
title: "{title}"
description: "Jupyter notebook example for Pixeltable"
---

# {title}

"""
    
    # Process cells
    for cell in notebook.get('cells', []):
        cell_type = cell.get('cell_type')
        source = ''.join(cell.get('source', []))
        
        if cell_type == 'markdown':
            # Skip first H1 if it exists
            if content.count('\n') < 10 and source.strip().startswith('# '):
                source = '\n'.join(source.split('\n')[1:])
            content += source + '\n\n'
            
        elif cell_type == 'code':
            if source.strip():
                content += f"```python\n{source}\n```\n\n"
                
                # Add simple output indication
                outputs = cell.get('outputs', [])
                if outputs:
                    content += "```\n# Output generated (see notebook for details)\n```\n\n"
    
    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Converted: {output_path}")

if __name__ == "__main__":
    notebook_path = sys.argv[1] if len(sys.argv) > 1 else "docs/notebooks/pixeltable-basics.ipynb"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "docs3/docs/examples/pixeltable-basics.mdx"
    
    convert_notebook_simple(notebook_path, output_path)
