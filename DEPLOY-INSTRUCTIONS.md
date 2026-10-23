# Deploy Instructions - Super Simple!

## Step 1: Create GitHub Repository (2 minutes)

1. Go to: **https://github.com/new**
2. Make sure you're logged in as **hyperlocalstudios**
3. Fill in:
   - Repository name: **`reading-the-trees`**
   - Description: "Reading the Trees zine anthology"
   - Select: **Public**
   - DO NOT check "Add a README"
4. Click **"Create repository"**

## Step 2: Connect and Push (1 minute)

Copy and paste these commands ONE AT A TIME into Terminal:

```bash
cd "/Users/klgraywill/CodeProjects/hyperlocal/reading-the-trees"
```

```bash
git branch -M main
```

```bash
git remote add origin https://github.com/hyperlocalstudios/reading-the-trees.git
```

```bash
git push -u origin main
```

**When it asks for username/password:**
- Username: `hyperlocalstudios`
- Password: Use a NEW token from https://github.com/settings/tokens/new
  - Check the "repo" box
  - Generate and copy the token
  - Paste it when Terminal asks for password

## Step 3: Enable GitHub Pages (1 minute)

1. Go to: **https://github.com/hyperlocalstudios/reading-the-trees/settings/pages**
2. Under "Branch":
   - Select: **main**
   - Select: **/ (root)**
3. Click **"Save"**
4. Wait 2 minutes and refresh

Your site will be live at:
**https://hyperlocalstudios.github.io/reading-the-trees**

## That's It!

The images are hosted right in the repository, no separate image hosting needed!

To update the site later, just edit index.html and:
```bash
git add .
git commit -m "Update zine info"
git push
```
