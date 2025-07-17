#!/bin/bash
# Quarto-based notebook conversion for Pixeltable docs

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="docs3/docs/examples"

echo "🔮 Quarto Notebook Conversion for Pixeltable"
echo "📂 Source: $NOTEBOOK_SOURCE"
echo "📂 Output: $DOCS_OUTPUT"
echo ""

# Check if Quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "❌ Quarto not found. Install with:"
    echo "   pip install quarto-cli"
    echo "   or visit: https://quarto.org/docs/get-started/"
    exit 1
fi

echo "✅ Quarto found: $(quarto --version)"
echo ""

# Create output directory structure
mkdir -p "$DOCS_OUTPUT"
mkdir -p "$DOCS_OUTPUT/fundamentals"
mkdir -p "$DOCS_OUTPUT/integrations" 
mkdir -p "$DOCS_OUTPUT/use-cases"

# Function to convert single notebook
convert_notebook() {
    local notebook_path="$1"
    local output_dir="$2"
    local notebook_name=$(basename "$notebook_path" .ipynb)
    
    echo "  🔄 Converting: $notebook_name"
    
    # Use Quarto to convert to docusaurus-md format
    quarto render "$notebook_path" --to docusaurus-md --output-dir "$output_dir" || {
        echo "  ❌ Quarto conversion failed for $notebook_name"
        return 1
    }
    
    # Quarto outputs .md files, rename to .mdx for Docusaurus
    if [ -f "$output_dir/$notebook_name.md" ]; then
        mv "$output_dir/$notebook_name.md" "$output_dir/$notebook_name.mdx"
        echo "  ✅ Created: $notebook_name.mdx"
    else
        echo "  ⚠️  Expected output file not found: $output_dir/$notebook_name.md"
    fi
}

echo "📝 Converting key notebooks..."

# 1. Essential basics
echo ""
echo "🚀 Converting basics..."
convert_notebook "$NOTEBOOK_SOURCE/pixeltable-basics.ipynb" "$DOCS_OUTPUT"

# 2. Top use cases (most important ones)
echo ""
echo "💡 Converting use cases..."
convert_notebook "$NOTEBOOK_SOURCE/use-cases/rag-demo.ipynb" "$DOCS_OUTPUT/use-cases"
convert_notebook "$NOTEBOOK_SOURCE/use-cases/object-detection-in-videos.ipynb" "$DOCS_OUTPUT/use-cases"
convert_notebook "$NOTEBOOK_SOURCE/use-cases/audio-transcriptions.ipynb" "$DOCS_OUTPUT/use-cases"

# 3. Key integrations (most popular ones)
echo ""
echo "🔌 Converting integrations..."
convert_notebook "$NOTEBOOK_SOURCE/integrations/working-with-openai.ipynb" "$DOCS_OUTPUT/integrations"
convert_notebook "$NOTEBOOK_SOURCE/integrations/working-with-anthropic.ipynb" "$DOCS_OUTPUT/integrations"
convert_notebook "$NOTEBOOK_SOURCE/integrations/working-with-ollama.ipynb" "$DOCS_OUTPUT/integrations"

echo ""
echo "📊 CONVERSION COMPLETE!"
echo ""

# Count results
total_files=$(find "$DOCS_OUTPUT" -name "*.mdx" | wc -l)
echo "✅ Converted: $total_files notebook(s)"
echo ""

echo "📁 Generated files:"
find "$DOCS_OUTPUT" -name "*.mdx" | sort

echo ""
echo "🚀 Next steps:"
echo "   1. Update sidebars.js to include these examples"
echo "   2. Test with: npm start"
echo "   3. If successful, convert more notebooks"
