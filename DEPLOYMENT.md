# Deployment Guide for Overwatch Comparison App

## Option 1: Vercel (Easiest for beginners)

### Frontend (React) on Vercel:
1. Push your code to GitHub
2. Connect GitHub repo to Vercel
3. Set build command: `cd frontend && npm run build`
4. Set output directory: `frontend/build`
5. Add custom domain in Vercel dashboard

### Backend options for Vercel:
- **Option A**: Convert Django to Vercel serverless functions
- **Option B**: Deploy backend separately (see other options below)

## Option 2: DigitalOcean App Platform (Full-stack)

### Setup:
1. Create DigitalOcean account
2. Create new App
3. Connect GitHub repository
4. Configure components:
   - **Web Service** (Frontend): 
     - Build: `cd frontend && npm run build`
     - Run: `cd frontend && npx serve -s build -l 3000`
   - **Web Service** (Backend):
     - Build: `cd backend && pip install -r requirements.txt`
     - Run: `cd backend && python manage.py runserver 0.0.0.0:8000`

### Custom Domain:
1. Go to Settings > Domains
2. Add your domain
3. Update DNS records with your domain provider

## Option 3: VPS with Docker (Most control)

### Prerequisites:
- VPS with Ubuntu/Debian
- Docker and Docker Compose installed
- Domain pointing to server IP

### Deployment steps:
```bash
# 1. Clone repository on server
git clone <your-repo-url>
cd overwatch-compare

# 2. Update docker-compose.yml with your domain
# Edit ALLOWED_HOSTS to include your domain

# 3. Build and run
docker-compose up -d

# 4. Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Option 4: Netlify + Railway

### Frontend (Netlify):
1. Connect GitHub repo to Netlify
2. Set build settings:
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/build`
3. Add custom domain in Netlify

### Backend (Railway):
1. Connect GitHub repo to Railway
2. Add environment variables:
   - `DJANGO_SETTINGS_MODULE=overwatch_api.settings`
   - `ALLOWED_HOSTS=*`
3. Railway will auto-deploy Django app

## Domain Setup (General)

### 1. Purchase Domain:
- Namecheap, GoDaddy, Google Domains, etc.

### 2. DNS Configuration:
```
Type    Name    Value
A       @       <your-server-ip>
A       www     <your-server-ip>
```

### 3. SSL Certificate:
- Most platforms provide free SSL automatically
- For VPS: Use Let's Encrypt (certbot)

## Environment Variables for Production

### Backend (.env file):
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Frontend (build time):
```
REACT_APP_API_URL=https://yourdomain.com/api
```

## Cost Estimates:

- **Vercel**: Free tier (hobby projects)
- **Netlify + Railway**: Free tier available
- **DigitalOcean App Platform**: $5-12/month
- **VPS**: $5-20/month + domain (~$10-15/year)

## Recommended for Your App:
1. **Beginner**: Vercel (frontend) + Railway (backend)
2. **Intermediate**: DigitalOcean App Platform
3. **Advanced**: VPS with Docker

Choose based on your budget, technical expertise, and scaling needs.
