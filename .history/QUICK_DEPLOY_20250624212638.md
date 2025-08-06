# 🎯 QUICK DEPLOY TO YOUR RENDER.COM INSTANCE

## ✅ COMPLETED: Code is on GitHub!
**Repository:** https://github.com/DzenanMuftic/modern360-assessment

---

## 🚀 NOW DO THIS IN RENDER.COM:

### 1. Go to Render.com
- Open: https://render.com
- Sign in with GitHub

### 2. Create Web Service
- Click "New +" → "Web Service"
- Select: **DzenanMuftic/modern360-assessment**
- Settings:
  ```
  Build Command: ./build.sh
  Start Command: gunicorn app:app
  ```

### 3. Add Environment Variables
**Copy & paste these in Render dashboard:**
```
SECRET_KEY=ESxz82k0B7ZDE4CIsM4QABj32NsD3bsw5GnCYBorsFU
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

**YOU NEED TO ADD:**
```
GOOGLE_CLIENT_ID=get-from-google-cloud-console
GOOGLE_CLIENT_SECRET=get-from-google-cloud-console  
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-gmail@gmail.com
```

---

## 🔑 BEFORE DEPLOYING - GET CREDENTIALS:

### Google OAuth (5 minutes):
1. Go to: https://console.cloud.google.com
2. Create project → Enable Google+ API
3. Create OAuth 2.0 credentials
4. Copy Client ID & Secret

### Gmail App Password (2 minutes):
1. Enable 2FA on Gmail
2. Generate App Password
3. Copy 16-character password

---

## 🎉 AFTER DEPLOY:
Your app will be live at: `https://your-app-name.onrender.com`

Update Google OAuth redirect URI with your actual URL.

**That's it! Your Modern360 Assessment Platform will be live! 🚀**

---

## 📖 Detailed Instructions:
See `DEPLOY_TO_RENDER.md` for complete step-by-step guide.
