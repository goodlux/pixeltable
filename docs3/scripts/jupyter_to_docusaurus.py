#!/usr/bin/env python3
"""
🎭 THE GREAT JUPYTER → DOCUSAURUS TRANSMOGRIFICATION ENGINE 🎭

Transmutes sacred .ipynb scrolls into noble .mdx parchments
for the Docusaurus documentation realm!
"""

import json
import re
import os
import argparse
import html
from pathlib import Path
from typing import Dict, List, Any

class JupyterToDocusaurusAlchemist:
    """The Grand Alchemist of Notebook Transformation"""
    
    def __init__(self):
        self.cell_counter = 0
        
    def transmute_notebook(self, notebook_path: str, output_dir: str = None) -> str:
        """Main transmutation ritual"""
        print(f"🔮 Transmuting {notebook_path}...")
        
        # Read the sacred notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Extract title from filename or first markdown cell
        title = self._extract_title(notebook, notebook_path)
        
        # Begin the transformation
        mdx_content = self._create_frontmatter(title, notebook)
        mdx_content += self._transmute_cells(notebook['cells'])
        
        # Determine output path
        if output_dir is None:
            output_dir = os.path.dirname(notebook_path)
            
        output_path = self._generate_output_path(notebook_path, output_dir)
        
        # Write the transformed parchment
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mdx_content)
            
        print(f"✨ Transmutation complete! Parchment created: {output_path}")
        return output_path
    
    def _extract_title(self, notebook: Dict, path: str) -> str:
        """Extract title from notebook or filename"""
        # Try to find title in first markdown cell
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                h1_match = re.search(r'^#\s+(.+)', source, re.MULTILINE)
                if h1_match:
                    return h1_match.group(1).strip()
                break
        
        # Fallback to filename
        return Path(path).stem.replace('_', ' ').replace('-', ' ').title()
    
    def _create_frontmatter(self, title: str, notebook: Dict) -> str:
        """Create the sacred frontmatter"""
        # Extract description from notebook metadata or first few cells
        description = self._extract_description(notebook)
        
        # Clean up YAML special characters to prevent parsing errors
        title = self._clean_yaml_string(title)
        description = self._clean_yaml_string(description)
        
        frontmatter = f"""---
title: "{title}"
description: "{description}"
---

"""
        return frontmatter
    
    def _clean_yaml_string(self, text: str) -> str:
        """Clean text for safe YAML inclusion"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Replace problematic characters
        text = text.replace('"', '\\"')
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Truncate if too long
        if len(text) > 150:
            text = text[:147] + "..."
        return text.strip()
    
    def _extract_description(self, notebook: Dict) -> str:
        """Extract description from notebook"""
        # Try notebook metadata first
        metadata = notebook.get('metadata', {})
        if 'description' in metadata:
            return metadata['description']
        
        # Try first few markdown cells
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                # Skip title lines, get first paragraph
                lines = [line.strip() for line in source.split('\n') if line.strip()]
                for line in lines:
                    if not line.startswith('#') and len(line) > 20:
                        return line
        
        return "Jupyter notebook converted to documentation"
    
    def _transmute_cells(self, cells: List[Dict]) -> str:
        """Transmute all cells into MDX"""
        content = ""
        
        for cell in cells:
            cell_type = cell.get('cell_type')
            
            if cell_type == 'markdown':
                content += self._transmute_markdown_cell(cell)
            elif cell_type == 'code':
                content += self._transmute_code_cell(cell)
            elif cell_type == 'raw':
                content += self._transmute_raw_cell(cell)
                
            content += "\n"
        
        return content
    
    def _transmute_markdown_cell(self, cell: Dict) -> str:
        """Transform markdown cells"""
        source = ''.join(cell.get('source', []))
        
        # Clean up notebook-specific markdown
        source = self._clean_markdown(source)
        
        return source + "\n"
    
    def _transmute_code_cell(self, cell: Dict) -> str:
        """Transform code cells into beautiful code blocks"""
        source = ''.join(cell.get('source', []))
        outputs = cell.get('outputs', [])
        
        content = f"```python\n{source}\n```\n"
        
        # Add outputs if they exist
        if outputs:
            content += self._transmute_outputs(outputs)
            
        return content
    
    def _transmute_raw_cell(self, cell: Dict) -> str:
        """Transform raw cells"""
        source = ''.join(cell.get('source', []))
        return f"```\n{source}\n```\n"
    
    def _transmute_outputs(self, outputs: List[Dict]) -> str:
        """Transform cell outputs"""
        content = ""
        
        for output in outputs:
            output_type = output.get('output_type')
            
            if output_type == 'stream':
                text = ''.join(output.get('text', []))
                content += f"```bash\n{text}\n```\n"
                
            elif output_type in ['execute_result', 'display_data']:
                data = output.get('data', {})
                
                # Handle text output
                if 'text/plain' in data:
                    text = ''.join(data['text/plain'])
                    content += f"```\n{text}\n```\n"
                
                # Handle images
                if 'image/png' in data:
                    content += ":::note Output\nImage output (PNG data) - please save and reference manually\n:::\n"
                
                # Handle HTML
                if 'text/html' in data:
                    html_content = ''.join(data['text/html'])
                    content += f"```html\n{html_content}\n```\n"
            
            elif output_type == 'error':
                error_text = '\n'.join(output.get('traceback', []))
                content += f"```python\n# Error:\n{error_text}\n```\n"
        
        return content
    
    def _clean_markdown(self, markdown: str) -> str:
        """Clean up markdown for Docusaurus MDX compatibility"""
        # Fix unclosed HTML tags that break MDX
        markdown = self._fix_html_tags(markdown)
        
        # Convert notebook-specific syntax
        markdown = re.sub(r'<img src="([^"]+)"([^>]*?)>', r'![Image](\1)', markdown)
        
        # Fix problematic characters in MDX
        markdown = self._fix_mdx_syntax(markdown)
        
        return markdown
    
    def _fix_html_tags(self, content: str) -> str:
        """Fix common HTML tag issues for MDX"""
        # Remove or fix unclosed tags
        content = re.sub(r'<(ul|ol|li|div|span|p)(?![^>]*/>)(?![^>]*</\1>)', '', content)
        
        # Convert self-closing tags to proper format
        content = re.sub(r'<(br|hr|img)([^>]*)(?<!/)>', r'<\1\2 />', content)
        
        # Remove problematic HTML attributes that break MDX
        content = re.sub(r'<([^>]+)\s+style="[^"]*"([^>]*)>', r'<\1\2>', content)
        
        return content
    
    def _fix_mdx_syntax(self, content: str) -> str:
        """Fix MDX-specific syntax issues"""
        # Fix URLs that look like JSX tags
        content = re.sub(r'<(https?://[^>\s]+)>', r'[\1](\1)', content)
        
        # Escape angle brackets that aren't HTML tags
        content = re.sub(r'<(?![a-zA-Z/!])', r'&lt;', content)
        content = re.sub(r'(?<![a-zA-Z])>', r'&gt;', content)
        
        # Fix bare URLs that might confuse MDX
        content = re.sub(r'(?<!\[)(?<!\()https?://[^\s<>"\[\]]+', lambda m: f'[{m.group()}]({m.group()})', content)
        
        return content
    
    def _generate_output_path(self, input_path: str, output_dir: str) -> str:
        """Generate output path for the MDX file"""
        input_name = Path(input_path).stem
        # Convert to URL-friendly filename
        safe_name = re.sub(r'[^a-zA-Z0-9-_]', '-', input_name).lower()
        safe_name = re.sub(r'-+', '-', safe_name).strip('-')
        
        return os.path.join(output_dir, f"{safe_name}.mdx")


def main():
    """The main transmutation ritual"""
    parser = argparse.ArgumentParser(
        description="🎭 Transmute Jupyter notebooks into Docusaurus MDX parchments"
    )
    parser.add_argument('notebook', help='Path to the .ipynb file to transmute')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input)')
    parser.add_argument('-d', '--docs-dir', help='Place in docs directory structure')
    parser.add_argument('--preserve-structure', action='store_true', help='Preserve nested directory structure')
    
    args = parser.parse_args()
    
    # Determine output directory
    output_dir = args.output
    if args.docs_dir:
        output_dir = os.path.join('docs3', 'docs', args.docs_dir)
        os.makedirs(output_dir, exist_ok=True)
    elif output_dir is None:
        output_dir = os.path.dirname(args.notebook)
    
    # Perform the transmutation
    alchemist = JupyterToDocusaurusAlchemist()
    alchemist.transmute_notebook(args.notebook, output_dir)


if __name__ == "__main__":
    main()
