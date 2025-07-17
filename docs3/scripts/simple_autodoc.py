#!/usr/bin/env python3
"""
Simplified Pixeltable API Documentation Generator

Creates basic MDX documentation for the core Pixeltable API based on 
the public interface defined in __init__.py
"""

import re
from pathlib import Path


# Core API functions from pixeltable.__init__.py with their signatures and descriptions
CORE_API_FUNCTIONS = {
    # Table operations
    'create_table': {
        'signature': 'create_table(path: str, schema: Optional[dict[str, Any]] = None, *, source: Optional[TableDataSource] = None, ...)',
        'description': 'Create a new base table with optional data import from various sources.',
        'type': 'function'
    },
    'create_view': {
        'signature': 'create_view(path: str, base: Union[Table, DataFrame], *, additional_columns: Optional[dict[str, Any]] = None, ...)',
        'description': 'Create a view of an existing table object with optional additional columns.',
        'type': 'function'
    },
    'create_snapshot': {
        'signature': 'create_snapshot(path: str, base: Union[Table, DataFrame], *, additional_columns: Optional[dict[str, Any]] = None, ...)',
        'description': 'Create a snapshot of an existing table object.',
        'type': 'function'
    },
    'create_replica': {
        'signature': 'create_replica(destination: str, source: Union[str, Table])',
        'description': 'Create a replica of a table, either remote or local.',
        'type': 'function'
    },
    'get_table': {
        'signature': 'get_table(path: str)',
        'description': 'Get a handle to an existing table, view, or snapshot.',
        'type': 'function'
    },
    'drop_table': {
        'signature': 'drop_table(table: Union[str, Table], force: bool = False, if_not_exists: Literal["error", "ignore"] = "error")',
        'description': 'Drop a table, view, or snapshot.',
        'type': 'function'
    },
    'list_tables': {
        'signature': 'list_tables(dir_path: str = "", recursive: bool = True)',
        'description': 'List the tables in a directory.',
        'type': 'function'
    },
    
    # Directory operations
    'create_dir': {
        'signature': 'create_dir(path: str, if_exists: Literal["error", "ignore", "replace", "replace_force"] = "error", parents: bool = False)',
        'description': 'Create a directory.',
        'type': 'function'
    },
    'drop_dir': {
        'signature': 'drop_dir(path: str, force: bool = False, if_not_exists: Literal["error", "ignore"] = "error")',
        'description': 'Remove a directory.',
        'type': 'function'
    },
    'list_dirs': {
        'signature': 'list_dirs(path: str = "", recursive: bool = True)',
        'description': 'List the directories in a directory.',
        'type': 'function'
    },
    'ls': {
        'signature': 'ls(path: str = "")',
        'description': 'List the contents of a Pixeltable directory.',
        'type': 'function'
    },
    'move': {
        'signature': 'move(path: str, new_path: str)',
        'description': 'Move a schema object to a new directory and/or rename it.',
        'type': 'function'
    },
    
    # System functions
    'init': {
        'signature': 'init(config_overrides: Optional[dict[str, Any]] = None)',
        'description': 'Initialize the Pixeltable environment.',
        'type': 'function'
    },
    'configure_logging': {
        'signature': 'configure_logging(*, to_stdout: Optional[bool] = None, level: Optional[int] = None, add: Optional[str] = None, remove: Optional[str] = None)',
        'description': 'Configure logging settings.',
        'type': 'function'
    },
    'list_functions': {
        'signature': 'list_functions()',
        'description': 'Returns information about all registered functions.',
        'type': 'function'
    },
    
    # UDF and tools
    'udf': {
        'signature': 'udf(*args, **kwargs)',
        'description': 'Decorator to create user-defined functions.',
        'type': 'function'
    },
    'uda': {
        'signature': 'uda(*args, **kwargs)',
        'description': 'Decorator to create user-defined aggregates.',
        'type': 'function'
    },
    'expr_udf': {
        'signature': 'expr_udf(*args, **kwargs)',
        'description': 'Decorator to create expression user-defined functions.',
        'type': 'function'
    },
    'retrieval_udf': {
        'signature': 'retrieval_udf(*args, **kwargs)',
        'description': 'Decorator to create retrieval user-defined functions.',
        'type': 'function'
    },
    'mcp_udfs': {
        'signature': 'mcp_udfs(*args, **kwargs)',
        'description': 'Create UDFs from MCP server functions.',
        'type': 'function'
    },
    'query': {
        'signature': 'query(*args, **kwargs)',
        'description': 'Execute a query expression.',
        'type': 'function'
    },
    'tools': {
        'signature': 'tools(*args: Union[Function, Tool])',
        'description': 'Specify a collection of UDFs to be used as LLM tools.',
        'type': 'function'
    },
    'tool': {
        'signature': 'tool(fn: Function, name: Optional[str] = None, description: Optional[str] = None)',
        'description': 'Specify a Pixeltable UDF to be used as an LLM tool with customizable metadata.',
        'type': 'function'
    },
    'array': {
        'signature': 'array(elements: Iterable)',
        'description': 'Create an array expression from elements.',
        'type': 'function'
    },
    
    # Core classes
    'Table': {
        'signature': 'class Table',
        'description': 'Represents a Pixeltable table, view, or snapshot.',
        'type': 'class'
    },
    'Column': {
        'signature': 'class Column',
        'description': 'Represents a column in a Pixeltable table.',
        'type': 'class'
    },
    'DataFrame': {
        'signature': 'class DataFrame',
        'description': 'Represents a query result set with pandas-like operations.',
        'type': 'class'
    },
    'View': {
        'signature': 'class View',
        'description': 'Represents a view in Pixeltable.',
        'type': 'class'
    },
    'InsertableTable': {
        'signature': 'class InsertableTable',
        'description': 'Base class for tables that support insertion.',
        'type': 'class'
    },
    'UpdateStatus': {
        'signature': 'class UpdateStatus',
        'description': 'Status information for table updates.',
        'type': 'class'
    },
    'Function': {
        'signature': 'class Function',
        'description': 'Base class for Pixeltable functions.',
        'type': 'class'
    },
    'Aggregator': {
        'signature': 'class Aggregator',
        'description': 'Base class for aggregation functions.',
        'type': 'class'
    },
    
    # Type system
    'Array': {
        'signature': 'class Array',
        'description': 'Array data type.',
        'type': 'class'
    },
    'Audio': {
        'signature': 'class Audio',
        'description': 'Audio data type.',
        'type': 'class'
    },
    'Bool': {
        'signature': 'class Bool',
        'description': 'Boolean data type.',
        'type': 'class'
    },
    'Date': {
        'signature': 'class Date',
        'description': 'Date data type.',
        'type': 'class'
    },
    'Document': {
        'signature': 'class Document',
        'description': 'Document data type.',
        'type': 'class'
    },
    'Float': {
        'signature': 'class Float',
        'description': 'Float data type.',
        'type': 'class'
    },
    'Image': {
        'signature': 'class Image',
        'description': 'Image data type.',
        'type': 'class'
    },
    'Int': {
        'signature': 'class Int',
        'description': 'Integer data type.',
        'type': 'class'
    },
    'Json': {
        'signature': 'class Json',
        'description': 'JSON data type.',
        'type': 'class'
    },
    'Required': {
        'signature': 'class Required',
        'description': 'Marks a field as required (non-nullable).',
        'type': 'class'
    },
    'String': {
        'signature': 'class String',
        'description': 'String data type.',
        'type': 'class'
    },
    'Timestamp': {
        'signature': 'class Timestamp',
        'description': 'Timestamp data type.',
        'type': 'class'
    },
    'Video': {
        'signature': 'class Video',
        'description': 'Video data type.',
        'type': 'class'
    },
    
    # Exceptions
    'Error': {
        'signature': 'class Error',
        'description': 'Base exception class for Pixeltable errors.',
        'type': 'class'
    },
    'ExprEvalError': {
        'signature': 'class ExprEvalError',
        'description': 'Exception raised during expression evaluation.',
        'type': 'class'
    },
    'PixeltableWarning': {
        'signature': 'class PixeltableWarning',
        'description': 'Warning class for Pixeltable warnings.',
        'type': 'class'
    },
}

# Function modules (simplified list)
FUNCTION_MODULES = {
    'anthropic': 'Integration with Anthropic Claude models',
    'audio': 'Audio processing functions',
    'bedrock': 'AWS Bedrock integration',
    'date': 'Date and time functions',
    'deepseek': 'DeepSeek model integration',
    'fireworks': 'Fireworks AI integration',
    'gemini': 'Google Gemini integration',
    'groq': 'Groq integration',
    'huggingface': 'Hugging Face model integration',
    'image': 'Image processing functions',
    'json': 'JSON manipulation functions',
    'llama_cpp': 'Llama.cpp integration',
    'math': 'Mathematical functions',
    'mistralai': 'Mistral AI integration',
    'ollama': 'Ollama integration',
    'openai': 'OpenAI integration',
    'replicate': 'Replicate integration',
    'string': 'String manipulation functions',
    'timestamp': 'Timestamp functions',
    'together': 'Together AI integration',
    'video': 'Video processing functions',
    'vision': 'Computer vision functions',
    'whisper': 'Whisper speech recognition functions'
}

EXT_FUNCTION_MODULES = {
    'whisperx': 'WhisperX advanced speech recognition',
    'yolox': 'YOLOX object detection'
}


def generate_function_doc(name: str, info: dict) -> str:
    """Generate MDX documentation for a single function."""
    obj_type = info['type']
    signature = info['signature']
    description = info['description']
    
    mdx_content = f"""### {name}

```python
{signature}
```

{description}

---

"""
    return mdx_content


def generate_core_api_doc() -> str:
    """Generate the core API documentation."""
    
    mdx_content = """---
title: Core API
sidebar_position: 1
---

# Core API

The main Pixeltable module provides the fundamental functionality for creating and managing tables, views, data types, and operations.

"""
    
    # Group functions by category
    categories = {
        'Table Operations': ['create_table', 'create_view', 'create_snapshot', 'create_replica', 'get_table', 'drop_table', 'list_tables'],
        'Directory Operations': ['create_dir', 'drop_dir', 'list_dirs', 'ls', 'move'],
        'System Functions': ['init', 'configure_logging', 'list_functions'],
        'User-Defined Functions': ['udf', 'uda', 'expr_udf', 'retrieval_udf', 'mcp_udfs', 'query', 'tools', 'tool', 'array'],
        'Core Classes': ['Table', 'Column', 'DataFrame', 'View', 'InsertableTable', 'UpdateStatus', 'Function', 'Aggregator'],
        'Data Types': ['Array', 'Audio', 'Bool', 'Date', 'Document', 'Float', 'Image', 'Int', 'Json', 'Required', 'String', 'Timestamp', 'Video'],
        'Exceptions': ['Error', 'ExprEvalError', 'PixeltableWarning']
    }
    
    for category, functions in categories.items():
        mdx_content += f"## {category}\n\n"
        for func_name in functions:
            if func_name in CORE_API_FUNCTIONS:
                mdx_content += generate_function_doc(func_name, CORE_API_FUNCTIONS[func_name])
    
    return mdx_content


def generate_functions_overview() -> str:
    """Generate the functions overview documentation."""
    
    mdx_content = """---
title: Functions
sidebar_position: 1
---

# Functions

Pixeltable functions provide built-in functionality for data transformation, AI model integration, and common operations.

## Available Function Modules

"""
    
    for module_name, description in FUNCTION_MODULES.items():
        mdx_content += f"- **[{module_name.replace('_', ' ').title()}](./{module_name})**: {description}\n"
    
    return mdx_content


def generate_function_module_doc(module_name: str, description: str) -> str:
    """Generate documentation for a function module."""
    
    display_name = module_name.replace('_', ' ').title()
    
    mdx_content = f"""---
title: {display_name}
sidebar_position: 1
---

# {display_name}

{description}

*Documentation for specific functions in this module will be automatically generated from the codebase.*

## Usage

```python
import pixeltable as pxt

# Access functions from this module
pxt.functions.{module_name}.<function_name>()
```

"""
    return mdx_content


def generate_io_doc() -> str:
    """Generate I/O documentation."""
    
    mdx_content = """---
title: Input/Output
sidebar_position: 1
---

# Input/Output

Input/Output utilities for importing and exporting data in various formats.

*Documentation for I/O functions will be automatically generated from the codebase.*

## Usage

```python
import pixeltable as pxt

# Access I/O functions
pxt.io.<function_name>()
```

"""
    return mdx_content


def generate_iterators_doc() -> str:
    """Generate iterators documentation."""
    
    mdx_content = """---
title: Iterators
sidebar_position: 1
---

# Iterators

Built-in iterators for data transformation and processing workflows.

*Documentation for iterator functions will be automatically generated from the codebase.*

## Usage

```python
import pixeltable as pxt

# Access iterator functions
pxt.iterators.<function_name>()
```

"""
    return mdx_content


def generate_ext_doc() -> str:
    """Generate extensions documentation."""
    
    mdx_content = """---
title: Extensions
sidebar_position: 1
---

# Extensions

Extension modules providing additional functionality and integrations.

## Available Modules

"""
    
    for module_name, description in EXT_FUNCTION_MODULES.items():
        mdx_content += f"- **[{module_name.replace('_', ' ').title()}](./ext-functions-{module_name})**: {description}\n"
    
    return mdx_content


def generate_ext_function_module_doc(module_name: str, description: str) -> str:
    """Generate documentation for an extension function module."""
    
    display_name = module_name.replace('_', ' ').title()
    
    mdx_content = f"""---
title: {display_name}
sidebar_position: 1
---

# {display_name}

{description}

*Documentation for specific functions in this module will be automatically generated from the codebase.*

## Usage

```python
import pixeltable as pxt

# Access extension functions
pxt.ext.functions.{module_name}.<function_name>()
```

"""
    return mdx_content


def main():
    """Generate all SDK documentation."""
    
    print("🚀 Starting simplified Pixeltable autodoc generation...")
    
    # Set up paths
    docs_root = Path(__file__).parent.parent / "docs" / "sdk"
    
    # Create main core API doc
    core_content = generate_core_api_doc()
    (docs_root / "core" / "core.mdx").write_text(core_content)
    print("✅ Generated core API documentation")
    
    # Create functions overview
    functions_content = generate_functions_overview()
    (docs_root / "functions" / "index.mdx").write_text(functions_content)
    print("✅ Generated functions overview")
    
    # Create individual function module docs
    for module_name, description in FUNCTION_MODULES.items():
        module_content = generate_function_module_doc(module_name, description)
        filename = f"functions-{module_name}.mdx"
        (docs_root / "functions" / filename).write_text(module_content)
    print(f"✅ Generated {len(FUNCTION_MODULES)} function module docs")
    
    # Create I/O docs
    io_content = generate_io_doc()
    (docs_root / "io" / "io.mdx").write_text(io_content)
    print("✅ Generated I/O documentation")
    
    # Create iterators docs
    iterators_content = generate_iterators_doc()
    (docs_root / "iterators" / "iterators.mdx").write_text(iterators_content)
    print("✅ Generated iterators documentation")
    
    # Create extension docs
    ext_content = generate_ext_doc()
    (docs_root / "ext" / "ext.mdx").write_text(ext_content)
    
    # Create extension function module docs
    for module_name, description in EXT_FUNCTION_MODULES.items():
        module_content = generate_ext_function_module_doc(module_name, description)
        filename = f"ext-functions-{module_name}.mdx"
        (docs_root / "ext" / filename).write_text(module_content)
    print(f"✅ Generated {len(EXT_FUNCTION_MODULES)} extension module docs")
    
    # Create category index files
    category_indexes = {
        ('core', 'Core API'): 'The core Pixeltable API provides the fundamental functionality for creating and managing tables, views, and data operations.',
        ('functions', 'Functions'): 'Pixeltable functions provide built-in functionality for data transformation, AI model integration, and common operations.',
        ('io', 'Input/Output'): 'Input/Output utilities for importing and exporting data in various formats.',
        ('iterators', 'Iterators'): 'Built-in iterators for data transformation and processing workflows.',
        ('ext', 'Extensions'): 'Extension modules providing additional functionality and integrations.'
    }
    
    for (category_name, title), description in category_indexes.items():
        index_content = f"""---
title: {title}
sidebar_position: 1
---

# {title}

{description}

## Available Modules

- [Core](./core): Main pixeltable functions and classes

""" if category_name == 'core' else f"""---
title: {title}
sidebar_position: 1
---

# {title}

{description}

*See the individual module pages for detailed documentation.*

"""
        (docs_root / category_name / "index.mdx").write_text(index_content)
    
    print("✅ Generated category index files")
    print(f"📍 Output location: {docs_root}")
    print()
    print("🎉 Simplified SDK documentation generation complete!")
    print("   The documentation provides a solid foundation with the core API fully documented.")
    print("   Function modules are stubbed out and ready for full autodoc integration.")


if __name__ == "__main__":
    main()
