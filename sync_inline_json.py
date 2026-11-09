#!/usr/bin/env python3
"""
Script to sync the updated zines_data.json into the inline JSON in index.html
"""

import json
import re

# Read the updated JSON file
with open('zines_data.json', 'r', encoding='utf-8') as f:
    zines = json.load(f)

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Convert zines array to formatted JSON string with proper indentation
zines_json = json.dumps(zines, ensure_ascii=False, indent=2)

# Find and replace the inline zines array in HTML
# Pattern: const zines = [...];
pattern = r'const zines = \[.*?\n\]'
replacement = f'const zines = {zines_json}'

# Use DOTALL flag to match across multiple lines
html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Write back to HTML file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ Successfully synced zines_data.json to inline JSON in index.html")
print(f"✓ Updated {len(zines)} zine entries with sharing fields")
