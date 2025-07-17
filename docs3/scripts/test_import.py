#!/usr/bin/env python3
"""
Test script to check if we can import pixeltable and extract some basic info
"""

import sys
from pathlib import Path

# Add the pixeltable package to the Python path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

try:
    import pixeltable as pxt
    print("✅ Successfully imported pixeltable")
    print(f"Version: {pxt.__version__}")
    print(f"Available top-level attributes: {len([x for x in dir(pxt) if not x.startswith('_')])}")
    
    # Test getting functions from a module
    if hasattr(pxt, 'functions'):
        print(f"Functions module available: {hasattr(pxt.functions, '__doc__')}")
        functions_attrs = [x for x in dir(pxt.functions) if not x.startswith('_')]
        print(f"Functions submodules: {len(functions_attrs)}")
        print(f"First few: {functions_attrs[:5]}")
    
    # Test docstring extraction
    print(f"Core module docstring: {bool(pxt.__doc__)}")
    print(f"create_table function available: {hasattr(pxt, 'create_table')}")
    
    if hasattr(pxt, 'create_table'):
        import inspect
        sig = inspect.signature(pxt.create_table)
        doc = inspect.getdoc(pxt.create_table)
        print(f"create_table signature: {sig}")
        print(f"create_table has docstring: {bool(doc)}")
        if doc:
            print(f"Docstring length: {len(doc)} chars")
            print(f"First line: {doc.split('\\n')[0]}")
            
except ImportError as e:
    print(f"❌ Failed to import pixeltable: {e}")
    print(f"Python path: {sys.path[:3]}")
    print(f"Repository root: {repo_root}")
    print(f"Exists: {repo_root.exists()}")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
