# 🚀 Deploy Modern360 to Render.com - Step by Step Guide

## 📋 Prerequisites Checklist

Before deploying, make sure you have:
- [ ] GitHub account
- [ ] Render.com account (free signup)
- [ ] Google Cloud Console account
- [ ] Gmail account for sending emails

## 🏗️ Step 1: Push to GitHub

### Option A: Create New Repository on GitHub
1. Go to [GitHub.com](https://github.com) and click "New Repository"
2. Name it: `modern360-assessment`
3. Make it **Public** (required for free Render deployment)
4. Don't initialize with README (we already have files)
5. Copy the repository URL

### Option B: Use Existing Repository
If you already have a repository, use that URL.

### Push Your Code
```bash
# Add GitHub remote (replace with your actual repository URL)
git remote add origin https://github.com/YOUR-USERNAME/modern360-assessment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🌐 Step 2: Set Up Google OAuth

### Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project:
   - Project name: "Modern360 Assessment"
   - Click "CREATE"

3. Enable Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click "ENABLE"

4. Create OAuth Credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "CREATE CREDENTIALS" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Name: "Modern360 Web Client"
   - Authorized redirect URIs: `https://your-app-name.onrender.com/auth/callback`
     (You'll update this with actual URL after deployment)

5. **Save these credentials** (you'll need them):
   - Client ID: `123456789.apps.googleusercontent.com`
   - Client Secret: `abc123def456`

## 📧 Step 3: Set Up Gmail for Email Sending

1. **Enable 2-Factor Authentication**:
   - Go to Google Account settings
   - Security > 2-Step Verification
   - Turn it ON

2. **Create App Password**:
   - In Google Account > Security
   - Click "App passwords"
   - Select "Mail" and "Other (Custom name)"
   - Name it: "Modern360 Assessment"
   - **Save the 16-character password**: `abcd efgh ijkl mnop`

## 🚀 Step 4: Deploy to Render.com

### 4.1 Create Render Account
1. Go to [Render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your repositories

### 4.2 Create Web Service
1. Click "New +" > "Web Service"
2. Connect your GitHub repository
3. Select your `modern360-assessment` repository
4. Configure the service:

```
Name: modern360-assessment
Environment: Python 3
Build Command: ./build.sh
Start Command: gunicorn app:app
Plan: Free (or Starter for better performance)
```

### 4.3 Add Environment Variables
In the Render dashboard, add these environment variables:

```bash
# Required Environment Variables
SECRET_KEY=your-super-secret-key-generate-random-32-chars
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**To generate SECRET_KEY**, use this command:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4.4 Add PostgreSQL Database
1. In Render dashboard, click "New +" > "PostgreSQL"
2. Name: `modern360-db`
3. Plan: Free
4. Click "Create Database"
5. Copy the "External Database URL"
6. Add it as environment variable:
   ```
   DATABASE_URL=postgresql://username:password@hostname:port/database
   ```

### 4.5 Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your app will be available at: `https://modern360-assessment-xxxx.onrender.com`

## 🔧 Step 5: Update Google OAuth with Real URL

After deployment:
1. Go back to Google Cloud Console
2. Edit your OAuth client
3. Update "Authorized redirect URIs" with your actual Render URL:
   ```
   https://your-actual-app-name.onrender.com/auth/callback
   ```

## 🎯 Step 6: Test Your Deployment

### Access Your Application
Your Modern360 Assessment Platform will be live at:
```
https://your-app-name.onrender.com
```

### Test Features:
1. ✅ **Landing Page** - Should load with professional design
2. ✅ **Google Login** - Click "Sign in with Google"
3. ✅ **Dashboard** - After login, should show dashboard
4. ✅ **Create Assessment** - Test creating a new assessment
5. ✅ **Send Invitations** - Test email invitation system
6. ✅ **Assessment Response** - Test the assessment form

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check Render logs in dashboard
   - Ensure all files are committed to GitHub
   - Verify `build.sh` is executable

2. **OAuth Error**
   - Verify Google Client ID/Secret are correct
   - Check redirect URI matches exactly
   - Ensure Google+ API is enabled

3. **Email Not Sending**
   - Verify Gmail app password (not regular password)
   - Check 2FA is enabled on Gmail
   - Confirm MAIL_* environment variables

4. **Database Errors**
   - Ensure DATABASE_URL is set correctly
   - Check PostgreSQL database is created

### View Logs:
In Render dashboard > Your Service > "Logs" tab

## 🎉 Success! Your Platform is Live

Once deployed successfully, you'll have:

### 🌐 **Live Web Application**: 
`https://your-app-name.onrender.com`

### ✨ **Features Available**:
- Professional landing page
- Google OAuth authentication
- Assessment creation and management
- Email invitation system
- Real-time dashboard analytics
- Mobile-responsive design
- Secure database storage

### 👥 **Ready for Users**:
- Share the URL with your team
- Create assessments and send invitations
- Collect 360-degree feedback professionally

## 📱 Mobile Access
Your platform works perfectly on:
- Desktop computers
- Tablets
- Mobile phones
- Any modern web browser

## 🔒 Security Features
Your deployment includes:
- HTTPS encryption (automatic with Render)
- Google OAuth security
- Secure session management
- Environment variable protection
- Database security

## 📊 Next Steps
1. Create your first assessment
2. Invite team members
3. Start collecting feedback
4. View analytics and results

Your Modern360 Assessment Platform is now live and ready for professional use! 🚀
