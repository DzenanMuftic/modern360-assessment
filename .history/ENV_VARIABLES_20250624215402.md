# ✅ ENVIRONMENT VARIABLES FOR RENDER.COM

## ALREADY SET ✅
SECRET_KEY=ESxz82k0B7ZDE4CIsM4QABj32NsD3bsw5GnCYBorsFU
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

## STILL NEEDED 📝

### EMAIL CONFIGURATION (Required for sending invitations)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

### GOOGLE OAUTH (Required for login)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

---

## 🔧 HOW TO GET THE MISSING VARIABLES:

### 1. GMAIL APP PASSWORD (2 minutes)
1. Go to Google Account Settings
2. Security → 2-Step Verification (enable if not enabled)
3. Security → App passwords
4. Generate password for "Modern360"
5. Copy the 16-character password (like: abcd efgh ijkl mnop)

### 2. GOOGLE OAUTH CREDENTIALS (5 minutes)
1. Go to: https://console.cloud.google.com
2. Create new project: "Modern360 Assessment"
3. APIs & Services → Library → Enable "Google+ API"
4. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client IDs
5. Application type: Web application
6. Authorized redirect URIs: https://your-app-name.onrender.com/auth/callback
7. Copy Client ID and Client Secret

---

## 📋 COMPLETE ENVIRONMENT VARIABLES LIST:

Copy these to your Render dashboard (replace with your actual values):

```
SECRET_KEY=ESxz82k0B7ZDE4CIsM4QABj32NsD3bsw5GnCYBorsFU
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

---

## 🚀 DEPLOYMENT STATUS:

✅ Code pushed to GitHub
✅ Basic environment variables set
📝 Need Gmail App Password
📝 Need Google OAuth credentials
📝 Need to update Render build commands

## NEXT STEPS:
1. Get Gmail App Password
2. Get Google OAuth credentials  
3. Add all environment variables to Render
4. Update build commands (see BUILD_FIX.md)
5. Deploy!
