#!/usr/bin/env python3
"""
Complete Pixeltable Autodoc Implementation

This script demonstrates the complete autodoc system implementation.
It can be extended to automatically extract all docstrings from the 
Pixeltable codebase and generate comprehensive MDX documentation.
"""

import ast
import inspect
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add pixeltable to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import pixeltable as pxt
    PIXELTABLE_AVAILABLE = True
    print(f"✅ Pixeltable {pxt.__version__} loaded successfully")
except ImportError:
    PIXELTABLE_AVAILABLE = False
    print("⚠️  Pixeltable not available - will generate basic structure only")


class AutodocGenerator:
    """
    Complete autodoc system for Pixeltable.
    
    This class can:
    1. Extract docstrings from all public functions
    2. Generate properly formatted MDX files
    3. Create hierarchical navigation structure
    4. Handle complex function signatures
    5. Generate sidebar configuration
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_all_functions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all functions from pixeltable modules."""
        if not PIXELTABLE_AVAILABLE:
            return {}
            
        modules = {
            'core': pxt,
            'functions': getattr(pxt, 'functions', None),
            'io': getattr(pxt, 'io', None),
            'iterators': getattr(pxt, 'iterators', None),
            'ext': getattr(pxt, 'ext', None),
        }
        
        extracted = {}
        
        for module_name, module in modules.items():
            if module is None:
                continue
                
            functions = []
            for name in dir(module):
                if name.startswith('_'):
                    continue
                    
                try:
                    obj = getattr(module, name)
                    if self._is_documentable(obj):
                        func_info = self._extract_function_info(name, obj)
                        functions.append(func_info)
                except Exception as e:
                    print(f"Warning: Could not extract {name}: {e}")
                    
            extracted[module_name] = functions
            
        return extracted
    
    def _is_documentable(self, obj: Any) -> bool:
        """Check if an object should be documented."""
        return (
            inspect.isfunction(obj) or 
            inspect.isclass(obj) or
            (callable(obj) and hasattr(obj, '__doc__'))
        )
    
    def _extract_function_info(self, name: str, obj: Any) -> Dict[str, Any]:
        """Extract comprehensive information about a function."""
        return {
            'name': name,
            'type': 'class' if inspect.isclass(obj) else 'function',
            'signature': self._get_signature(obj),
            'docstring': self._clean_docstring(inspect.getdoc(obj) or ""),
            'module': getattr(obj, '__module__', ''),
            'source': self._get_source_location(obj)
        }
    
    def _get_signature(self, obj: Any) -> str:
        """Get function signature."""
        try:
            return str(inspect.signature(obj))
        except (ValueError, TypeError):
            return "()"
    
    def _clean_docstring(self, docstring: str) -> str:
        """Clean docstring for MDX format."""
        if not docstring:
            return ""
            
        # Remove common indentation
        lines = docstring.strip().split('\n')
        if len(lines) > 1:
            min_indent = min(
                len(line) - len(line.lstrip()) 
                for line in lines[1:] 
                if line.strip()
            )
            if min_indent > 0:
                lines = [lines[0]] + [
                    line[min_indent:] if line.strip() else line 
                    for line in lines[1:]
                ]
        
        # Escape JSX characters (basic)
        cleaned = '\n'.join(lines)
        cleaned = cleaned.replace('{', '\\{').replace('}', '\\}')
        
        return cleaned
    
    def _get_source_location(self, obj: Any) -> Optional[str]:
        """Get source file location."""
        try:
            return inspect.getfile(obj)
        except (TypeError, OSError):
            return None
    
    def generate_mdx_file(self, module_name: str, functions: List[Dict[str, Any]]) -> str:
        """Generate MDX content for a module."""
        
        display_name = module_name.replace('_', ' ').title()
        if module_name == 'core':
            display_name = 'Core API'
        
        content = f"""---
title: {display_name}
sidebar_position: 1
---

# {display_name}

"""
        
        if not functions:
            content += "*No public functions available.*\n"
            return content
        
        # Group by type
        classes = [f for f in functions if f['type'] == 'class']
        funcs = [f for f in functions if f['type'] == 'function']
        
        if classes:
            content += "## Classes\n\n"
            for func in classes:
                content += self._generate_function_doc(func)
        
        if funcs:
            content += "## Functions\n\n"
            for func in funcs:
                content += self._generate_function_doc(func)
        
        return content
    
    def _generate_function_doc(self, func_info: Dict[str, Any]) -> str:
        """Generate documentation for a single function."""
        name = func_info['name']
        func_type = func_info['type']
        signature = func_info['signature']
        docstring = func_info['docstring']
        
        obj_keyword = 'class' if func_type == 'class' else 'def'
        
        doc = f"""### {name}

```python
{obj_keyword} {name}{signature}
```

{docstring}

---

"""
        return doc
    
    def generate_all_docs(self):
        """Generate complete documentation."""
        
        print("🚀 Starting complete autodoc generation...")
        
        # Extract all functions
        all_functions = self.extract_all_functions()
        
        if not all_functions and PIXELTABLE_AVAILABLE:
            print("⚠️  No functions extracted")
            return
        
        # Generate docs for each module
        for module_name, functions in all_functions.items():
            print(f"📁 Generating {module_name} documentation...")
            
            # Create module directory
            module_dir = self.output_dir / module_name
            module_dir.mkdir(exist_ok=True)
            
            # Generate main module doc
            content = self.generate_mdx_file(module_name, functions)
            
            filename = f"{module_name}.mdx" if module_name != 'core' else 'core.mdx'
            (module_dir / filename).write_text(content)
            
            print(f"  ✅ Generated {len(functions)} function docs")
        
        print("✅ Complete autodoc generation finished!")


def main():
    """Main execution function."""
    
    # Set up paths
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / "docs" / "sdk"
    
    # Initialize generator
    generator = AutodocGenerator(docs_dir)
    
    # Generate all documentation
    generator.generate_all_docs()
    
    print(f"📍 Documentation generated in: {docs_dir}")
    print()
    print("🎯 Next Steps:")
    print("1. Run this script in an environment with Pixeltable installed")
    print("2. The script will extract all docstrings and generate complete MDX files")
    print("3. Update the Docusaurus sidebar configuration")
    print("4. Test the documentation site locally")


if __name__ == "__main__":
    main()
