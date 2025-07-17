#!/bin/bash
# Fallback converter: Use nbconvert for failing notebooks, flat structure

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="/Users/rob/repos/pixeltable/docs3/docs/examples"

echo "🔄 Fallback Notebook Converter (nbconvert + flat structure)"
echo "📂 Source: $NOTEBOOK_SOURCE"
echo "📂 Output: $DOCS_OUTPUT (flat)"
echo ""

# Create output directory
mkdir -p "$DOCS_OUTPUT"

# Function to convert with nbconvert fallback
fallback_convert() {
    local notebook_path="$1"
    local notebook_name=$(basename "$notebook_path" .ipynb)
    
    echo "  🔄 Converting: $notebook_name"
    
    # Try nbconvert to markdown
    jupyter nbconvert --to markdown --no-input --output-dir="$DOCS_OUTPUT" "$notebook_path" || {
        echo "  ❌ nbconvert failed for $notebook_name"
        return 1
    }
    
    # Convert .md to .mdx with simple frontmatter
    local md_file="$DOCS_OUTPUT/$notebook_name.md"
    local mdx_file="$DOCS_OUTPUT/$notebook_name.mdx"
    
    if [ -f "$md_file" ]; then
        # Add simple frontmatter and rename
        {
            echo "---"
            echo "title: \"$(echo "$notebook_name" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')\""
            echo "description: \"Jupyter notebook example for Pixeltable\""
            echo "---"
            echo ""
            cat "$md_file"
        } > "$mdx_file"
        
        rm "$md_file"
        echo "  ✅ Created: $notebook_name.mdx"
        
        # Show file size
        local file_size=$(wc -c < "$mdx_file")
        echo "     Size: $(($file_size / 1024))KB"
    else
        echo "  ❌ No markdown file generated"
    fi
}

echo "🔍 Finding all notebooks..."

# Find all .ipynb files recursively and convert them
find "$NOTEBOOK_SOURCE" -name "*.ipynb" -type f | while read notebook; do
    fallback_convert "$notebook"
done

echo ""
echo "📊 FALLBACK CONVERSION COMPLETE!"
echo ""

# Show results
echo "📁 All converted files (flat structure):"
find "$DOCS_OUTPUT" -name "*.mdx" -exec ls -lh {} \; | sort

total_files=$(find "$DOCS_OUTPUT" -name "*.mdx" | wc -l)
echo ""
echo "✅ Total converted: $total_files notebooks"
echo "📁 All files in flat structure at: $DOCS_OUTPUT"
echo ""
echo "🚀 Next: Update sidebars.js to include all the new files"
