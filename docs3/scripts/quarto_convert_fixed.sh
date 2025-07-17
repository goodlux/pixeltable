#!/bin/bash
# Fixed Quarto-based notebook conversion for Pixeltable docs

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="docs3/docs/examples"

echo "🔮 Fixed Quarto Notebook Conversion for Pixeltable"
echo "📂 Source: $NOTEBOOK_SOURCE"
echo "📂 Output: $DOCS_OUTPUT"
echo ""

# Check if Quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "❌ Quarto not found. Install with:"
    echo "   pip install quarto-cli"
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
    echo "     From: $notebook_path"
    echo "     To: $output_dir"
    
    # Change to the output directory before running Quarto
    pushd "$output_dir" > /dev/null
    
    # Use Quarto to convert - using absolute paths
    quarto render "$(realpath "$notebook_path")" --to docusaurus-md --output "$notebook_name.mdx" || {
        echo "  ❌ Quarto conversion failed for $notebook_name"
        popd > /dev/null
        return 1
    }
    
    popd > /dev/null
    
    # Check if file was created
    if [ -f "$output_dir/$notebook_name.mdx" ]; then
        echo "  ✅ Created: $notebook_name.mdx"
        # Show file size for verification
        local file_size=$(wc -c < "$output_dir/$notebook_name.mdx")
        echo "     Size: $file_size bytes"
    else
        echo "  ❌ File not created: $output_dir/$notebook_name.mdx"
        echo "     Contents of $output_dir:"
        ls -la "$output_dir/"
    fi
}

echo "📝 Converting key notebooks..."

# 1. Essential basics
echo ""
echo "🚀 Converting basics..."
convert_notebook "$NOTEBOOK_SOURCE/pixeltable-basics.ipynb" "$DOCS_OUTPUT"

# 2. Top use cases 
echo ""
echo "💡 Converting use cases..."
convert_notebook "$NOTEBOOK_SOURCE/use-cases/rag-demo.ipynb" "$DOCS_OUTPUT/use-cases"

# Test with just a couple first
echo ""
echo "📊 CONVERSION TEST COMPLETE!"

# Count and list results
if [ -d "$DOCS_OUTPUT" ]; then
    echo ""
    echo "📁 Files in output directory:"
    find "$DOCS_OUTPUT" -name "*.mdx" -exec ls -lh {} \;
    
    total_files=$(find "$DOCS_OUTPUT" -name "*.mdx" | wc -l)
    echo ""
    echo "✅ Total converted: $total_files file(s)"
fi

echo ""
echo "🚀 Next steps:"
echo "   1. Check the generated files look good"
echo "   2. Test with: npm start"
echo "   3. If successful, convert more notebooks"
