# Quick Hosting Guide - Overwatch Comparison App

## 🚀 **Single Deployment Strategy** (Frontend + Backend Together)

Your app now uses a **unified deployment approach** where Django serves both the API and the React frontend from a single service. This is simpler, cheaper, and easier to manage!

### Option 1: Railway (FREE) - Recommended for beginners
**Best for**: Free hosting, automatic deployments

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Single deployment setup"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - "Deploy from GitHub" → Select your repository
   - Railway will automatically use the `build.sh` script
   - No additional configuration needed!

3. **Set Environment Variables in Railway:**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=*.railway.app,yourdomain.com
   ```

4. **Done!** Railway runs the build script, installs everything, and serves from one URL.

**Note**: If you see "executable `cd` could not be found" error, that's fixed now with the `build.sh` script approach.

---

### Option 2: DigitalOcean App Platform ($5/month) - Best for production
**Best for**: Professional hosting, custom domains

1. **Create App:**
   - Go to [digitalocean.com](https://digitalocean.com) → App Platform
   - "Create App" → Import from GitHub
   - Select your repository

2. **Configuration (auto-detected):**
   - **Build Command**: `cd frontend && npm run build && cd ../backend && pip install -r requirements.txt`
   - **Run Command**: `cd backend && python manage.py runserver 0.0.0.0:8080`

3. **Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=${APP_DOMAIN}
   CORS_ALLOWED_ORIGINS=https://${APP_DOMAIN}
   ```

---

### Option 3: Render (FREE) - Good free tier
**Best for**: Free hosting with good performance

1. **Web Service Setup:**
   - Go to [render.com](https://render.com)
   - "New Web Service" → Connect GitHub
   - **Build Command**: `cd frontend && npm run build && cd ../backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python manage.py runserver 0.0.0.0:$PORT`

2. **Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ```

---

## � Local Development & Testing

### Test the deployment locally:
```bash
# Option 1: Use the unified build script
python3 build_unified.py

# Option 2: Use Docker (exactly like production)
./deploy.sh development

# Option 3: Manual build and run
cd frontend && npm run build && cd ../backend && python manage.py runserver
```

All three methods serve your app at: **http://localhost:8000**

---

## 🎯 **How It Works:**

1. **React builds** to static files in `frontend/build/`
2. **Django serves** the React app at the root URL (`/`)
3. **API requests** go to `/api/` (same domain, no CORS issues)
4. **Single deployment** handles everything
5. **One URL** for your entire app

---

## 💰 Cost Comparison

| Platform | Cost | Setup Time | Best For |
|----------|------|------------|----------|
| **Railway** | FREE* | 2 min | Beginners, testing |
| **Render** | FREE* | 5 min | Small projects |
| **DigitalOcean** | $5/mo | 10 min | Production apps |

*Free tiers have usage limits but perfect for personal projects

---

## 🚨 Quick Deployment Checklist

- [ ] Test locally: `python3 build_unified.py`
- [ ] Code pushed to GitHub
- [ ] Platform account created (Railway/Render/DigitalOcean)
- [ ] Repository connected to platform
- [ ] Environment variables set
- [ ] Custom domain added (optional)
- [ ] Test: Your app loads at the deployed URL

---

## 📁 **What Changed (Simplified):**

- ✅ **Single Dockerfile** instead of separate frontend/backend
- ✅ **Django serves React** at the root URL
- ✅ **One docker-compose.yml** for everything
- ✅ **Simpler deploy script** 
- ✅ **Railway/Render configs** work out of the box
- ❌ **No nginx needed** (Django handles static files)
- ❌ **No complex routing** (everything through Django)

---

## 📞 Support

If you get stuck:
1. Check platform documentation (Vercel, Railway, DigitalOcean)
2. Verify environment variables are set correctly
3. Check DNS propagation: [whatsmydns.net](https://whatsmydns.net)
4. Test API endpoints directly: `https://yourdomain.com/api/heroes/`

**Most common issues:**
- CORS errors → Check `CORS_ALLOWED_ORIGINS`
- 404 errors → Check `ALLOWED_HOSTS` in Django
- Build failures → Check environment variables and build commands
