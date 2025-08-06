# 🚀 DEPLOY YOUR MODERN360 PLATFORM TO RENDER.COM

## ✅ STEP 1: CODE IS READY ON GITHUB!
Your repository is live at: **https://github.com/DzenanMuftic/modern360-assessment**

---

## 🌐 STEP 2: DEPLOY TO RENDER.COM

### **A. Go to Render.com**
1. Open: **https://render.com**
2. Click **"Get Started for Free"** or **"Sign In"**
3. **Sign up/Login with GitHub** (recommended)

### **B. Create New Web Service**
1. Click **"New +"** button
2. Select **"Web Service"**
3. Click **"Connect account"** to connect GitHub
4. Find and select: **DzenanMuftic/modern360-assessment**
5. Click **"Connect"**

### **C. Configure the Service**
```
Name: modern360-assessment
Environment: Python 3
Region: Oregon (US West) or closest to you
Branch: main
Build Command: ./build.sh
Start Command: gunicorn app:app
Plan: Free (for testing) or Starter ($7/month for better performance)
```

---

## 🔧 STEP 3: CONFIGURE ENVIRONMENT VARIABLES

In the Render dashboard, scroll down to **"Environment Variables"** and add these:

### **Required Variables:**
```bash
SECRET_KEY=your-secret-key-32-random-characters
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### **Generate SECRET_KEY:**
Run this command to generate a secure secret key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔑 STEP 4: SET UP GOOGLE OAUTH (REQUIRED)

### **A. Google Cloud Console Setup**
1. Go to: **https://console.cloud.google.com/**
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
   - **Authorized redirect URIs:** (Add this AFTER deployment)
     ```
     https://your-app-name.onrender.com/auth/callback
     ```

5. **Save these credentials:**
   - Client ID: `123456789.apps.googleusercontent.com`
   - Client Secret: `abc123def456`

---

## 📧 STEP 5: SET UP GMAIL FOR EMAILS

### **A. Enable 2-Factor Authentication**
1. Go to Google Account settings
2. Security > 2-Step Verification
3. Turn it ON

### **B. Create App Password**
1. In Google Account > Security
2. Click "App passwords"
3. Select "Mail" and "Other (Custom name)"
4. Name it: "Modern360 Assessment"
5. **Save the 16-character password:** `abcd efgh ijkl mnop`

---

## 🚀 STEP 6: DEPLOY!

1. **Add all environment variables** in Render
2. Click **"Create Web Service"**
3. **Wait 5-10 minutes** for deployment
4. Your app will be live at: `https://modern360-assessment-xxxx.onrender.com`

---

## 🔧 STEP 7: FINAL CONFIGURATION

### **A. Update Google OAuth**
After deployment:
1. Copy your actual Render URL
2. Go back to Google Cloud Console
3. Edit your OAuth client
4. Update "Authorized redirect URIs" with:
   ```
   https://your-actual-app-name.onrender.com/auth/callback
   ```

### **B. Add Database (Optional for Production)**
1. In Render dashboard: "New +" > "PostgreSQL"
2. Name: `modern360-db`
3. Plan: Free
4. Copy the "External Database URL"
5. Add as environment variable: `DATABASE_URL=postgresql://...`

---

## 🎉 SUCCESS! YOUR PLATFORM IS LIVE!

### **Your Live URL:**
```
https://your-app-name.onrender.com
```

### **Test Your Platform:**
✅ Landing page loads  
✅ "Sign in with Google" works  
✅ Dashboard appears after login  
✅ Create assessment works  
✅ Email invitations work  
✅ Mobile responsive  

---

## 🔍 TROUBLESHOOTING

### **If Build Fails:**
- Check Render logs in dashboard
- Ensure all environment variables are set

### **If OAuth Doesn't Work:**
- Verify Google Client ID/Secret
- Check redirect URI matches exactly
- Ensure Google+ API is enabled

### **If Emails Don't Send:**
- Use Gmail App Password (not regular password)
- Verify 2FA is enabled on Gmail

---

## 📞 NEED HELP?

Check the logs in your Render dashboard for any errors. The deployment usually takes 5-10 minutes.

**Your Modern360 Assessment Platform is ready to go live! 🚀**
