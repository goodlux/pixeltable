#!/bin/bash
# Simple notebook conversion using nbconvert

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="docs3/docs/examples"

echo "🚀 Simple Notebook Conversion Pipeline"
echo "📂 Source: $NOTEBOOK_SOURCE"
echo "📂 Output: $DOCS_OUTPUT"
echo ""

# Create output directory
mkdir -p "$DOCS_OUTPUT"

# Function to convert single notebook
convert_notebook() {
    local notebook_path="$1"
    local output_subdir="$2"
    local notebook_name=$(basename "$notebook_path" .ipynb)
    
    echo "  🔄 Converting: $notebook_name"
    
    # Create output subdirectory
    mkdir -p "$DOCS_OUTPUT/$output_subdir"
    
    # Use nbconvert for clean conversion
    jupyter nbconvert \
        --to markdown \
        --no-input \
        --output-dir="$DOCS_OUTPUT/$output_subdir" \
        "$notebook_path" || {
            echo "  ❌ nbconvert failed for $notebook_name"
            return 1
        }
    
    echo "  ✅ Converted: $notebook_name.md"
}

# Convert notebooks by category
echo "📝 Converting notebooks..."

# Root level
for notebook in "$NOTEBOOK_SOURCE"/*.ipynb; do
    if [ -f "$notebook" ]; then
        convert_notebook "$notebook" "."
    fi
done

# Fundamentals
if [ -d "$NOTEBOOK_SOURCE/fundamentals" ]; then
    echo "📚 Converting fundamentals..."
    for notebook in "$NOTEBOOK_SOURCE/fundamentals"/*.ipynb; do
        if [ -f "$notebook" ]; then
            convert_notebook "$notebook" "fundamentals"
        fi
    done
fi

# Feature Guides
if [ -d "$NOTEBOOK_SOURCE/feature-guides" ]; then
    echo "🔧 Converting feature guides..."
    for notebook in "$NOTEBOOK_SOURCE/feature-guides"/*.ipynb; do
        if [ -f "$notebook" ]; then
            convert_notebook "$notebook" "feature-guides"
        fi
    done
fi

# Use Cases
if [ -d "$NOTEBOOK_SOURCE/use-cases" ]; then
    echo "💡 Converting use cases..."
    for notebook in "$NOTEBOOK_SOURCE/use-cases"/*.ipynb; do
        if [ -f "$notebook" ]; then
            convert_notebook "$notebook" "use-cases"
        fi
    done
fi

# Integrations
if [ -d "$NOTEBOOK_SOURCE/integrations" ]; then
    echo "🔌 Converting integrations..."
    for notebook in "$NOTEBOOK_SOURCE/integrations"/*.ipynb; do
        if [ -f "$notebook" ]; then
            convert_notebook "$notebook" "integrations"
        fi
    done
fi

echo ""
echo "📊 CONVERSION COMPLETE!"
echo "🔄 Now run: python3 docs3/scripts/add_frontmatter.py"
echo "   This will convert .md files to .mdx with proper frontmatter"
