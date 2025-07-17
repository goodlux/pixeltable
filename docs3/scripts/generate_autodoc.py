#!/usr/bin/env python3
"""
Pixeltable API Documentation Generator

This script generates MDX documentation files for Docusaurus by extracting
docstrings from all public functions in the Pixeltable codebase.
"""

import ast
import importlib
import inspect
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
import re

# Add the pixeltable package to the Python path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

try:
    import pixeltable as pxt
    print(f"✅ Successfully imported pixeltable version {pxt.__version__}")
except ImportError as e:
    print(f"❌ Failed to import pixeltable: {e}")
    print("Make sure you're running this from the pixeltable repository with dependencies installed.")
    sys.exit(1)


class DocstringExtractor:
    """Extracts and processes docstrings from Python modules."""
    
    def __init__(self):
        self.docs_output_dir = Path(__file__).parent.parent / "docs" / "sdk"
        self.docs_output_dir.mkdir(parents=True, exist_ok=True)
        
    def clean_docstring(self, docstring: str) -> str:
        """Clean and format docstring for MDX."""
        if not docstring:
            return ""
        
        # Remove leading/trailing whitespace
        lines = docstring.strip().split('\n')
        
        # Remove common leading whitespace
        if len(lines) > 1:
            # Find minimum indentation (excluding first line and empty lines)
            min_indent = float('inf')
            for line in lines[1:]:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    min_indent = min(min_indent, indent)
            
            if min_indent != float('inf'):
                lines = [lines[0]] + [line[min_indent:] if line.strip() else line 
                                    for line in lines[1:]]
        
        # Join and clean up
        cleaned = '\n'.join(lines).strip()
        
        # Escape JSX-problematic characters but preserve code blocks
        # Replace standalone { and } but not those in code blocks
        lines = cleaned.split('\n')
        in_code_block = False
        processed_lines = []
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            
            if not in_code_block:
                # Only escape braces outside code blocks
                line = line.replace('{', '\\{').replace('}', '\\}')
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def extract_function_signature(self, func: Any) -> str:
        """Extract function signature."""
        try:
            sig = inspect.signature(func)
            return str(sig)
        except (ValueError, TypeError):
            return "()"
    
    def get_module_functions(self, module: Any) -> List[Tuple[str, Any]]:
        """Get all public functions from a module."""
        functions = []
        
        for name in dir(module):
            if name.startswith('_'):
                continue
                
            try:
                obj = getattr(module, name)
                
                # Include functions, classes, and callable objects that have documentation
                if (inspect.isfunction(obj) or 
                    inspect.isclass(obj) or 
                    (hasattr(obj, '__call__') and hasattr(obj, '__doc__') and obj.__doc__)):
                    functions.append((name, obj))
            except Exception:
                # Skip objects that can't be introspected
                continue
        
        return sorted(functions)
    
    def generate_function_doc(self, name: str, func: Any) -> str:
        """Generate MDX documentation for a single function."""
        docstring = self.clean_docstring(inspect.getdoc(func) or "")
        signature = self.extract_function_signature(func)
        
        # Determine if it's a class or function
        if inspect.isclass(func):
            obj_type = "class"
        elif inspect.isfunction(func):
            obj_type = "def"
        else:
            obj_type = "object"
        
        mdx_content = f"""### {name}

```python
{obj_type} {name}{signature}
```

{docstring}

---

"""
        return mdx_content
    
    def generate_module_doc(self, module_name: str, module: Any, functions: List[Tuple[str, Any]]) -> str:
        """Generate complete MDX documentation for a module."""
        
        # Clean module name for display
        display_name = module_name.replace('pixeltable.', '').replace('_', ' ').title()
        if display_name == 'Pixeltable':
            display_name = 'Core API'
        
        mdx_content = f"""---
title: {display_name}
sidebar_position: 1
---

# {display_name}

"""
        
        # Add module docstring if available
        module_doc = self.clean_docstring(inspect.getdoc(module) or "")
        if module_doc:
            mdx_content += f"{module_doc}\n\n"
        
        if not functions:
            mdx_content += "*No public functions available.*\n"
            return mdx_content
        
        # Group functions by type
        classes = []
        functions_list = []
        other = []
        
        for func_name, func in functions:
            if inspect.isclass(func):
                classes.append((func_name, func))
            elif inspect.isfunction(func):
                functions_list.append((func_name, func))
            else:
                other.append((func_name, func))
        
        # Add classes first
        if classes:
            mdx_content += "## Classes\n\n"
            for func_name, func in classes:
                mdx_content += self.generate_function_doc(func_name, func)
        
        # Then functions
        if functions_list:
            mdx_content += "## Functions\n\n"
            for func_name, func in functions_list:
                mdx_content += self.generate_function_doc(func_name, func)
        
        # Then other objects
        if other:
            mdx_content += "## Other\n\n"
            for func_name, func in other:
                mdx_content += self.generate_function_doc(func_name, func)
        
        return mdx_content
    
    def get_submodules(self) -> Dict[str, Any]:
        """Get all submodules to document."""
        submodules = {}
        
        # Core pixeltable module
        submodules['pixeltable'] = pxt
        
        # Functions submodules  
        if hasattr(pxt, 'functions'):
            submodules['pixeltable.functions'] = pxt.functions
            for attr_name in dir(pxt.functions):
                if not attr_name.startswith('_'):
                    try:
                        attr = getattr(pxt.functions, attr_name)
                        if inspect.ismodule(attr) and hasattr(attr, '__name__'):
                            if attr.__name__.startswith('pixeltable.functions.'):
                                submodules[attr.__name__] = attr
                    except Exception:
                        continue
        
        # IO submodules
        if hasattr(pxt, 'io'):
            submodules['pixeltable.io'] = pxt.io
        
        # Iterators submodules
        if hasattr(pxt, 'iterators'):
            submodules['pixeltable.iterators'] = pxt.iterators
        
        # Ext submodules
        if hasattr(pxt, 'ext'):
            submodules['pixeltable.ext'] = pxt.ext
            
            # Ext functions
            if hasattr(pxt.ext, 'functions'):
                submodules['pixeltable.ext.functions'] = pxt.ext.functions
                for attr_name in dir(pxt.ext.functions):
                    if not attr_name.startswith('_'):
                        try:
                            attr = getattr(pxt.ext.functions, attr_name)
                            if inspect.ismodule(attr) and hasattr(attr, '__name__'):
                                if attr.__name__.startswith('pixeltable.ext.functions.'):
                                    submodules[attr.__name__] = attr
                        except Exception:
                            continue
        
        return submodules
    
    def organize_modules_hierarchically(self, submodules: Dict[str, Any]) -> Dict[str, Dict]:
        """Organize modules into a hierarchical structure for navigation."""
        
        hierarchy = {
            'core': {
                'title': 'Core API',
                'modules': {},
                'position': 1
            },
            'functions': {
                'title': 'Functions',
                'modules': {},
                'position': 2
            },
            'io': {
                'title': 'Input/Output',
                'modules': {},
                'position': 3
            },
            'iterators': {
                'title': 'Iterators',
                'modules': {},
                'position': 4
            },
            'ext': {
                'title': 'Extensions',
                'modules': {},
                'position': 5
            }
        }
        
        for module_name, module in submodules.items():
            if module_name == 'pixeltable':
                hierarchy['core']['modules'][module_name] = module
            elif module_name == 'pixeltable.functions':
                hierarchy['functions']['modules'][module_name] = module
            elif module_name.startswith('pixeltable.functions.'):
                hierarchy['functions']['modules'][module_name] = module
            elif module_name.startswith('pixeltable.io'):
                hierarchy['io']['modules'][module_name] = module
            elif module_name.startswith('pixeltable.iterators'):
                hierarchy['iterators']['modules'][module_name] = module
            elif module_name.startswith('pixeltable.ext'):
                hierarchy['ext']['modules'][module_name] = module
        
        return hierarchy
    
    def generate_category_index(self, category_name: str, category_info: Dict) -> str:
        """Generate an index page for a category."""
        
        mdx_content = f"""---
title: {category_info['title']}
sidebar_position: {category_info['position']}
---

# {category_info['title']}

"""
        
        if category_name == 'core':
            mdx_content += """
The core Pixeltable API provides the fundamental functionality for creating and managing tables, views, and data operations.

## Available Modules

"""
        elif category_name == 'functions':
            mdx_content += """
Pixeltable functions provide built-in functionality for data transformation, AI model integration, and common operations.

## Available Function Modules

"""
        elif category_name == 'io':
            mdx_content += """
Input/Output utilities for importing and exporting data in various formats.

## Available Modules

"""
        elif category_name == 'iterators':
            mdx_content += """
Built-in iterators for data transformation and processing workflows.

## Available Modules

"""
        elif category_name == 'ext':
            mdx_content += """
Extension modules providing additional functionality and integrations.

## Available Modules

"""
        
        # List modules in this category
        for module_name in sorted(category_info['modules'].keys()):
            display_name = module_name.replace('pixeltable.', '').replace('_', ' ').title()
            if display_name == 'Pixeltable':
                display_name = 'Core API'
            link_name = module_name.replace('pixeltable.', '').replace('.', '-').lower()
            if link_name == 'pixeltable':
                link_name = 'core'
            mdx_content += f"- [{display_name}](./{link_name})\n"
        
        return mdx_content
    
    def sanitize_filename(self, name: str) -> str:
        """Convert module name to valid filename."""
        clean_name = name.replace('pixeltable.', '').replace('.', '-').lower()
        if clean_name == 'pixeltable':
            return 'core'
        return clean_name
    
    def generate_sidebar_config(self, hierarchy: Dict[str, Dict]) -> str:
        """Generate sidebar configuration for Docusaurus."""
        
        sidebar_items = []
        
        for category_name, category_info in hierarchy.items():
            if not category_info['modules']:
                continue
                
            category_items = []
            
            # Add category index
            category_items.append(f"'sdk/{category_name}/index'")
            
            # Add modules
            for module_name in sorted(category_info['modules'].keys()):
                filename = self.sanitize_filename(module_name)
                category_items.append(f"'sdk/{category_name}/{filename}'")
            
            category_config = f"""    {{
      type: 'category',
      label: '{category_info['title']}',
      items: [{', '.join(category_items)}],
    }}"""
            
            sidebar_items.append(category_config)
        
        sidebar_config = f"""  sdkSidebar: [
{',\\n'.join(sidebar_items)}
  ],"""
        
        return sidebar_config
    
    def generate_all_docs(self):
        """Generate all documentation files."""
        
        print("🚀 Starting Pixeltable autodoc generation...")
        
        # Get all submodules
        submodules = self.get_submodules()
        print(f"📦 Found {len(submodules)} modules to document")
        
        # Debug: print found modules
        for name in sorted(submodules.keys()):
            functions = self.get_module_functions(submodules[name])
            print(f"  📋 {name}: {len(functions)} functions")
        
        # Organize hierarchically
        hierarchy = self.organize_modules_hierarchically(submodules)
        
        # Generate docs for each category
        for category_name, category_info in hierarchy.items():
            if not category_info['modules']:
                print(f"⏭️  Skipping {category_info['title']} (no modules)")
                continue
                
            print(f"📁 Generating {category_info['title']} documentation...")
            
            # Create category directory
            category_dir = self.docs_output_dir / category_name
            category_dir.mkdir(exist_ok=True)
            
            # Generate category index
            index_content = self.generate_category_index(category_name, category_info)
            (category_dir / "index.mdx").write_text(index_content)
            print(f"  📄 Generated category index")
            
            # Generate module docs
            for module_name, module in category_info['modules'].items():
                print(f"  📄 Documenting {module_name}...")
                
                functions = self.get_module_functions(module)
                doc_content = self.generate_module_doc(module_name, module, functions)
                
                filename = self.sanitize_filename(module_name)
                (category_dir / f"{filename}.mdx").write_text(doc_content)
                
                print(f"    ✅ Generated {len(functions)} function docs")
        
        # Generate main SDK index
        main_index_content = """---
title: SDK Reference
sidebar_position: 1
---

# Pixeltable SDK Reference

Complete reference documentation for all Pixeltable functions, classes, and modules.

## API Categories

- **[Core API](./core)**: Fundamental table operations and data types
- **[Functions](./functions)**: Built-in functions for data transformation and AI integration  
- **[Input/Output](./io)**: Data import and export utilities
- **[Iterators](./iterators)**: Data processing and transformation workflows
- **[Extensions](./ext)**: Additional functionality and third-party integrations

## Quick Navigation

Use the sidebar to navigate through different API categories. Each category contains detailed documentation for all public functions, classes, and methods.

"""
        (self.docs_output_dir / "index.mdx").write_text(main_index_content)
        
        # Generate sidebar configuration
        print("🔧 Generating sidebar configuration...")
        sidebar_config = self.generate_sidebar_config(hierarchy)
        
        # Write sidebar config to a file for manual integration
        sidebar_file = self.docs_output_dir / "sidebar_config.js"
        sidebar_file.write_text(f"""// Add this to your sidebars.js file:

{sidebar_config}
""")
        
        print("✅ Documentation generation complete!")
        print(f"📍 Output location: {self.docs_output_dir}")
        print(f"📝 Sidebar config: {sidebar_file}")
        print()
        print("🔧 Next steps:")
        print("1. Add the SDK sidebar to your sidebars.js file")
        print("2. Update the navbar in docusaurus.config.js to link to /docs/sdk instead of external API reference")


if __name__ == "__main__":
    extractor = DocstringExtractor()
    extractor.generate_all_docs()
