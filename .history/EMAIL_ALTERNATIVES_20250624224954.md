# Alternative Email Provider Configurations for Modern360

## Option 1: Outlook/Hotmail SMTP
```bash
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-outlook-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

## Option 2: Yahoo Mail SMTP
```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-yahoo-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

## Option 3: SendGrid (Professional Email Service)
1. Sign up at https://sendgrid.com/ (free tier: 100 emails/day)
2. Create an API key
3. Use these settings:
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=your-verified-email@domain.com
```

## Option 4: Mailgun (Alternative Professional Service)
1. Sign up at https://www.mailgun.com/ (free tier: 5,000 emails/month)
2. Get SMTP credentials
3. Use provided SMTP settings

## Option 5: Try Gmail with Less Secure Apps (Not Recommended)
⚠️ This is less secure and Google is phasing this out:
1. Go to https://myaccount.google.com/lesssecureapps
2. Turn on "Less secure app access"
3. Use your regular Gmail password
