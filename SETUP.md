# 🛠 Portfolio Setup Guide

This guide will help you set up the DevMitra portfolio website locally on your machine.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.11+** ([Download here](https://python.org/downloads/))
- **Git** ([Download here](https://git-scm.com/downloads))
- **Code Editor** (VS Code, PyCharm, or any editor of your choice)

## 🚀 Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/logicbyroshan/portfolio-v2.0.git
cd portfolio-v2.0
```

### 2️⃣ Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration

Create a `.env` file in the root directory:

```env
# Basic Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (Optional - SQLite is default)
# DATABASE_URL=mysql://username:password@localhost:3306/portfolio_db

# Email Configuration (Required for contact forms)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Spotify API (Optional - for music section)
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret

# Google Gemini API (Optional - for AI chatbot)
GEMINI_API_KEY=your_gemini_api_key

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379/0
```

### 5️⃣ Database Setup

Run migrations to set up the database:

```bash
python manage.py migrate
```

### 6️⃣ Create Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

### 7️⃣ Collect Static Files (Production)

For production deployment:

```bash
python manage.py collectstatic
```

### 8️⃣ Run Development Server

Start the development server:

```bash
python manage.py runserver
```

🌐 **Access the website at:** http://127.0.0.1:8000/

## 🔧 Additional Configuration

### Email Setup (Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings → Security → 2-Step Verification → App Passwords
   - Select "Mail" and generate a password
   - Use this password in `EMAIL_HOST_PASSWORD`

### Spotify Integration

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app
3. Copy Client ID and Client Secret to your `.env` file
4. Add `http://127.0.0.1:8000/callback/` as a redirect URI

### Google Gemini API

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

## 📦 Database Options

### SQLite (Default)
No additional setup required. Database file will be created automatically.

### MySQL (Recommended for Production)

1. Install MySQL server
2. Create a database:
   ```sql
   CREATE DATABASE portfolio_db CHARACTER SET utf8mb4;
   CREATE USER 'portfolio_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'localhost';
   ```
3. Update `.env` with MySQL credentials
4. Install MySQL client: `pip install mysqlclient`

## 🚀 Deployment

### Quick Deploy on Render

1. Fork this repository
2. Connect to Render
3. Set environment variables in Render dashboard
4. Deploy!

### Docker Setup (Optional)

```bash
# Build image
docker build -t portfolio .

# Run container
docker run -p 8000:8000 portfolio
```

## 🔍 Troubleshooting

### Common Issues

**1. Module not found errors:**
```bash
pip install -r requirements.txt
```

**2. Database errors:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**3. Static files not loading:**
```bash
python manage.py collectstatic --clear
```

**4. Email not working:**
- Check Gmail App Password
- Verify EMAIL_* settings in `.env`
- Ensure Gmail 2FA is enabled

### Getting Help

If you encounter issues:

1. Check the [Issues](https://github.com/logicbyroshan/portfolio-v2.0/issues) page
2. Create a new issue with error details
3. Contact: [your-email@domain.com]

## 📝 Development Notes

### Project Structure Overview

- `portfolio/` - Main app (projects, skills, experience)
- `blog/` - Blog system with comments and categories
- `music/` - Spotify integration and playlists
- `ai/` - AI chatbot using Gemini API
- `auth_app/` - User authentication system
- `notifications/` - Email notifications
- `roshan/` - Personal resources and content

### Key Features to Test

1. **Contact Form** - Send test emails
2. **Blog System** - Create posts and comments
3. **Music Integration** - Test Spotify connectivity
4. **AI Chatbot** - Verify Gemini API responses
5. **Authentication** - Test signup/login flows

## 🎉 You're All Set!

Your portfolio website should now be running locally. Start customizing the content, colors, and features to make it your own!

---

**Need help?** Open an issue on GitHub or check the main [README.md](./README.md) for project overview.