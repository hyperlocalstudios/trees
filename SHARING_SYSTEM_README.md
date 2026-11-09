# Reading the Trees - Sharing System Documentation

## Overview

This system allows you to specify how each zine can be shared with website visitors. You control four sharing options and track distribution preferences for each zine.

---

## Sharing Options

Each zine can have one or more of these sharing options:

| Code | Public Display | Description | Required Fields |
|------|---------------|-------------|-----------------|
| **1** | **Preview Only** | Display basic info, creator credit, and description only (no downloads or purchases) | None |
| **2** | **Print-At-Home Copy** | Make the zine available as a free downloadable PDF | `pdf_url` (Google Drive link) |
| **3** | **Request a Copy** | Provide contact info so visitors can reach out to request copies | Artist's Instagram or Website |
| **4** | **Order a Copy** | Link to the creator's shop or website where visitors can purchase a physical copy | `shop_url` or `website` |

### Important Notes:
- **Option 1 is always included** - Every zine shows basic information
- **If ONLY option 1 is selected**, the website displays "Preview Only"
- **Multiple options can be selected** - e.g., a zine could offer both free downloads (2) AND shop purchases (4)

---

## Distribution Options (Internal Use Only)

These are **NOT displayed to the public** - they're for your records only:

| Code | Meaning | Description |
|------|---------|-------------|
| **L** | Limited Distribution | Original Exchange collection, mystery bundles only |
| **O** | Open Distribution | Continue printing, future themed bundles, partner retailers |

---

## How to Add Sharing Preferences

### Step 1: Open the Data Entry Guide

Open `SHARING_DATA_ENTRY_GUIDE.csv` in Excel, Google Sheets, or any spreadsheet program.

### Step 2: Fill in the Columns

For each zine, enter:

1. **Sharing** (required): Enter numbers 1-4, separated by commas
   - Examples:
     - `1` = Preview only
     - `1,2` = Preview + Free download
     - `1,2,3,4` = All options available
     - `1,3,4` = Preview + Request + Order (no free download)

2. **Distribution** (optional): Enter `L` or `O`

3. **PDF URL** (required if sharing includes 2):
   - Upload your PDF to Google Drive
   - Right-click → Get link → Set to "Anyone with the link can view"
   - Copy the full Google Drive link
   - Paste into this column

4. **Shop URL** (required if sharing includes 4):
   - If the artist has a dedicated shop page, enter it here
   - If left blank, the system will use the artist's website

5. **Notes** (optional): Any internal notes for your reference

### Step 3: Transfer to JSON

Once you've filled out the CSV, you'll need to manually update the `zines_data.json` file.

For each zine, update these fields:

```json
{
  "title": "Example Zine",
  "sharing": [1, 2, 3],          // Array of numbers from your CSV
  "distribution": "O",            // "L" or "O" from your CSV
  "pdf_url": "https://drive.google.com/...",  // Google Drive link
  "shop_url": "https://shop.example.com"      // Shop URL (optional)
}
```

### Step 4: Sync to Website

After updating `zines_data.json`, run:

```bash
cd /Users/klgraywill/CodeProjects/Hyperlocal/reading-the-trees
python3 sync_inline_json.py
```

This will update the inline JSON in `index.html` to match your changes.

---

## Examples

### Example 1: Preview Only (Default)
**Sharing:** `1`
**Distribution:** `L`
**Result:** Website shows "Preview Only" - visitors can only view basic info

```json
{
  "sharing": [1],
  "distribution": "L",
  "pdf_url": "",
  "shop_url": ""
}
```

### Example 2: Free Download Available
**Sharing:** `1,2`
**Distribution:** `O`
**PDF URL:** `https://drive.google.com/file/d/abc123/view`
**Result:** Website shows "Print-At-Home Copy" button

```json
{
  "sharing": [1, 2],
  "distribution": "O",
  "pdf_url": "https://drive.google.com/file/d/abc123/view",
  "shop_url": ""
}
```

### Example 3: Multiple Sharing Options
**Sharing:** `1,2,3,4`
**Distribution:** `O`
**PDF URL:** `https://drive.google.com/file/d/abc123/view`
**Shop URL:** `https://etsy.com/shop/artistshop`
**Result:** Website shows all three options:
- 📥 Print-At-Home Copy (links to Google Drive)
- ✉️ Request a Copy (links to artist's Instagram/website)
- 🛒 Order a Copy (links to shop)

```json
{
  "sharing": [1, 2, 3, 4],
  "distribution": "O",
  "pdf_url": "https://drive.google.com/file/d/abc123/view",
  "shop_url": "https://etsy.com/shop/artistshop"
}
```

### Example 4: Request & Order Only (No Free Download)
**Sharing:** `1,3,4`
**Distribution:** `L`
**Shop URL:** `https://artist.com/shop`
**Result:** Website shows:
- ✉️ Request a Copy
- 🛒 Order a Copy

```json
{
  "sharing": [1, 3, 4],
  "distribution": "L",
  "pdf_url": "",
  "shop_url": "https://artist.com/shop"
}
```

---

## Google Drive Setup for PDFs

1. Upload your PDF to Google Drive
2. Right-click the file → **Share**
3. Under "General access", select **Anyone with the link**
4. Set permission to **Viewer**
5. Click **Copy link**
6. Paste the full link into the CSV (e.g., `https://drive.google.com/file/d/1ABC-XYZ123/view?usp=sharing`)

**Note:** Google Drive links work great because:
- No storage limits on your GitHub repo
- Easy to update PDFs without changing code
- Bandwidth is handled by Google
- Visitors can download or view in browser

---

## Troubleshooting

### Sharing section doesn't appear
- Check that `sharing` array exists and has at least one number
- Verify JSON syntax is correct (commas, brackets)
- Run `sync_inline_json.py` to ensure HTML is updated

### "Print-At-Home Copy" button doesn't work
- Verify `pdf_url` is not empty
- Test the Google Drive link in a private browser window
- Ensure link sharing is set to "Anyone with the link"

### "Request a Copy" has no link
- Ensure the artist has either `instagram` or `website` filled in
- The system will automatically use the first available contact method

### Changes aren't showing on website
- Make sure you updated BOTH `zines_data.json` AND ran `sync_inline_json.py`
- Clear your browser cache (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
- Check browser console for JavaScript errors

---

## File Structure

```
reading-the-trees/
├── zines_data.json                    # Main data source (edit this)
├── index.html                         # Website (contains inline JSON copy)
├── sync_inline_json.py                # Script to sync JSON to HTML
├── SHARING_DATA_ENTRY_GUIDE.csv       # Spreadsheet for easy data entry
└── SHARING_SYSTEM_README.md           # This file
```

---

## Quick Reference

### Sharing Codes
- `1` = Preview Only (always included)
- `2` = Free Download
- `3` = Contact for Copy
- `4` = Shop Purchase

### Distribution Codes (Internal)
- `L` = Limited
- `O` = Open

### Required URLs
- **Option 2** requires: `pdf_url`
- **Option 3** requires: `instagram` OR `website` (already in your data)
- **Option 4** requires: `shop_url` OR `website`

---

## Support

If you encounter issues or have questions:
1. Check the examples above
2. Verify your JSON syntax at [jsonlint.com](https://jsonlint.com/)
3. Review the browser console for JavaScript errors
4. Check that `sync_inline_json.py` ran without errors

---

**Last Updated:** 2026-11-08
