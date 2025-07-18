#!/usr/bin/env python3
"""Find and fix common MDX parsing issues in converted notebooks."""

import re
import os
import glob

def fix_mdx_issues(file_path):
    """Fix common MDX parsing issues in a file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_applied = []
    
    # 1. Escape unescaped curly braces in regular text (not in code blocks)
    # This is the most common cause of MDX parsing errors
    
    # First, protect code blocks from modification
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    # Protect fenced code blocks
    content = re.sub(r'```[\s\S]*?```', save_code_block, content)
    # Protect inline code
    content = re.sub(r'`[^`]+`', save_code_block, content)
    
    # Now escape curly braces in the remaining content
    original_braces = content.count('{') + content.count('}')
    content = content.replace('{', '\\{').replace('}', '\\}')
    new_braces = content.count('\\{') + content.count('\\}')
    
    if new_braces > 0:
        fixes_applied.append(f"Escaped {new_braces//2} curly brace pairs")
    
    # Restore code blocks
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", code_block)
    
    # 2. Fix any remaining JSX image tags that might have issues
    def fix_img_tag(match):
        full_tag = match.group(0)
        # Ensure self-closing tag has space before />
        if not full_tag.endswith(' />'):
            fixed = full_tag[:-2] + ' />'
            return fixed
        return full_tag
    
    img_fixes = 0
    new_content = re.sub(r'<img[^>]*/?>', fix_img_tag, content)
    if new_content != content:
        img_fixes = len(re.findall(r'<img[^>]*/?>', content))
        fixes_applied.append(f"Fixed {img_fixes} img tags")
        content = new_content
    
    # 3. Escape any remaining problematic characters
    # Fix HTML entities that might confuse JSX
    content = re.sub(r'&(?!amp;|lt;|gt;|quot;|#)', r'&amp;', content)
    
    return content, fixes_applied, content != original_content

def main():
    """Fix all MDX files in the jupyter directory."""
    
    jupyter_dir = "/Users/rob/repos/pixeltable/docs3/docs/jupyter"
    mdx_files = glob.glob(os.path.join(jupyter_dir, "*.mdx"))
    
    print(f"Found {len(mdx_files)} MDX files to check...")
    
    for file_path in mdx_files:
        filename = os.path.basename(file_path)
        print(f"\nChecking {filename}...")
        
        try:
            fixed_content, fixes, was_modified = fix_mdx_issues(file_path)
            
            if was_modified:
                # Backup original
                backup_path = file_path + ".backup"
                with open(file_path, 'r', encoding='utf-8') as f:
                    with open(backup_path, 'w', encoding='utf-8') as backup:
                        backup.write(f.read())
                
                # Write fixed version
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"  ✅ Fixed: {', '.join(fixes)}")
                print(f"  📁 Backup saved as {filename}.backup")
            else:
                print(f"  ✓ No fixes needed")
                
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
    
    print(f"\n🎉 Completed processing {len(mdx_files)} files!")
    print("Try running Docusaurus again to see if the errors are resolved.")

if __name__ == "__main__":
    main()
