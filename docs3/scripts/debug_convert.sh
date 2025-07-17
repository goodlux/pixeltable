#!/bin/bash
# Debug version to see what's going wrong

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="docs3/docs/examples"

echo "🔍 DEBUGGING NOTEBOOK CONVERSION"
echo ""

# Check if jupyter is available
echo "📋 Checking jupyter installation..."
which jupyter || echo "❌ jupyter not found in PATH"
echo ""

# Check if nbconvert is available
echo "📋 Checking nbconvert..."
jupyter nbconvert --help >/dev/null 2>&1 && echo "✅ nbconvert available" || echo "❌ nbconvert not available"
echo ""

# Check if notebook exists
NOTEBOOK_PATH="$NOTEBOOK_SOURCE/pixeltable-basics.ipynb"
echo "📋 Checking notebook file: $NOTEBOOK_PATH"
if [ -f "$NOTEBOOK_PATH" ]; then
    echo "✅ Notebook exists"
    echo "📊 File size: $(wc -c < "$NOTEBOOK_PATH") bytes"
else
    echo "❌ Notebook not found"
    echo "📁 Available files in $NOTEBOOK_SOURCE:"
    ls -la "$NOTEBOOK_SOURCE"/*.ipynb 2>/dev/null || echo "No .ipynb files found"
fi
echo ""

# Try converting with full error output
if [ -f "$NOTEBOOK_PATH" ]; then
    echo "🧪 Testing nbconvert with full error output..."
    mkdir -p "$DOCS_OUTPUT"
    jupyter nbconvert \
        --to markdown \
        --no-input \
        --output-dir="$DOCS_OUTPUT" \
        "$NOTEBOOK_PATH" || echo "❌ Conversion failed - see error above"
fi
