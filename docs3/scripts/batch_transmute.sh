#!/bin/bash

# 🎭 THE GREAT BATCH TRANSMUTATION RITUAL 🎭
# Transmutes all Jupyter scrolls in a directory into Docusaurus parchments

echo "🔮 Beginning the Great Batch Transmutation..."

# Make the Python script executable
chmod +x scripts/jupyter_to_docusaurus.py

# Find all .ipynb files and transmute them
find . -name "*.ipynb" -type f | while read notebook; do
    echo "⚗️ Transmuting: $notebook"
    python3 scripts/jupyter_to_docusaurus.py "$notebook" -d "examples"
done

echo "✨ All notebooks have been transmuted into MDX parchments!"
echo "📜 Check the docs3/docs/examples directory for your new documentation scrolls"
