#!/bin/bash
# Enhanced Mass Notebook Transmogrification for Pixeltable
# Processes entire nested notebook directory structure

set -e

# Configuration
NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="docs3/docs/examples"
SCRIPT_DIR="docs3/scripts"

echo "🧙‍♂️ MASS TRANSMOGRIFICATION COMMENCING..."
echo "📂 Source: $NOTEBOOK_SOURCE"
echo "📂 Output: $DOCS_OUTPUT"
echo ""

# Create output directory structure
mkdir -p "$DOCS_OUTPUT"

# Function to process a single notebook
process_notebook() {
    local notebook_path="$1"
    local output_subdir="$2"
    
    # Create output subdirectory
    mkdir -p "$DOCS_OUTPUT/$output_subdir"
    
    echo "  🔄 Processing: $(basename "$notebook_path")"
    
    # Run transmutation
    python3 "$SCRIPT_DIR/jupyter_to_docusaurus.py" \
        "$notebook_path" \
        -o "$DOCS_OUTPUT/$output_subdir"
        
    if [ $? -eq 0 ]; then
        echo "  ✅ Transmuted: $output_subdir/$(basename "$notebook_path" .ipynb).mdx"
    else
        echo "  ❌ Failed: $notebook_path"
    fi
}

# Process root level notebooks
echo "📝 Processing root level notebooks..."
for notebook in "$NOTEBOOK_SOURCE"/*.ipynb; do
    if [ -f "$notebook" ]; then
        process_notebook "$notebook" "."
    fi
done

# Process nested directories
echo ""
echo "📁 Processing nested directories..."

# Fundamentals
if [ -d "$NOTEBOOK_SOURCE/fundamentals" ]; then
    echo "📚 Processing fundamentals..."
    for notebook in "$NOTEBOOK_SOURCE/fundamentals"/*.ipynb; do
        if [ -f "$notebook" ]; then
            process_notebook "$notebook" "fundamentals"
        fi
    done
fi

# Feature Guides  
if [ -d "$NOTEBOOK_SOURCE/feature-guides" ]; then
    echo "🔧 Processing feature guides..."
    for notebook in "$NOTEBOOK_SOURCE/feature-guides"/*.ipynb; do
        if [ -f "$notebook" ]; then
            process_notebook "$notebook" "feature-guides"
        fi
    done
fi

# Use Cases
if [ -d "$NOTEBOOK_SOURCE/use-cases" ]; then
    echo "💡 Processing use cases..."
    for notebook in "$NOTEBOOK_SOURCE/use-cases"/*.ipynb; do
        if [ -f "$notebook" ]; then
            process_notebook "$notebook" "use-cases"
        fi
    done
fi

# Integrations (the big one!)
if [ -d "$NOTEBOOK_SOURCE/integrations" ]; then
    echo "🔌 Processing integrations..."
    for notebook in "$NOTEBOOK_SOURCE/integrations"/*.ipynb; do
        if [ -f "$notebook" ]; then
            process_notebook "$notebook" "integrations"
        fi
    done
fi

echo ""
echo "📊 TRANSMOGRIFICATION COMPLETE!"
echo ""

# Generate index files for each category
echo "📋 Generating category index files..."

# Main examples index
cat > "$DOCS_OUTPUT/index.mdx" << 'EOF'
---
title: "Examples"
description: "Interactive examples and tutorials for Pixeltable"
---

# Pixeltable Examples

Comprehensive collection of interactive notebooks showcasing Pixeltable's capabilities.

## 🚀 Getting Started

Start with the basics and build up to advanced multimodal AI workflows.

- [Pixeltable Basics](./pixeltable-basics) - Core concepts and first steps

## 📚 Fundamentals

Master the core concepts of Pixeltable:

- [Tables and Data Operations](./fundamentals/tables-and-data-operations)
- [Computed Columns](./fundamentals/computed-columns) 
- [Queries and Expressions](./fundamentals/queries-and-expressions)

## 🔧 Feature Guides

Deep dives into specific Pixeltable features:

- [User-Defined Functions](./feature-guides/udfs-in-pixeltable)
- [Embedding Indexes](./feature-guides/embedding-indexes)
- [Working with External Files](./feature-guides/working-with-external-files)
- [Time Zones](./feature-guides/time-zones)

## 💡 Use Cases

Real-world applications and complete workflows:

- [RAG Demo](./use-cases/rag-demo) - Retrieval-Augmented Generation
- [RAG Operations](./use-cases/rag-operations) - Advanced RAG patterns
- [Object Detection in Videos](./use-cases/object-detection-in-videos)
- [Audio Transcriptions](./use-cases/audio-transcriptions)

## 🔌 Integrations

Connect Pixeltable with popular AI platforms:

### Language Models
- [OpenAI](./integrations/working-with-openai)
- [Anthropic](./integrations/working-with-anthropic) 
- [Google Gemini](./integrations/working-with-gemini)
- [Mistral AI](./integrations/working-with-mistralai)
- [AWS Bedrock](./integrations/working-with-bedrock)

### Local & Open Source
- [Ollama](./integrations/working-with-ollama)
- [Llama.cpp](./integrations/working-with-llama-cpp)
- [Hugging Face](./integrations/working-with-hugging-face)

### Cloud Platforms
- [Fireworks](./integrations/working-with-fireworks)
- [Together AI](./integrations/working-with-together)
- [Groq](./integrations/working-with-groq)
- [Replicate](./integrations/working-with-replicate)
- [DeepSeek](./integrations/working-with-deepseek)

### Tools & Platforms
- [Label Studio](./integrations/using-label-studio-with-pixeltable)
- [FiftyOne](./integrations/working-with-fiftyone)

## 🎯 Quick Links

**New to Pixeltable?** Start with [Pixeltable Basics](./pixeltable-basics)

**Building RAG systems?** Check out the [RAG Demo](./use-cases/rag-demo)

**Working with media?** See [Object Detection in Videos](./use-cases/object-detection-in-videos)

**Need AI integrations?** Browse our [integration guides](./integrations/)

---

*All examples include executable code and detailed explanations. Most can be run locally or in cloud environments like Google Colab.*
EOF

# Integrations index
mkdir -p "$DOCS_OUTPUT/integrations"
cat > "$DOCS_OUTPUT/integrations/index.mdx" << 'EOF'
---
title: "AI Platform Integrations"
description: "Connect Pixeltable with popular AI platforms and services"
---

# AI Platform Integrations

Pixeltable works seamlessly with major AI platforms. These guides show you how to integrate with each service.

## Language Model Providers

### Major Platforms
- [OpenAI](./working-with-openai) - GPT models and vision APIs
- [Anthropic](./working-with-anthropic) - Claude models and vision
- [Google Gemini](./working-with-gemini) - Gemini Pro and Ultra
- [AWS Bedrock](./working-with-bedrock) - Amazon's AI platform

### Specialized Providers  
- [Mistral AI](./working-with-mistralai) - European AI leader
- [Fireworks](./working-with-fireworks) - Fast inference platform
- [Together AI](./working-with-together) - Open source models
- [Groq](./working-with-groq) - Ultra-fast inference
- [Replicate](./working-with-replicate) - Cloud model hosting
- [DeepSeek](./working-with-deepseek) - Advanced reasoning models

## Local & Open Source

- [Ollama](./working-with-ollama) - Local LLM deployment
- [Llama.cpp](./working-with-llama-cpp) - Efficient local inference  
- [Hugging Face](./working-with-hugging-face) - Open source model hub

## Tools & Platforms

- [Label Studio](./using-label-studio-with-pixeltable) - Data labeling platform
- [FiftyOne](./working-with-fiftyone) - Computer vision datasets

## Getting Started

1. **Choose your platform** from the list above
2. **Follow the integration guide** for setup instructions
3. **Run the example notebook** to see it in action
4. **Adapt the patterns** for your specific use case

Each integration guide includes:
- ✅ Setup and authentication
- ✅ Basic usage examples  
- ✅ Advanced patterns and best practices
- ✅ Troubleshooting tips
EOF

echo "✅ Generated category index files"
echo ""

# Count results
total_notebooks=$(find "$DOCS_OUTPUT" -name "*.mdx" -not -name "index.mdx" | wc -l)
echo "📈 RESULTS:"
echo "   📝 Transmuted: $total_notebooks notebooks"
echo "   📁 Categories: fundamentals, feature-guides, use-cases, integrations"
echo "   🎯 Ready for: Docusaurus integration"
echo ""
echo "🚀 Next steps:"
echo "   1. Review generated markdown files in $DOCS_OUTPUT"  
echo "   2. Add examples section to your Docusaurus sidebar"
echo "   3. Test notebook rendering and links"
echo "   4. Add Binder/Colab badges to key examples"
echo ""
echo "🎉 Your 'LAME ASS mintlify' notebooks are now AWESOME Docusaurus examples!"
