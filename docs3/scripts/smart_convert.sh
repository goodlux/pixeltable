#!/bin/bash
# Smart notebook conversion using nbconvert + post-processing

set -e

NOTEBOOK_SOURCE="/Users/rob/repos/pixeltable/docs/notebooks"
DOCS_OUTPUT="docs3/docs/examples"

echo "🚀 Smart Notebook Conversion Pipeline"
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
    
    # Step 1: Use nbconvert for clean conversion (no input prompts, limited output)
    jupyter nbconvert \
        --to markdown \
        --no-input \
        --output-dir="$DOCS_OUTPUT/$output_subdir" \
        "$notebook_path" \
        2>/dev/null || {
            echo "  ❌ nbconvert failed for $notebook_name"
            return 1
        }
    
    # Step 2: Post-process to MDX with frontmatter
    local md_file="$DOCS_OUTPUT/$output_subdir/$notebook_name.md"
    local mdx_file="$DOCS_OUTPUT/$output_subdir/$notebook_name.mdx"
    
    if [ -f "$md_file" ]; then
        python3 -c "
import re
import sys

# Read the markdown file
with open('$md_file', 'r') as f:
    content = f.read()

# Extract title from filename or first H1
title = '$notebook_name'.replace('_', ' ').replace('-', ' ').title()

# Look for H1 in content
h1_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
if h1_match:
    title = h1_match.group(1).strip()
    # Remove the H1 from content since it'll be in frontmatter
    content = re.sub(r'^#\s+.+\n?', '', content, count=1, flags=re.MULTILINE)

# Extract description from first meaningful paragraph
description = 'Jupyter notebook example for Pixeltable'
lines = content.split('\n')
for line in lines:
    clean_line = line.strip()
    if clean_line and not clean_line.startswith('#') and not clean_line.startswith('!') and len(clean_line) > 30:
        # Remove markdown formatting for description
        description = re.sub(r'[*_\`]', '', clean_line)
        description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)
        if len(description) > 150:
            description = description[:147] + '...'
        break

# Clean title and description for YAML
title = title.replace('\"', '\\\\"')
description = description.replace('\"', '\\\\"')

# Create frontmatter
frontmatter = f'''---
title: \"{title}\"
description: \"{description}\"
---

'''

# Clean content for MDX
# Remove excessive image outputs
content = re.sub(r'!\[png\]\([^)]+\)', ':::note\n📊 Chart/image output (rendered in notebook)\n:::', content)

# Remove style tags
content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)

# Limit very long code output blocks
def limit_output_block(match):
    block_content = match.group(1)
    lines = block_content.split('\n')
    if len(lines) > 20:
        return '    ' + '\n    '.join(lines[:10]) + '\n    ... (output truncated)'
    return match.group(0)

content = re.sub(r'^    (.+)$', limit_output_block, content, flags=re.MULTILINE)

# Write MDX file
with open('$mdx_file', 'w') as f:
    f.write(frontmatter + content)

print(f'  ✅ Created: {os.path.basename(\"$mdx_file\")}')
"
        # Remove the original .md file
        rm "$md_file"
    else
        echo "  ❌ No markdown file generated for $notebook_name"
    fi
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

# Count results
total_mdx=$(find "$DOCS_OUTPUT" -name "*.mdx" -not -name "index.mdx" | wc -l)
echo "   📝 Converted: $total_mdx notebooks"
echo "   📁 Using nbconvert for clean output"
echo "   🎯 MDX files ready for Docusaurus"
echo ""
echo "🚀 Next steps:"
echo "   1. Review generated files for any issues"
echo "   2. Add to Docusaurus sidebar configuration"
echo "   3. Test the documentation site"
