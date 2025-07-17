#!/usr/bin/env python3
"""
Generate remaining function module docs
"""

from pathlib import Path

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
    'json': 'JSON manipulation functions',
    'llama_cpp': 'Llama.cpp integration',
    'math': 'Mathematical functions',
    'mistralai': 'Mistral AI integration',
    'ollama': 'Ollama integration',
    'replicate': 'Replicate integration',
    'string': 'String manipulation functions',
    'timestamp': 'Timestamp functions',
    'together': 'Together AI integration',
    'video': 'Video processing functions',
    'vision': 'Computer vision functions',
    'whisper': 'Whisper speech recognition functions'
}

def generate_function_module_doc(module_name: str, description: str) -> str:
    """Generate documentation for a function module."""
    
    display_name = module_name.replace('_', ' ').title()
    
    # Special cases for display names
    if module_name == 'llama_cpp':
        display_name = 'Llama.cpp'
    elif module_name == 'mistralai':
        display_name = 'Mistral AI'
    elif module_name == 'openai':
        display_name = 'OpenAI'
    elif module_name == 'huggingface':
        display_name = 'Hugging Face'
    
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
pxt.functions.{module_name}.<function_name>(...)
```

"""
    return mdx_content

def main():
    docs_root = Path(__file__).parent.parent / "docs" / "sdk" / "functions"
    
    # Generate docs for modules that don't exist yet
    existing_files = set(f.name for f in docs_root.glob("*.mdx"))
    
    for module_name, description in FUNCTION_MODULES.items():
        filename = f"functions-{module_name}.mdx"
        if filename not in existing_files:
            content = generate_function_module_doc(module_name, description)
            (docs_root / filename).write_text(content)
            print(f"Generated {filename}")

if __name__ == "__main__":
    main()
