# 🚀 Deployment Guide - Streamlit Cloud

This guide shows how to deploy the Nutraceutical Formulation AI Reviewer on Streamlit Cloud.

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Repository pushed to GitHub

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your GitHub repository contains:
```
nutraceutical-reviewer/
├── app.py
├── ingredient_database.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env (with dummy values - secrets will be on Streamlit Cloud)
└── .streamlit/
    ├── config.toml
    └── secrets_template.toml
```

Push to GitHub:
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"** button
3. Connect your GitHub account if prompted
4. Fill in deployment details:
   - **Repository**: `praveenkumar815/nutraceutical-reviewer`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy"**

The app will deploy in 1-3 minutes. You'll get a unique URL:
```
https://yourusername-nutraceutical-reviewer.streamlit.app
```

### 3. Configure Secrets

After deployment:

1. Click **"Manage app"** in the top right
2. Go to **"Secrets"** tab
3. Paste your secret in TOML format:
   ```toml
   GOOGLE_API_KEY = "your_actual_google_api_key_here"
   ```
4. Click **"Save"**
5. App automatically restarts

## Accessing Secrets in App

The app automatically reads from `.streamlit/secrets.toml` locally or Streamlit Cloud secrets:

```python
import streamlit as st

api_key = st.secrets["GOOGLE_API_KEY"]
```

## Troubleshooting Deployment

### "App deploy failed"
- Check that `requirements.txt` has all dependencies
- Verify `app.py` is in the root directory
- Ensure no syntax errors in Python files

### "ModuleNotFoundError"
- Add missing packages to `requirements.txt`
- Redeploy after updating requirements

### "GOOGLE_API_KEY not found"
- Verify secrets are set in Streamlit Cloud dashboard
- Check the exact secret name matches: `GOOGLE_API_KEY`
- Wait a moment and refresh - secrets take a few seconds to apply

### "Vector DB Error"
- Normal on first run - database creates automatically
- Complete an analysis to populate the database
- Error persists? Check disk space on server

### Performance Issues
- Use smaller embedding models
- Limit vector search results (currently k=5)
- Cache responses when possible

## Environment Variables

The app uses `.env` for local development:
```env
GOOGLE_API_KEY=your_key_here
```

On Streamlit Cloud, set via **Secrets** dashboard (not .env).

## Auto-Redeployment

To redeploy with code changes:

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. Streamlit Cloud auto-deploys within a few minutes

Or manually redeploy from Streamlit Cloud dashboard.

## Production Checklist

Before going live:
- [ ] Google API key set in Streamlit Cloud secrets
- [ ] README has clear usage instructions
- [ ] Error messages are user-friendly
- [ ] .gitignore prevents API key leaks
- [ ] requirements.txt is complete and pinned
- [ ] App runs locally without errors
- [ ] Tested with sample inputs

## Monitoring & Updates

Access your deployed app:
- **View App**: Click the URL in Streamlit dashboard
- **View Logs**: Click "Manage" → "View logs"
- **Edit Settings**: Click "Manage" → "Settings"
- **Stop App**: Click "Manage" → "Delete app"

## Performance Optimization

For better performance:

1. **Cache Resources**:
   ```python
   @st.cache_resource
   def init_ai_components():
       # Initialize once, reuse for all sessions
   ```

2. **Lazy Loading**:
   - Load embeddings only when needed
   - Initialize vector DB on first use

3. **Limits**:
   - Max file size: 200MB (configured in config.toml)
   - Request timeout: 30 seconds
   - Memory: ~1GB per app

## Security Best Practices

✅ **Do:**
- Store API keys in Streamlit Cloud secrets
- Use `.env` only for local development
- Never commit `.env` to GitHub
- Validate all user inputs
- Use HTTPS (automatic on Streamlit Cloud)

❌ **Don't:**
- Put API keys in code
- Share secrets in GitHub issues
- Store sensitive data locally
- Use hardcoded credentials

## Cost Estimation

Streamlit Cloud pricing:
- **Free tier**: 1 app, always on, limited resources
- **Pro tier**: ~$20/month, multiple apps, more resources

For this app with free tier:
- Small daily usage: ✅ Free
- Moderate daily usage: ✅ Free
- Heavy daily usage: Consider Pro tier

Google API costs depend on usage:
- Embeddings: $0.02-0.1 per 1M tokens
- LLM: $0.075-0.6 per 1M input tokens
- Check [Google pricing](https://ai.google.dev/pricing)

## Custom Domain

To use a custom domain (Pro feature):
1. Go to Streamlit Cloud app settings
2. Under "Linked apps", add your domain
3. Point DNS to Streamlit Cloud
4. Verify and enable HTTPS

## Support & Help

- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Community](https://discuss.streamlit.io)
- [Google API Docs](https://ai.google.dev/docs)
- GitHub Issues for this project

---

**Happy Deploying! 🎉**
