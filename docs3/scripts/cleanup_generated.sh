#!/bin/bash
# Delete all generated MDX files

echo "🗑️ Cleaning up generated MDX files..."

# Delete main pixeltable-basics.mdx
rm -f "/Users/rob/repos/pixeltable/docs3/docs/examples/pixeltable-basics.mdx"

# Delete all MDX files in subdirectories except index.mdx
find "/Users/rob/repos/pixeltable/docs3/docs/examples" -name "*.mdx" -not -name "index.mdx" -delete

echo "✅ Cleanup complete!"
echo "📁 Kept index.mdx files for structure"
