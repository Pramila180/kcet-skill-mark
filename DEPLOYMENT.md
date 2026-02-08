# 🌐 Deployment Guide - Skill Marks Portal

## 🚀 Quick Deployment Options

### Option 1: Render (Recommended - Free)
1. **Create account**: https://render.com/
2. **Connect GitHub**: Upload your code to GitHub
3. **New Web Service**: 
   - Choose "Web Service"
   - Connect your GitHub repo
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. **Environment Variables**:
   - `SECRET_KEY`: Generate a random secret key
   - `FLASK_ENV`: production

### Option 2: PythonAnywhere (Free Tier)
1. **Sign up**: https://www.pythonanywhere.com/
2. **Create Web App**:
   - Python version: 3.9+
   - Framework: Flask
   - Upload your files
3. **Install requirements**: `pip install -r requirements.txt`
4. **Configure WSGI**: Update the WSGI file

### Option 3: Heroku (Free Tier Available)
1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: 
   ```bash
   git init
   git add .
   git commit -m "Initial deploy"
   heroku git:remote -a your-app-name
   git push heroku main
   ```

## 🔧 Production Setup

### Environment Variables
```bash
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
FLASK_ENV=production
HOST=0.0.0.0
PORT=5000
```

### Database Setup
- **Local**: SQLite (already configured)
- **Production**: PostgreSQL recommended
- **Free PostgreSQL**: 
  - ElephantSQL (free tier)
  - Supabase (free tier)

### File Storage
- **Local**: `/uploads` folder (current setup)
- **Cloud**: AWS S3, Google Cloud Storage, or Cloudinary for production

## 🌍 Static IP Solutions

### Option A: Cloud Hosting (Recommended)
- **Render**: Provides static URL
- **PythonAnywhere**: Static subdomain
- **Heroku**: Static appname.herokuapp.com

### Option B: Static IP Services
- **AWS EC2**: Elastic IP
- **DigitalOcean**: Floating IP
- **Vultr**: Static IP

### Option C: Domain + DNS
1. **Buy domain**: GoDaddy, Namecheap
2. **DNS pointing**: Point to your server
3. **SSL certificate**: Let's Encrypt (free)

## 📱 Mobile Access

Once deployed, your app will be accessible from:
- **Any device** with internet
- **Mobile phones**
- **Tablets**
- **Other computers**

## 🔐 Security Considerations

1. **Change SECRET_KEY**: Generate a new one for production
2. **HTTPS**: Enable SSL certificate
3. **Database security**: Use environment variables
4. **File upload limits**: Already configured (16MB)
5. **Input validation**: Already implemented

## 🚀 Quick Start with Render

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/skill-marks-portal.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com/
   - Click "New Web Service"
   - Connect GitHub
   - Select your repo
   - Deploy!

Your app will be live at: `https://your-app-name.onrender.com`

## 📞 Support

For deployment issues:
- Check logs on your hosting platform
- Verify environment variables
- Ensure all requirements are installed
