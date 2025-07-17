#!/bin/bash
# Convert notebooks and move them to the right place (because Quarto cult logic)

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="/Users/rob/repos/pixeltable/docs3/docs/examples"

echo "🕯️ Appeasing the Quarto Cult Gods"
echo ""

# Function to convert and move
convert_and_move() {
    local notebook_path="$1"
    local target_dir="$2"
    local notebook_name=$(basename "$notebook_path" .ipynb)
    local notebook_dir=$(dirname "$notebook_path")
    
    echo "  🔄 Converting: $notebook_name"
    
    # Convert (creates file next to original notebook)
    quarto render "$notebook_path" --to docusaurus-md || {
        echo "  ❌ Conversion failed"
        return 1
    }
    
    # Move from cult location to proper location
    if [ -f "$notebook_dir/$notebook_name.mdx" ]; then
        mkdir -p "$target_dir"
        mv "$notebook_dir/$notebook_name.mdx" "$target_dir/"
        echo "  ✅ Moved to: $target_dir/$notebook_name.mdx"
    else
        echo "  ❌ File not found: $notebook_dir/$notebook_name.mdx"
    fi
}

echo "🔌 Converting integrations..."
convert_and_move "$NOTEBOOK_SOURCE/integrations/working-with-openai.ipynb" "$DOCS_OUTPUT/integrations"
convert_and_move "$NOTEBOOK_SOURCE/integrations/working-with-anthropic.ipynb" "$DOCS_OUTPUT/integrations"
convert_and_move "$NOTEBOOK_SOURCE/integrations/working-with-ollama.ipynb" "$DOCS_OUTPUT/integrations"

echo ""
echo "💡 Converting remaining use cases..."
convert_and_move "$NOTEBOOK_SOURCE/use-cases/audio-transcriptions.ipynb" "$DOCS_OUTPUT/use-cases"
convert_and_move "$NOTEBOOK_SOURCE/use-cases/object-detection-in-videos.ipynb" "$DOCS_OUTPUT/use-cases"

echo ""
echo "📊 CULT APPEASEMENT COMPLETE!"
echo ""
echo "🚀 Now update sidebars.js and test with npm start"
