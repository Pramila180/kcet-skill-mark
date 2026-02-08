# 🚀 Deploy Skill Marks Portal on Render - Step by Step Guide

## 📋 Prerequisites
- GitHub account
- Render account (free tier available)
- Your project files ready

## 🗂️ Step 1: Prepare Your Project

### 1.1 Create .gitignore file
```bash
# Create this file in your project root
__pycache__/
*.pyc
instance/
uploads/
*.db
.env
```

### 1.2 Update app.py for Render
Your app.py is already configured for Render with:
- Environment variables support
- Production-ready configuration
- Proper port handling

## 🐙 Step 2: Push to GitHub

### 2.1 Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name: `skill-marks-portal`
4. Description: `College Skill Marks Management System`
5. Make it Public (Render free tier requires public repos)
6. Click "Create repository"

### 2.2 Push Your Code
```bash
# Open terminal in your project folder
cd "c:/Users/pramila/OneDrive - Kamaraj College of Engineering and Technology/Desktop/fold/skill mark web"

# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for Render deployment"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/skill-marks-portal.git
git branch -M main
git push -u origin main
```

## 🌐 Step 3: Deploy on Render

### 3.1 Create Render Account
1. Go to https://render.com
2. Click "Sign Up"
3. Choose GitHub authentication
4. Authorize Render to access your GitHub

### 3.2 Create New Web Service
1. After login, click "New +"
2. Select "Web Service"
3. Choose "Connect a repository"
4. Find and select `skill-marks-portal`
5. Click "Connect"

### 3.3 Configure Web Service
```
Name: skill-marks-portal
Region: Choose nearest (e.g., Oregon)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 3.4 Advanced Settings
1. Click "Advanced" tab
2. Add Environment Variables:
   ```
   SECRET_KEY=your-very-long-random-secret-key-here
   FLASK_ENV=production
   ```

### 3.5 Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-5 minutes)
3. Your app will be live at: `https://skill-marks-portal.onrender.com`

## 🔧 Step 4: Post-Deployment Setup

### 4.1 Test Your App
- Visit your Render URL
- Test student login: `24UCS001` / `24ucs001`
- Test admin login: `facultycse` / `facultycse123`

### 4.2 Handle Database
Render uses PostgreSQL automatically:
- Your SQLite will be replaced by PostgreSQL
- Database will be created automatically
- All tables will be created on first run

### 4.3 File Uploads
Render's filesystem is ephemeral:
- For production, consider cloud storage (AWS S3, Cloudinary)
- For now, uploads work but reset on redeploy

## 🛠️ Step 5: Troubleshooting

### Common Issues & Solutions:

#### Issue 1: Build Failed
**Solution**: Check requirements.txt
```bash
# Make sure these are in requirements.txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
gunicorn==21.2.0
Werkzeug==2.3.7
```

#### Issue 2: Application Error
**Solution**: Check logs in Render dashboard
- Go to your service → Logs tab
- Look for specific error messages

#### Issue 3: Database Connection Error
**Solution**: Wait for full deployment
- PostgreSQL needs time to initialize
- Try accessing after 5 minutes

#### Issue 4: 404 Not Found
**Solution**: Check start command
- Should be: `gunicorn app:app`
- Not: `python app.py`

#### Issue 5: Uploads Not Working
**Solution**: Check file permissions
- Render creates uploads folder automatically
- May need to handle file storage differently

## 🔄 Step 6: Updates and Maintenance

### Updating Your App
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render auto-deploys on push to main branch
```

### Monitoring
- Check Render dashboard for logs
- Monitor usage on free tier (750 hours/month)
- Set up alerts if needed

## 📱 Step 7: Share Your App

### Your Live App URL
Once deployed, your app will be accessible at:
`https://skill-marks-portal.onrender.com`

### Student Access
- Share this URL with students
- They can login and upload certificates
- Admin can approve via `/admin` route

## 🎯 Success Checklist

✅ GitHub repository created and pushed
✅ Render web service configured
✅ Environment variables set
✅ Application deployed successfully
✅ Student login working
✅ Admin login working
✅ Certificate upload working
✅ Admin approval working

## 📞 Support

If you encounter issues:
1. Check Render logs first
2. Verify environment variables
3. Ensure all requirements are installed
4. Check your GitHub repository is public

---

**🎉 Your Skill Marks Portal is now live on Render!**
