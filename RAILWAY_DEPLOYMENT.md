# 🚂 Railway Deployment Guide

## 🎯 Deployment URL
```
https://youtube458-production.up.railway.app
```

## 📋 Prerequisites

1. **Railway Account** - Sign up at https://railway.app
2. **GitHub Repository** - Push your code to GitHub
3. **Environment Variables** - All credentials ready:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `YOUTUBE_API_KEY`
   - `WEB_UI_SECRET`
   - `ENVIRONMENT=production`

---

## 🚀 5-Minute Deployment

### Step 1: Prepare GitHub Repository
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: YouTube Channel Monitor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Youtube458.git
git push -u origin main
```

### Step 2: Connect to Railway

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub"**
4. Connect your GitHub account
5. Select **Youtube458** repository
6. Railway will auto-detect the `Dockerfile` and deploy

### Step 3: Set Environment Variables

In Railway Dashboard:
1. Go to **Variables** tab
2. Add all variables:
   ```
   ENVIRONMENT=production
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
   YOUTUBE_API_KEY=your_api_key
   WEB_UI_SECRET=your_strong_password
   FLASK_PORT=5000
   FLASK_HOST=0.0.0.0
   ```

### Step 4: Deploy

Click **"Deploy"** - Railway will:
- Build the Docker image
- Start the Flask app on port 5000
- Generate the domain: `youtube458-production.up.railway.app`

### Step 5: Access Your App

```
Web Dashboard: https://youtube458-production.up.railway.app
Login with your WEB_UI_SECRET password
```

---

## 🔧 Configuration Files Created

### 📄 Dockerfile
- Uses Python 3.11 slim image
- Installs all dependencies
- Includes health check
- Optimized for production

### 📄 railway.json
- Specifies build configuration
- Sets deployment start command
- Configures restart policy

### 📄 Procfile
- Defines web and bot processes
- Used by Railway for multi-process apps

---

## 🤖 Running Bot & Web Simultaneously

### Option A: Single Service (Recommended)
```bash
# Deploy only the web app via Railway
# The Procfile shows bot command, but Railway will run the main CMD from Dockerfile
```

### Option B: Multiple Services
To run both bot and web in Railway:

1. Create 2 services in Railway Dashboard
2. Service 1 (Web):
   - Start Command: `python app.py`
   - Port: 5000

3. Service 2 (Bot):
   - Start Command: `python bot.py`
   - No port needed

---

## 📊 Monitoring & Logs

### View Logs in Railway Dashboard:
```
Dashboard → Deployments → View Logs
```

### Common Log Messages:
```
✅ "Running on http://0.0.0.0:5000"  - Web server started
✅ "Checking channel status..."        - Bot processing
⚠️  "Host validation: ..."             - Domain check
❌ "Error checking status:"            - YouTube API issue
```

---

## 🔐 Domain Configuration

### Default Railway Domain:
```
https://youtube458-production.up.railway.app
```

### Add Custom Domain (Optional):

1. In Railway Dashboard → Settings
2. Custom Domain
3. Add your domain (e.g., youtube.yourdomain.com)
4. Update DNS records as instructed
5. Set `CUSTOM_DOMAINS=youtube.yourdomain.com` in Environment

### SSL/TLS:
- ✅ Automatically enabled for Railway domains
- ✅ Automatic renewal
- ✅ HTTPS redirect enabled in production

---

## 🚨 Troubleshooting

### App Won't Start
```
Error: "Address already in use"
→ Railway manages ports automatically, delete channels.db and restart

Error: "ModuleNotFoundError"
→ Check if all dependencies in requirements.txt are listed
→ Run: pip install -r requirements.txt locally to verify
```

### Bot Not Responding
```
Problem: Telegram commands not working
Solution:
1. Verify TELEGRAM_BOT_TOKEN is correct
2. Check TELEGRAM_CHAT_ID exists
3. View logs in Railway Dashboard
4. Restart the deployment
```

### YouTube API Errors
```
Error: "Invalid API key" or "Quota exceeded"
Solution:
1. Verify YOUTUBE_API_KEY is correct
2. Check quota in Google Cloud Console: 
   https://console.cloud.google.com/
3. Increase quota limit if needed
```

### Database Lock Issues
```
Error: "database is locked"
Solution:
1. Delete channels.db (Railway storage is temporary)
2. Restart the deployment
3. Database will be recreated automatically
```

---

## 🆚 Local vs Production

| Feature | Local | Production |
|---------|-------|-----------|
| Debug Mode | ✅ On | ❌ Off |
| Security Headers | ❌ No | ✅ Yes |
| HTTPS | ❌ No | ✅ Yes |
| Domain | localhost:5000 | youtube458-production.up.railway.app |
| Database Storage | Local file | Railway's persistent storage |
| Logs | Console output | Railway Dashboard |

---

## 📝 Environment Variables

```env
# Production
ENVIRONMENT=production

# Telegram
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx

# YouTube
YOUTUBE_API_KEY=xxx

# Flask
FLASK_PORT=5000
FLASK_HOST=0.0.0.0

# Security
WEB_UI_SECRET=change-me

# Optional
CUSTOM_DOMAINS=yourdomain.com
```

---

## 🔄 Deployment Workflow

### Update Your App:
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
```

### Railway Auto-Deploys:
1. GitHub webhook triggered
2. Docker image rebuilt
3. Old service stopped
4. New service started
5. Available at URL within ~2-3 minutes

---

## 📊 Railway Pricing

**Free Tier Includes:**
- ✅ 5 team members
- ✅ $5 credit/month
- ✅ Shared PostgreSQL database
- ✅ File storage
- ✅ Unlimited deploys

**Cost Estimate (Typical):**
- Web service (5-10GB): ~$0/month (within free tier)
- Bot service: $0/month (minimal resources)
- Database: Included

---

## 🛠️ Advanced Configuration

### Custom Start Script:
Create `start.sh` for multi-process:
```bash
#!/bin/bash
python app.py &
python bot.py
```

Then in `Procfile`:
```
web: bash start.sh
```

### Enable Persistence:
Railway provides `/data` directory:
```python
import os
db_path = os.getenv('DB_PATH', '/data/channels.db')
```

---

## 📞 Support

- **Railway Docs**: https://docs.railway.app
- **Community**: https://railway.app/discord
- **Status Page**: https://status.railway.app

---

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] All environment variables set in Railway
- [ ] TELEGRAM_BOT_TOKEN verified (from BotFather)
- [ ] TELEGRAM_CHAT_ID verified
- [ ] YOUTUBE_API_KEY verified (quota available)
- [ ] WEB_UI_SECRET set to strong password
- [ ] Dockerfile builds successfully
- [ ] Test web dashboard: https://youtube458-production.up.railway.app
- [ ] Test bot: /status command in Telegram
- [ ] Check logs in Railway Dashboard

---

🎉 **You're live!** Your YouTube Channel Monitor is now running on Railway! 🚀
