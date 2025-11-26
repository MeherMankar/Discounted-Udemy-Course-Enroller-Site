# Deployment Guide

## 🚀 Deploy to Render

### Step 1: Prepare Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: udemy-course-enroller
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements_web.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 wsgi:app`
5. Add Environment Variable:
   - **Key**: `SECRET_KEY`
   - **Value**: (generate random string)
6. Click **"Create Web Service"**

### Step 3: Access Your App
- URL: `https://your-app-name.onrender.com`

---

## ⚡ Deploy to Vercel

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Deploy
```bash
vercel
```

### Step 3: Configure
Follow prompts:
- Link to existing project? **No**
- Project name: **udemy-course-enroller**
- Directory: **.**
- Override settings? **No**

### Step 4: Set Environment Variables
```bash
vercel env add SECRET_KEY
```

### Step 5: Production Deploy
```bash
vercel --prod
```

---

## 🔧 Environment Variables

Set these on your hosting platform:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret | `your-random-secret-key-here` |
| `PORT` | Server port (auto-set by host) | `5000` |

---

## 📝 Important Notes

### Render
- ✅ Best for this app (supports WebSockets)
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Persistent storage

### Vercel
- ⚠️ Serverless (may have WebSocket limitations)
- ✅ Fast deployment
- ✅ Free tier available
- ⚠️ Stateless (sessions may not persist)

**Recommendation**: Use **Render** for full functionality with WebSockets.

---

## 🔒 Security

Before deploying:

1. **Change SECRET_KEY**:
   ```python
   # Generate a secure key
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Set Environment Variables** (don't hardcode secrets)

3. **Enable HTTPS** (automatic on Render/Vercel)

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check requirements.txt
pip install -r requirements_web.txt
```

### WebSocket Issues
- Use Render (better WebSocket support)
- Check CORS settings in web_app.py

### Port Issues
- Render/Vercel auto-assign ports
- Don't hardcode port 5000

### Session Issues
- Set SECRET_KEY environment variable
- Check session configuration

---

## 📊 Monitoring

### Render Dashboard
- View logs in real-time
- Monitor resource usage
- Check deployment status

### Vercel Dashboard
- View function logs
- Monitor bandwidth
- Check deployment history

---

## 🔄 Updates

### Update Deployed App
```bash
git add .
git commit -m "Update"
git push
```

Render/Vercel will auto-deploy on push.

---

## 💡 Tips

1. **Use Render** for production (better WebSocket support)
2. **Set environment variables** for secrets
3. **Monitor logs** for errors
4. **Test locally** before deploying
5. **Use HTTPS** always (automatic on both platforms)

---

## 🆘 Support

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- GitHub Issues: Report bugs in your repo

---

**Ready to deploy!** 🎉