#!/bin/bash
# Clean up generated files and start fresh

echo "🗑️ Cleaning up generated MDX files..."

# Remove all generated MDX files except index files
find docs3/docs/examples -name "*.mdx" -not -name "index.mdx" -delete
find docs3/docs/examples -name "*.md" -delete

echo "✅ Cleanup complete!"
echo "📁 Kept index.mdx files for structure"
