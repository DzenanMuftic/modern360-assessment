# Gmail SMTP Setup Guide

This guide will help you set up Gmail SMTP for sending verification emails in the Modern360 Assessment Platform.

## Prerequisites

- Gmail account
- 2-Factor Authentication enabled on your Google account

## Step-by-Step Setup

### 1. Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Under "Signing in to Google", click on "2-Step Verification"
3. Follow the prompts to enable 2-Factor Authentication if not already enabled
4. This is **required** for generating App Passwords

### 2. Generate App Password

1. Stay in [Google Account Security](https://myaccount.google.com/security)
2. Under "Signing in to Google", you should now see "App passwords"
3. Click on "App passwords"
4. You may need to sign in again
5. In the "Select app" dropdown, choose "Mail"
6. In the "Select device" dropdown, choose "Other (custom name)"
7. Enter "Modern360 Assessment" as the device name
8. Click "Generate"
9. **Copy the 16-character password** that appears (it will look like: `abcd efgh ijkl mnop`)

### 3. Update Your .env File

Create or update your `.env` file with the following:

```bash
# Email configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Important Notes:**
- Replace `your-email@gmail.com` with your actual Gmail address
- Replace `abcd efgh ijkl mnop` with the 16-character App Password you generated
- Use the App Password, **NOT** your regular Gmail password
- Include spaces in the app password as shown by Google (or remove them - both work)

### 4. Test the Configuration

1. Start your Flask application
2. Go to the login page
3. Enter your email address
4. Check if you receive the verification email

## Troubleshooting

### Error: "Application-specific password required"
- This means you're using your regular Gmail password instead of an App Password
- Generate an App Password following the steps above

### Error: "Username and Password not accepted"
- Double-check your email address in `MAIL_USERNAME`
- Verify you're using the correct App Password
- Make sure 2-Factor Authentication is enabled

### Error: "SMTPAuthenticationError"
- Ensure 2-Factor Authentication is enabled on your Google account
- Regenerate the App Password if needed
- Check that `MAIL_SERVER` is set to `smtp.gmail.com`
- Verify `MAIL_PORT` is set to `587`

### Not Receiving Emails
- Check your spam/junk folder
- Verify the recipient email address is correct
- Check Flask application logs for any SMTP errors
- Test with a different email service (like Outlook) to isolate the issue

## Alternative Email Providers

If you prefer not to use Gmail, here are other SMTP configurations:

### Outlook/Hotmail
```bash
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

### Yahoo Mail
```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

### SendGrid (Recommended for Production)
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

## Security Best Practices

1. **Never commit your .env file** to version control
2. **Use App Passwords** instead of regular passwords
3. **Rotate App Passwords** periodically
4. **Use environment variables** in production (Render.com automatically handles this)
5. **Consider using SendGrid or similar service** for production deployments

## Production Deployment

When deploying to Render.com:

1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add the environment variables:
   - `MAIL_SERVER=smtp.gmail.com`
   - `MAIL_PORT=587`
   - `MAIL_USERNAME=your-email@gmail.com`
   - `MAIL_PASSWORD=your-16-character-app-password`
   - `MAIL_DEFAULT_SENDER=your-email@gmail.com`

5. Click "Save Changes"
6. Your application will automatically restart with the new configuration

The email authentication system will now work correctly!
