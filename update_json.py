#!/usr/bin/env python3
"""
Script to add sharing, distribution, and pdf_url fields to all zine entries
"""

import json

# Read the existing JSON file
with open('zines_data.json', 'r', encoding='utf-8') as f:
    zines = json.load(f)

# Add new fields to each zine
for zine in zines:
    # Add sharing field (default to [1] - preview only)
    zine['sharing'] = [1]

    # Add distribution field (empty string by default)
    zine['distribution'] = ""

    # Add pdf_url field (empty string by default)
    zine['pdf_url'] = ""

    # Optional: add shop_url field for option 4
    zine['shop_url'] = ""

# Write back to file with nice formatting
with open('zines_data.json', 'w', encoding='utf-8') as f:
    json.dump(zines, f, ensure_ascii=False, indent=2)

print(f"✓ Updated {len(zines)} zine entries")
print("✓ Added 'sharing', 'distribution', 'pdf_url', and 'shop_url' fields to all entries")
