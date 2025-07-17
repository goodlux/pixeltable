#!/bin/bash
# MDX Error Inspector - Let's see what's actually at these error positions

DOCS_OUTPUT="/Users/rob/repos/pixeltable/docs3/docs/examples"

echo "🔍 MDX Error Inspector - Let's see what's causing the issues"
echo ""

# Function to inspect specific error locations
inspect_errors() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "📄 Inspecting: $filename"
    
    # Check line 4, column 33 (common error location)
    if [ -f "$file" ]; then
        echo "  Line 4, around column 33:"
        sed -n '4p' "$file" | cut -c25-50 | cat -n
        echo ""
        
        # Check what's in the frontmatter/description area
        echo "  First 10 lines (frontmatter area):"
        head -10 "$file" | cat -n
        echo ""
        
        # Look for problematic patterns
        echo "  Checking for common JSX issues:"
        
        if grep -n "description.*Jupyter notebook example" "$file" > /dev/null; then
            echo "    ✅ Found standard description"
        else
            echo "    ❌ Description might be malformed"
        fi
        
        if grep -n "\\\\{" "$file" > /dev/null; then
            echo "    ⚠️  Found escaped braces: \\{}"
        fi
        
        if grep -n "[0-9][a-zA-Z]*=" "$file" > /dev/null; then
            echo "    ❌ Found number-prefixed attributes"
        fi
        
        echo "  ----------------------------------------"
    fi
}

# Inspect a few problematic files to understand the pattern
echo "🔍 Inspecting files with column 33 errors..."

inspect_errors "$DOCS_OUTPUT/time-zones.mdx"
inspect_errors "$DOCS_OUTPUT/working-with-anthropic.mdx" 
inspect_errors "$DOCS_OUTPUT/pixeltable-basics.mdx"

echo ""
echo "🔍 Let's also check one with the 'unexpected character 0' error..."
inspect_errors "$DOCS_OUTPUT/queries-and-expressions.mdx"
