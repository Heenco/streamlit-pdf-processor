# Quick API Deployment Guide

## Option 1: Railway (Recommended)

1. **Sign up**: Go to [railway.app](https://railway.app) and create account
2. **Connect GitHub**: Link your GitHub account
3. **Deploy**: 
   - Click "New Project" 
   - Select "Deploy from GitHub repo"
   - Choose your `streamlit-pdf-processor` repository
   - Railway will automatically detect the FastAPI app
4. **Environment**: Set environment variable `PORT` if needed
5. **Domain**: Railway provides a free domain like `your-app.railway.app`

## Option 2: Render

1. **Sign up**: Go to [render.com](https://render.com)
2. **New Web Service**: 
   - Connect GitHub
   - Select repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
3. **Deploy**: Free tier available

## Option 3: ngrok (Temporary/Testing)

```bash
# Install ngrok
# Download from https://ngrok.com/

# Make your local API public
ngrok http 8000
```

This gives you a public URL like: `https://abc123.ngrok.io`

## Option 4: Heroku

```bash
# Install Heroku CLI
# Create app
heroku create your-pdf-api

# Deploy
git push heroku main
```

## Option 5: Fly.io

```bash
# Install flyctl
# Deploy
fly launch
fly deploy
```

## Best Choice: Railway

Railway is the easiest and most reliable for your use case:
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ No credit card required initially
- ✅ Good performance
- ✅ Easy custom domains

Your API will be available at something like:
`https://streamlit-pdf-processor-production.up.railway.app`
