#!/bin/bash
# Convert all notebooks under 1MB (because we're not masochists)

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="/Users/rob/repos/pixeltable/docs3/docs/examples"
MAX_SIZE_MB=1

echo "🧠 Smart Notebook Conversion (< ${MAX_SIZE_MB}MB only)"
echo "📂 Source: $NOTEBOOK_SOURCE"
echo "📂 Output: $DOCS_OUTPUT"
echo ""

# Function to check file size and convert if reasonable
smart_convert() {
    local notebook_path="$1"
    local target_dir="$2"
    local notebook_name=$(basename "$notebook_path" .ipynb)
    local notebook_dir=$(dirname "$notebook_path")
    
    # Check file size (in bytes)
    local file_size=$(wc -c < "$notebook_path")
    local max_size_bytes=$((MAX_SIZE_MB * 1024 * 1024))
    local size_mb=$((file_size / 1024 / 1024))
    
    if [ "$file_size" -gt "$max_size_bytes" ]; then
        echo "  ⏭️  Skipping: $notebook_name (${size_mb}MB - too chonky)"
        return 0
    fi
    
    echo "  🔄 Converting: $notebook_name ($(($file_size / 1024))KB)"
    
    # Convert (creates file next to original notebook)
    quarto render "$notebook_path" --to docusaurus-md || {
        echo "  ❌ Conversion failed for $notebook_name"
        return 1
    }
    
    # Move from cult location to proper location
    if [ -f "$notebook_dir/$notebook_name.mdx" ]; then
        mkdir -p "$target_dir"
        mv "$notebook_dir/$notebook_name.mdx" "$target_dir/"
        echo "  ✅ Moved to: $target_dir/$notebook_name.mdx"
    else
        echo "  ❌ File not found after conversion: $notebook_dir/$notebook_name.mdx"
    fi
}

# Convert all notebooks recursively, checking size first
echo "🔍 Scanning and converting reasonable-sized notebooks..."

# Root level
for notebook in "$NOTEBOOK_SOURCE"/*.ipynb; do
    if [ -f "$notebook" ]; then
        smart_convert "$notebook" "$DOCS_OUTPUT"
    fi
done

# Fundamentals
if [ -d "$NOTEBOOK_SOURCE/fundamentals" ]; then
    echo ""
    echo "📚 Processing fundamentals..."
    for notebook in "$NOTEBOOK_SOURCE/fundamentals"/*.ipynb; do
        if [ -f "$notebook" ]; then
            smart_convert "$notebook" "$DOCS_OUTPUT/fundamentals"
        fi
    done
fi

# Feature Guides
if [ -d "$NOTEBOOK_SOURCE/feature-guides" ]; then
    echo ""
    echo "🔧 Processing feature guides..."
    for notebook in "$NOTEBOOK_SOURCE/feature-guides"/*.ipynb; do
        if [ -f "$notebook" ]; then
            smart_convert "$notebook" "$DOCS_OUTPUT/feature-guides"
        fi
    done
fi

# Use Cases
if [ -d "$NOTEBOOK_SOURCE/use-cases" ]; then
    echo ""
    echo "💡 Processing use cases..."
    for notebook in "$NOTEBOOK_SOURCE/use-cases"/*.ipynb; do
        if [ -f "$notebook" ]; then
            smart_convert "$notebook" "$DOCS_OUTPUT/use-cases"
        fi
    done
fi

# Integrations
if [ -d "$NOTEBOOK_SOURCE/integrations" ]; then
    echo ""
    echo "🔌 Processing integrations..."
    for notebook in "$NOTEBOOK_SOURCE/integrations"/*.ipynb; do
        if [ -f "$notebook" ]; then
            smart_convert "$notebook" "$DOCS_OUTPUT/integrations"
        fi
    done
fi

echo ""
echo "📊 SMART CONVERSION COMPLETE!"
echo ""

# Show what we got
echo "📁 Converted files:"
find "$DOCS_OUTPUT" -name "*.mdx" -exec ls -lh {} \; | sort

total_files=$(find "$DOCS_OUTPUT" -name "*.mdx" | wc -l)
echo ""
echo "✅ Total converted: $total_files notebooks"
echo "🧠 Only converted reasonable-sized files (< ${MAX_SIZE_MB}MB)"
echo ""
echo "🚀 Next: Update sidebars.js to include the new files"
