# Quick Deploy Guide

## 🚀 One-Click Deploy

### Deploy to Render (Recommended)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Sign in to Render
3. Click "Create Web Service"
4. Wait for deployment (5-10 minutes)
5. Access your app at the provided URL

### Deploy to Vercel
```bash
npm i -g vercel
vercel
```

---

## 📋 Quick Setup

### 1. Clone Repository
```bash
git clone YOUR_REPO_URL
cd Discounted-Udemy-Course-Enroller
```

### 2. Install Dependencies
```bash
pip install -r requirements_web.txt
```

### 3. Test Locally
```bash
python web_app.py
```
Open: http://localhost:5000

### 4. Deploy
Choose your platform:
- **Render**: Push to GitHub, connect repo on Render
- **Vercel**: Run `vercel` command
- **Heroku**: `git push heroku main`

---

## 🔑 Environment Variables

Set on your hosting platform:

```
SECRET_KEY=your-random-secret-key-here
```

Generate secure key:
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📦 Files for Deployment

- ✅ `web_app.py` - Main application
- ✅ `wsgi.py` - WSGI entry point
- ✅ `requirements_web.txt` - Dependencies
- ✅ `Procfile` - Render/Heroku config
- ✅ `vercel.json` - Vercel config
- ✅ `render.yaml` - Render blueprint
- ✅ `runtime.txt` - Python version

---

## 🎯 Platform Comparison

| Feature | Render | Vercel | Heroku |
|---------|--------|--------|--------|
| WebSockets | ✅ Yes | ⚠️ Limited | ✅ Yes |
| Free Tier | ✅ Yes | ✅ Yes | ✅ Yes |
| Auto Deploy | ✅ Yes | ✅ Yes | ✅ Yes |
| HTTPS | ✅ Auto | ✅ Auto | ✅ Auto |
| **Best For** | **This App** | Static/API | Full Apps |

**Recommendation**: Use **Render** for best compatibility.

---

## ✅ Deployment Checklist

- [ ] Push code to GitHub
- [ ] Set SECRET_KEY environment variable
- [ ] Configure build command
- [ ] Configure start command
- [ ] Test deployment
- [ ] Access app URL

---

## 🔧 Commands

### Render
```bash
# Build Command
pip install -r requirements_web.txt

# Start Command
gunicorn --worker-class eventlet -w 1 wsgi:app
```

### Vercel
```bash
vercel --prod
```

### Local Testing
```bash
python web_app.py
```

---

## 📱 Access Your App

After deployment:
- **Render**: `https://your-app.onrender.com`
- **Vercel**: `https://your-app.vercel.app`
- **Heroku**: `https://your-app.herokuapp.com`

---

## 🆘 Need Help?

See detailed guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Deploy in 5 minutes!** 🎉