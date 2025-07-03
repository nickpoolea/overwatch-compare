# Quick Hosting Guide - Overwatch Comparison App

## 🚀 **BEST OPTION: Single Platform Hosting** (Recommended)

### Option 1: DigitalOcean App Platform ($5/month) - FULL STACK
**Best for**: Everything in one place, super simple

1. **One-Click Deployment:**
   ```bash
   # Push to GitHub first
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create App on DigitalOcean:**
   - Go to [digitalocean.com](https://digitalocean.com) → App Platform
   - Click "Create App" → Import from GitHub
   - Select your repository
   - DigitalOcean will auto-detect both React and Django!

3. **Auto Configuration:**
   - **Frontend**: Automatically detected from `frontend/` folder
   - **Backend**: Automatically detected from `backend/` folder
   - **Domain**: Add your custom domain in one click
   - **SSL**: Automatically provided for free

4. **Set Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=${APP_DOMAIN}
   CORS_ALLOWED_ORIGINS=https://${APP_DOMAIN}
   ```

5. **Deploy:** Click "Create Resources" - Done! 🎉

---

### Option 2: Railway (FREE/Cheap) - FULL STACK
**Best for**: Free hosting, simple setup

1. **Deploy Both Together:**
   - Go to [railway.app](https://railway.app)
   - "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects monorepo structure

2. **Configuration:**
   - **Root Directory**: Leave empty (Railway handles both)
   - **Build Command**: `cd frontend && npm run build && cd ../backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python manage.py runserver 0.0.0.0:$PORT`

3. **Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=*.railway.app,yourdomain.com
   PORT=8000
   ```

---

### Option 3: Render (FREE) - FULL STACK
### Option 3: Render (FREE) - FULL STACK
**Best for**: Free hosting with databases

1. **Web Service Setup:**
   - Go to [render.com](https://render.com)
   - "New Web Service" → Connect GitHub
   - **Build Command**: `cd frontend && npm run build && cd ../backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python manage.py runserver 0.0.0.0:$PORT`

2. **Static Site for Frontend:**
   - Create second service: "Static Site"
   - **Build Command**: `cd frontend && npm run build`
   - **Publish Directory**: `frontend/build`

---

## 🔧 **Alternative: Split Hosting Options**

### Vercel + Railway (If you prefer separate services)
1. **Frontend on Vercel** - Great for React apps
2. **Backend on Railway** - Great for Django APIs
3. **Connect them** with environment variables

---

## 🛠 VPS Deployment (Advanced)

### Prerequisites:
- Ubuntu/Debian VPS (DigitalOcean, Linode, AWS EC2)
- Domain name pointing to server IP

### Quick Setup:
```bash
# On your server
git clone https://github.com/yourusername/overwatch-compare.git
cd overwatch-compare

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy with custom domain
./deploy.sh production

# Setup SSL (replace yourdomain.com)
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 🔧 Environment Variables

### Required for Production:

**Backend (.env):**
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Frontend (.env.production):**
```
REACT_APP_API_URL=https://yourdomain.com/api
GENERATE_SOURCEMAP=false
```

---

## 🌐 DNS Setup

After deploying, update your domain's DNS:

```
Type    Name    Value                          TTL
A       @       YOUR_SERVER_IP                 300
A       www     YOUR_SERVER_IP                 300
CNAME   *       yourdomain.com                 300
```

For CDN/hosting platforms:
```
CNAME   @       your-app.vercel.app           300
CNAME   www     your-app.vercel.app           300
```

---

## 💰 Cost Comparison - SINGLE PLATFORM HOSTING

| Platform | Cost | Setup Time | Pros | Best For |
|----------|------|------------|------|----------|
| **Railway** | FREE* | 5 min | Auto-deploy, simple | Beginners |
| **Render** | FREE* | 5 min | Great free tier | Small projects |
| **DigitalOcean** | $5/mo | 10 min | Professional, scalable | Production |
| **Heroku** | $7/mo | 10 min | Classic PaaS | Traditional apps |

*Free tiers have limitations but perfect for testing

---

## 🚀 **SUPER SIMPLE: One-Command Local Test**

Want to test single-platform hosting locally?

```bash
# Build everything and serve from Django
python3 build_unified.py
```

This builds React and serves it through Django - exactly like production!

---

## 🚨 Quick Deployment Checklist - SINGLE PLATFORM

- [ ] Run `python3 build_unified.py` locally to test
- [ ] Code pushed to GitHub
- [ ] Choose platform (Railway/Render for free, DigitalOcean for production)
- [ ] Environment variables configured
- [ ] Domain purchased and DNS configured (optional)
- [ ] Test: `https://yourdomain.com/api/heroes/` should work
- [ ] Test: `https://yourdomain.com/` should show your React app

## 🎯 **Why Single Platform is Better:**

✅ **Simpler**: One deployment instead of two  
✅ **Cheaper**: No separate hosting costs  
✅ **Faster**: No cross-origin requests  
✅ **Easier**: One domain, one SSL certificate  
✅ **Better SEO**: Single domain authority  

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
