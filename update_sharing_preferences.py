#!/usr/bin/env python3
"""
Script to update zines_data.json with sharing preferences from the distribution spreadsheet
"""

import json
import csv
import re

# Read the CSV file
csv_data = []
with open('Hyperlocal_Exchange_Distribution_Prefs.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_data.append(row)

# Read the existing JSON
with open('zines_data.json', 'r', encoding='utf-8') as f:
    zines = json.load(f)

# Helper function to normalize strings for matching
def normalize(s):
    if not s:
        return ""
    # Remove special characters, convert to lowercase, remove extra spaces
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)  # Keep alphanumeric, spaces, hyphens
    s = re.sub(r'\s+', ' ', s)  # Normalize spaces
    return s

# Helper function to check if checkmark exists
def has_checkmark(value):
    if not value:
        return False
    # Check for checkmark symbol or 'â'
    return 'â' in value or '✓' in value or value.strip().lower() == 'yes'

# Create a mapping of CSV entries to their preferences
csv_mapping = {}
for row in csv_data:
    artist = normalize(row.get('Artist', ''))
    title = normalize(row.get('Zine title', ''))

    # Determine sharing codes
    sharing_codes = [1]  # Always include default

    if has_checkmark(row.get('PDF', '')):
        sharing_codes.append(2)

    if has_checkmark(row.get('Contact', '')):
        sharing_codes.append(3)

    if has_checkmark(row.get('Shop link', '')):
        sharing_codes.append(4)

    # Remove duplicates and sort
    sharing_codes = sorted(list(set(sharing_codes)))

    # Get distribution preference
    distro = row.get('Distro', '').strip()
    if distro.lower() == 'open':
        distribution = 'O'
    elif distro.lower() == 'limited':
        distribution = 'L'
    else:
        distribution = ''

    # Get URLs
    pdf_url = row.get('Drive URL', '').strip()
    shop_url = ''

    # Parse the "Link / contact given" column for shop URLs
    link_contact = row.get('Link / contact given', '').strip()
    if link_contact:
        # Look for URLs in the link_contact field
        url_patterns = [
            r'https?://[^\s,;]+',
            r'www\.[^\s,;]+'
        ]
        for pattern in url_patterns:
            matches = re.findall(pattern, link_contact)
            if matches:
                # Filter for shop-related URLs
                for url in matches:
                    url_lower = url.lower()
                    if any(shop_term in url_lower for shop_term in ['etsy', 'shop', 'store', 'ko-fi', 'patreon', 'itch.io']):
                        shop_url = url
                        break
                if shop_url:
                    break

    # Store preferences
    csv_mapping[(artist, title)] = {
        'sharing': sharing_codes,
        'distribution': distribution,
        'pdf_url': pdf_url,
        'shop_url': shop_url
    }

# Update the JSON entries
matched_count = 0
unmatched_csv = []
unmatched_json = []

for zine in zines:
    zine_artist = normalize(zine.get('artist', ''))
    zine_title = normalize(zine.get('title', ''))

    # Try to find a match
    match_found = False
    best_match = None

    # Try exact match first
    if (zine_artist, zine_title) in csv_mapping:
        best_match = csv_mapping[(zine_artist, zine_title)]
        match_found = True
    else:
        # Try partial matches
        for (csv_artist, csv_title), prefs in csv_mapping.items():
            # Check if artist name is similar
            artist_match = (
                csv_artist in zine_artist or
                zine_artist in csv_artist or
                (csv_artist and zine_artist and csv_artist.split()[0] == zine_artist.split()[0])
            )

            # Check if title is similar
            title_match = (
                csv_title in zine_title or
                zine_title in csv_title or
                (len(csv_title) > 5 and len(zine_title) > 5 and
                 csv_title[:10] == zine_title[:10])
            )

            if artist_match and title_match:
                best_match = prefs
                match_found = True
                break

    if match_found and best_match:
        zine['sharing'] = best_match['sharing']
        zine['distribution'] = best_match['distribution']
        zine['pdf_url'] = best_match['pdf_url']
        zine['shop_url'] = best_match['shop_url']
        matched_count += 1
        print(f"✓ Matched: {zine['artist']} - {zine['title']}")
    else:
        # Keep as preview only
        print(f"⚠ No match: {zine['artist']} - {zine['title']} (keeping as Preview Only)")
        unmatched_json.append(f"{zine['artist']} - {zine['title']}")

# Write updated JSON
with open('zines_data.json', 'w', encoding='utf-8') as f:
    json.dump(zines, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"✓ Successfully updated {matched_count} out of {len(zines)} zine entries")
print(f"⚠ {len(zines) - matched_count} entries kept as Preview Only (no match found)")
print(f"{'='*60}")

if unmatched_json:
    print(f"\nUnmatched zines (kept as Preview Only):")
    for item in unmatched_json:
        print(f"  - {item}")
