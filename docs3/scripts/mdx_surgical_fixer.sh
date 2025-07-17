#!/bin/bash
# MDX Surgical JSX Fixer - Fix the EXACT errors Docusaurus is complaining about

set -e

DOCS_OUTPUT="/Users/rob/repos/pixeltable/docs3/docs/examples"

echo "🔧 MDX Surgical JSX Fixer - Targeting specific Docusaurus errors"
echo "📂 Target: $DOCS_OUTPUT"
echo ""

# Function to surgically fix JSX compliance issues
surgical_fix() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "  🔧 Fixing: $filename"
    
    # Create backup
    cp "$file" "$file.backup"
    
    # Python script to fix specific JSX issues
    python3 - "$file" << 'EOF'
import sys
import re

def fix_jsx_issues(content):
    """Fix specific JSX compliance issues that Docusaurus complains about"""
    
    # Fix 1: "Unexpected character '0' before name" 
    # This happens with invalid attributes like width="100px" becoming width=100px
    # Fix: Ensure all attribute values are quoted
    content = re.sub(r'(\w+)=([0-9][a-zA-Z%]*)', r'\1="\2"', content)
    
    # Fix 2: "Unexpected character '0' after attribute name"
    # This happens with malformed attributes like style0="..." 
    # Fix: Remove invalid attribute names starting with numbers
    content = re.sub(r'\s+[0-9][a-zA-Z0-9]*="[^"]*"', '', content)
    
    # Fix 3: Self-closing tag issues - "Unexpected closing tag </a>, expected </img>"
    # Fix: Properly self-close void elements
    void_elements = ['img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']
    
    for element in void_elements:
        # Fix unclosed void elements
        content = re.sub(rf'<{element}([^>]*?)>(?!</{element}>)', rf'<{element}\1 />', content)
        
        # Fix void elements with closing tags
        content = re.sub(rf'<{element}([^>]*?)></{element}>', rf'<{element}\1 />', content)
    
    # Fix 4: JSX expression issues - "Could not parse expression with acorn"
    # Fix: Escape problematic content in code blocks and inline expressions
    
    # Fix malformed JSX expressions - often caused by unescaped braces
    # Replace standalone { or } that aren't part of valid JSX expressions
    content = re.sub(r'(?<!{){(?!{)([^}]*?)(?<!})}(?!})', r'\\{\1\\}', content)
    
    # Fix 5: Import/export parsing issues
    # Remove or comment out malformed import statements
    content = re.sub(r'^import[^;]*;?\s*$', r'<!-- \g<0> -->', content, flags=re.MULTILINE)
    content = re.sub(r'^export[^;]*;?\s*$', r'<!-- \g<0> -->', content, flags=re.MULTILINE)
    
    # Fix 6: HTML attribute compliance for JSX
    content = content.replace('class=', 'className=')
    content = content.replace('for=', 'htmlFor=')
    
    # Fix 7: Escape problematic characters in code blocks
    # Find code blocks and escape JSX-problematic content
    def escape_code_block(match):
        code = match.group(1)
        # Escape braces in code blocks
        code = code.replace('{', '\\{').replace('}', '\\}')
        return f'```{code}```'
    
    content = re.sub(r'```(.*?)```', escape_code_block, content, flags=re.DOTALL)
    
    # Fix 8: Remove HTML comments that can break JSX parsing
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Fix 9: Fix malformed URLs in markdown links
    content = re.sub(r'\[([^\]]*)\]\(([^)]*)\)', lambda m: f'[{m.group(1)}]({m.group(2).replace(" ", "%20")})', content)
    
    return content

def fix_specific_docusaurus_errors(content):
    """Fix the exact patterns from the error messages"""
    
    # Error: "Unexpected character `/` before local name"
    # Fix: Escape problematic forward slashes in JSX
    content = re.sub(r'<([^a-zA-Z])', r'&lt;\1', content)
    
    # Error: HTML entities in JSX contexts
    html_entities = {
        '&lt;': '<',
        '&gt;': '>', 
        '&amp;': '&',
        '&quot;': '"',
        '&apos;': "'",
        '&nbsp;': ' '
    }
    
    for entity, char in html_entities.items():
        content = content.replace(entity, char)
    
    # Fix style attributes to be JSX-compliant objects
    def fix_style_attr(match):
        style_content = match.group(1)
        # Convert CSS string to JSX style object format
        return f'style={{{{{repr(style_content)}}}}}'
    
    content = re.sub(r'style="([^"]*)"', fix_style_attr, content)
    
    return content

if __name__ == "__main__":
    filepath = sys.argv[1]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply fixes
    content = fix_jsx_issues(content)
    content = fix_specific_docusaurus_errors(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"    ✅ Fixed JSX issues in {filepath}")

EOF
    
    # Additional sed fixes for specific patterns
    sed -i '' \
        -e 's/<img \([^>]*\)>/<img \1 \/>/g' \
        -e 's/<br>/<br \/>/g' \
        -e 's/<hr>/<hr \/>/g' \
        -e 's/<input \([^>]*\)>/<input \1 \/>/g' \
        -e 's/class="/className="/g' \
        -e 's/for="/htmlFor="/g' \
        "$file"
    
    echo "    ✅ Applied surgical fixes to $filename"
}

# Function to validate MDX file (basic check)
validate_mdx() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Basic validation - check for common JSX issues
    if grep -q "class=" "$file"; then
        echo "    ⚠️  Warning: Still contains 'class=' attributes"
    fi
    
    if grep -q "<img[^>]*[^/]>" "$file"; then
        echo "    ⚠️  Warning: Contains unclosed img tags" 
    fi
    
    if grep -q "^import " "$file"; then
        echo "    ⚠️  Warning: Contains import statements"
    fi
    
    # Check file size (files over 2MB might have other issues)
    local size=$(wc -c < "$file")
    if [ $size -gt 2097152 ]; then  # 2MB
        echo "    ⚠️  Warning: Large file ($(($size / 1024 / 1024))MB) - might have performance issues"
    fi
}

echo "🔍 Finding and fixing all MDX files..."

# Process all MDX files
find "$DOCS_OUTPUT" -name "*.mdx" -type f | while read mdx_file; do
    surgical_fix "$mdx_file"
    validate_mdx "$mdx_file"
done

echo ""
echo "🔧 SURGICAL MDX FIXES COMPLETE!"
echo ""

# Show summary
total_files=$(find "$DOCS_OUTPUT" -name "*.mdx" | wc -l)
echo "✅ Processed: $total_files MDX files"
echo "🔧 Applied surgical fixes for:"
echo "   - Unexpected character errors"
echo "   - Unclosed tag issues" 
echo "   - JSX expression parsing"
echo "   - Import/export problems"
echo "   - HTML attribute compliance"
echo ""
echo "🚀 Now try: npm start in docs3/"
echo ""
echo "💡 If there are still errors, we can target the specific remaining issues!"
