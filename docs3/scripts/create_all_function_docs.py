#!/usr/bin/env python3
"""
Create all remaining function module documentation files
"""

from pathlib import Path

# Remaining modules to create
modules = [
    ('date', 'Date and time manipulation functions'),
    ('deepseek', 'DeepSeek model integration for code and text generation'),
    ('fireworks', 'Fireworks AI integration for fast model inference'),
    ('gemini', 'Google Gemini integration for multimodal AI tasks'),
    ('groq', 'Groq integration for ultra-fast LLM inference'),
    ('huggingface', 'Hugging Face model integration for open-source models'),
    ('json', 'JSON manipulation and processing functions'),
    ('llama-cpp', 'Llama.cpp integration for local model inference'),
    ('math', 'Mathematical functions and operations'),
    ('mistralai', 'Mistral AI integration for efficient language models'),
    ('ollama', 'Ollama integration for local model management'),
    ('replicate', 'Replicate integration for cloud-based model inference'),
    ('string', 'String manipulation and text processing functions'),
    ('timestamp', 'Timestamp and time-based operations'),
    ('together', 'Together AI integration for collaborative model inference'),
    ('video', 'Video processing functions for analysis and transformation'),
    ('vision', 'Computer vision functions for image analysis'),
    ('whisper', 'Whisper speech recognition and audio transcription')
]

def create_module_docs():
    docs_dir = Path('/Users/rob/repos/pixeltable/docs3/docs/sdk/functions')
    
    for module_file, description in modules:
        # Convert file name to display name and code name
        if module_file == 'llama-cpp':
            display_name = 'Llama.cpp'
            code_name = 'llama_cpp'
        elif module_file == 'mistralai':
            display_name = 'Mistral AI'
            code_name = 'mistralai'
        elif module_file == 'huggingface':
            display_name = 'Hugging Face'
            code_name = 'huggingface'
        else:
            display_name = module_file.replace('-', ' ').title()
            code_name = module_file.replace('-', '_')
        
        content = f"""---
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
pxt.functions.{code_name}.<function_name>(...)
```
"""
        
        filename = f'functions-{module_file}.mdx'
        file_path = docs_dir / filename
        
        file_path.write_text(content)
        print(f"Created {filename}")

if __name__ == "__main__":
    create_module_docs()
    print("✅ All function module docs created!")
