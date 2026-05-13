# 🚀 Quickstart - Deploy to Streamlit Cloud in 5 Minutes

## Prerequisites
- GitHub account with repo: `praveenkumar815/nutraceutical-reviewer`
- Google API key from [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

## Deploy Steps

### Step 1: Push to GitHub ✓
Already done! Your code is ready.

### Step 2: Go to Streamlit Cloud
Navigate to [share.streamlit.io](https://share.streamlit.io)

### Step 3: Click "New app"
![Create new app](docs/streamlit-new-app.png)

### Step 4: Fill in Details
- **Repository**: `praveenkumar815/nutraceutical-reviewer`
- **Branch**: `main`
- **Main file path**: `app.py`

### Step 5: Deploy
Click **"Deploy"** and wait 1-3 minutes for deployment.

### Step 6: Add Secrets
Once deployed:
1. Click **"Manage"** (top right)
2. Go to **"Secrets"** tab
3. Paste:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
4. Click **"Save"**

### Step 7: Access Your App
Your live URL:
```
https://praveenkumar815-nutraceutical-reviewer.streamlit.app
```

## Test It Works

1. Go to your app URL
2. Enter sample data:
   - Product: "Test Energy"
   - Category: "Energy"
   - Ingredients: "Caffeine - 400mg"
   - Claims: "Guaranteed to work"
3. Click "Analyze Formulation"
4. See results appear!

## Troubleshooting

### "ModuleNotFoundError"
- Ensure all packages from `requirements.txt` installed
- Clear browser cache and reload

### "GOOGLE_API_KEY not found"
- Check Streamlit Cloud secrets are added
- Wait 30 seconds for secrets to sync
- Click reload in app

### "Analysis Error"
- Verify Google API key is valid
- Check [makersuite.google.com](https://makersuite.google.com) for key
- Create new key if needed

## Share Your Link
Your live app is ready to share!

```
💊 Nutraceutical AI Reviewer
https://praveenkumar815-nutraceutical-reviewer.streamlit.app
```

---

**🎉 You're Live! The app is now accessible online.**

For more details, see [DEPLOYMENT.md](DEPLOYMENT.md)
