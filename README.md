<div align="center">
  <img src="./screenshots/Portfolio Thumb.jpg" alt="Portfolio Cover" width="100%" style="border-radius: 10px; margin-bottom: 20px;"/>
</div>

<h1 align="center">🌐 DevMitra — Intelligent Portfolio Website</h1>
<p align="center">
  <b>A next-gen portfolio platform built with Django, MySQL, APIs, and creativity — to showcase projects, skills, experiences, and more in an interactive and intelligent way.</b>
</p>
<p align="center">
  🌍 <b>Live Demo:</b> <a href="https://roshandamor.me" target="_blank">https://roshandamor.me</a> | 
  📖 <b>Setup Guide:</b> <a href="./SETUP.md">SETUP.md</a>
</p>

<p align="center">
  <a href="https://github.com/logicbyroshan/portfolio-v2.0/stargazers">
    <img src="https://img.shields.io/github/stars/logicbyroshan/portfolio-v2.0?style=flat-square&color=yellow" alt="Stars"/>
  </a>
  <a href="https://github.com/logicbyroshan/portfolio-v2.0/network/members">
    <img src="https://img.shields.io/github/forks/logicbyroshan/portfolio-v2.0?style=flat-square&color=blue" alt="Forks"/>
  </a>
  <a href="#">
    <img src="https://img.shields.io/github/repo-size/logicbyroshan/portfolio-v2.0?style=flat-square&color=orange" alt="Repo Size"/>
  </a>
  <a href="#">
    <img src="https://img.shields.io/github/last-commit/logicbyroshan/portfolio-v2.0?style=flat-square&color=green" alt="Last Commit"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"/>
  </a>
</p>

## 📸 Screenshots

<div align="center">
  <table>
    <tr>
      <td width="50%">
        <img src="./screenshots/Hero.png" alt="Hero Section" style="border-radius: 8px;"/>
        <p align="center"><b>Hero Section</b></p>
      </td>
      <td width="50%">
        <img src="./screenshots/Projects.png" alt="Projects Section" style="border-radius: 8px;"/>
        <p align="center"><b>Projects Section</b></p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <img src="./screenshots/Skills.png" alt="Skills Section" style="border-radius: 8px;"/>
        <p align="center"><b>Skills Section</b></p>
      </td>
      <td width="50%">
        <img src="./screenshots/Contacts.png" alt="Contact Section" style="border-radius: 8px;"/>
        <p align="center"><b>Contact Section</b></p>
      </td>
    </tr>
  </table>
</div>

---

## ✨ About DevMitra
**DevMitra** is not just a portfolio — it’s a **personal platform**.  
It goes beyond static resumes by offering dynamic features like blogs, projects, music playlists, AI chatbot, achievements, resources, and even collaboration tools.  

This project reflects my **journey, creativity, and technical growth**.  
I built DevMitra to document my work, share my learnings, and provide visitors with an **interactive experience** instead of just static information.

---

## 🚀 Features

### ✅ Current Features
- 🖥 **Responsive UI** — Fully mobile-friendly, smooth animations, optimized CSS architecture
- 📂 **Projects & Experience** — Detail pages with filtering, sorting, and pagination  
- ✍️ **Blog System** — Dedicated blog app with commenting, categories, and rich content
- 🎵 **Music Integration** — Spotify API integration with playlist management
- 🏆 **Skills & Achievements** — Interactive showcase with detailed skill pages
- 📚 **Resources Hub** — Personal resources and downloadable materials (roshan app)
- 🤖 **AI Assistant** — Gemini API powered chatbot for portfolio queries
- ✉️ **Smart Notifications** — Email system with contact forms and confirmations
- 📄 **Resume Features** — PDF preview and video resume integration
- 🔒 **Authentication System** — Complete user management with secure login/signup
- 🎨 **Centralized CSS** — Consolidated animations, components, and responsive design  

### 🔮 Upcoming Features
- ✅ **ToDo App** (integrated mini-app).  
- ✅ **Project Manager & Blog Manager** (admin tools).  
- 🌍 **Dedicated Blog Website** with preferences, social login, AI suggestions.  
- 🛠 **Custom Admin Dashboard** to manage projects, blogs, resources, and notifications.  
- 🔗 **REST API Integration** across apps (portfolio + blog + community).  
- 💬 **Real-time Collaboration** (WebSockets for Code Together).  
- 🎮 **Gamified Blogs** — Reader badges & engagement tracking.  
- 👥 **User Profiles** — Social login, preferences, and personalization.  
- ⚡ **DevOps Ready** — Dockerization, CI/CD, and scalable deployment.  

---

## 📂 Complete Project Structure

```bash
portfolio-v2.0/
├── 📁 Root Files & Configuration
│   ├── manage.py                    # Django management script
│   ├── requirements.txt             # Python dependencies
│   ├── db.sqlite3                   # SQLite database (auto-generated)
│   ├── .env                         # Environment variables (create this)
│   ├── .gitignore                   # Git ignore rules
│   ├── README.md                    # Project documentation
│   ├── SETUP.md                     # Detailed setup guide
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── CODE_QUALITY.md             # Code standards & best practices
│   ├── SECURITY.md                 # Security policy & vulnerability reporting
│   ├── deploye_key                 # SSH deploy key (if needed)
│   └── deploye_key.pub             # SSH public key (if needed)
│
├── 📁 Django Apps
│   ├── config/                      # Main Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py              # Django configuration
│   │   ├── urls.py                  # URL routing
│   │   ├── wsgi.py                  # WSGI application
│   │   └── asgi.py                  # ASGI application (async support)
│   │
│   ├── portfolio/                   # Main portfolio application
│   │   ├── models.py                # Database models (Projects, Skills, etc.)
│   │   ├── views.py                 # View logic
│   │   ├── urls.py                  # URL patterns
│   │   ├── admin.py                 # Django admin configuration
│   │   ├── forms.py                 # Django forms
│   │   ├── context_processors.py    # Context processors
│   │   ├── sitemaps.py              # SEO sitemaps
│   │   ├── migrations/              # Database migrations
│   │   └── templatetags/            # Custom template tags
│   │
│   ├── blog/                        # Blog system
│   │   ├── models.py                # Blog models (Post, Comment, Category)
│   │   ├── views.py                 # Blog views
│   │   ├── urls.py                  # Blog URL patterns
│   │   ├── admin.py                 # Blog admin interface
│   │   ├── sitemaps.py              # Blog SEO
│   │   └── migrations/              # Blog database migrations
│   │
│   ├── ai/                          # AI Assistant (Gemini API)
│   │   ├── models.py                # AI conversation models
│   │   ├── views.py                 # AI API endpoints
│   │   ├── llm_utils.py             # AI utility functions
│   │   ├── utils.py                 # Helper functions
│   │   ├── urls.py                  # AI URL patterns
│   │   └── templates/ai/            # AI chat templates
│   │
│   ├── music/                       # Spotify Integration
│   │   ├── models.py                # Music models (Playlist, Track)
│   │   ├── views.py                 # Music views
│   │   ├── spotify_service.py       # Spotify API service
│   │   ├── urls.py                  # Music URL patterns
│   │   ├── static/                  # Music app static files
│   │   └── templates/music/         # Music templates
│   │
│   ├── auth_app/                    # Authentication System
│   │   ├── models.py                # User models (if extended)
│   │   ├── views.py                 # Auth views (login, signup, etc.)
│   │   ├── urls.py                  # Auth URL patterns
│   │   └── migrations/              # Auth migrations
│   │
│   ├── notifications/               # Email & Notification System
│   │   ├── models.py                # Notification models
│   │   ├── views.py                 # Notification views
│   │   ├── services.py              # Email services
│   │   ├── signals.py               # Django signals
│   │   └── migrations/              # Notification migrations
│   │
│   └── roshan/                      # Personal Resources App
│       ├── models.py                # Resource models
│       ├── views.py                 # Resource views
│       ├── forms.py                 # Resource forms
│       ├── urls.py                  # Resource URL patterns
│       ├── templates/               # Resource templates
│       └── migrations/              # Resource migrations
│
├── 📁 Frontend Assets
│   ├── static/                      # Static files (served in production)
│   │   ├── css/                     # Compiled CSS files
│   │   ├── js/                      # JavaScript files
│   │   └── images/                  # Static images
│   │
│   ├── templates/                   # HTML Templates
│   │   ├── base.html                # Base template
│   │   ├── home.html                # Homepage
│   │   ├── aboutme.html             # About page
│   │   ├── projects.html            # Projects listing
│   │   ├── project-dtl.html         # Project detail
│   │   ├── blogs.html               # Blog listing
│   │   ├── blog-dtl.html            # Blog detail
│   │   ├── experience.html          # Experience page
│   │   ├── experience-dtl.html      # Experience detail
│   │   ├── achievements.html        # Achievements page
│   │   ├── resources.html           # Resources page
│   │   ├── resource-detail.html     # Resource detail
│   │   ├── skill-dtl.html           # Skill detail
│   │   ├── robots.txt               # SEO robots file
│   │   ├── auth_app/                # Auth templates
│   │   ├── emails/                  # Email templates
│   │   └── legal/                   # Legal pages (privacy, terms)
│   │
│   └── media/                       # User uploaded files (auto-generated)
│       ├── achievements/            # Achievement images
│       ├── avatars/                 # User avatars
│       ├── blog_covers/             # Blog cover images
│       ├── project_covers/          # Project cover images
│       ├── project_images/          # Project gallery images
│       ├── resume/                  # Resume files (PDF, etc.)
│       └── tech_icons/              # Technology icons
│
├── 📁 Development & Documentation
│   ├── screenshots/                 # Project screenshots for README
│   ├── logs/                        # Application logs (auto-generated)
│   └── .vscode/                     # VS Code settings (optional)
│
└── 📁 Deployment & CI/CD
    └── .github/                     # GitHub workflows (if using GitHub Actions)
```

---

## 🚀 Quick Start & Detailed Setup

> **⚠️ Important:** Follow these steps carefully to avoid common setup issues like "logs folder not found" and other errors.

### 📋 Prerequisites
- **Python 3.11+** ([Download](https://python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Code Editor** (VS Code recommended)

For complete setup details with API configurations, see: **[SETUP.md](./SETUP.md)**

### 🛠 Step-by-Step Setup

#### 1️⃣ Clone the Repository
```bash
# Clone the project
git clone https://github.com/logicbyroshan/portfolio-v2.0.git
cd portfolio-v2.0

# Verify you're in the right directory
ls  # Should show manage.py, requirements.txt, etc.
```

#### 2️⃣ Create Required Directories (Fix Common Issues)
```bash
# Create missing directories that might cause errors
mkdir logs           # For application logs
mkdir media         # For uploaded files (if not exists)
mkdir static        # For static files (if not exists)

# Create media subdirectories (Windows)
mkdir media\achievements, media\avatars, media\blog_covers, media\project_covers, media\project_images, media\resume, media\tech_icons

# Create media subdirectories (macOS/Linux)
mkdir -p media/{achievements,avatars,blog_covers,project_covers,project_images,resume,tech_icons}
```

#### 3️⃣ Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (Command Prompt)  
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
which python  # Should point to venv/Scripts/python or venv/bin/python
```

#### 4️⃣ Install Dependencies
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list  # Should show Django, etc.
```

#### 5️⃣ Environment Configuration
Create a `.env` file in the root directory:

```bash
# Create .env file
# Windows
echo. > .env

# macOS/Linux
touch .env
```

Add this content to `.env`:
```env
# Django Settings
SECRET_KEY=django-insecure-your-very-long-secret-key-here-make-it-at-least-50-characters-long
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (SQLite is default, no setup needed)
# For MySQL: DATABASE_URL=mysql://username:password@localhost:3306/portfolio_db

# Email Configuration (for contact forms)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Optional API Keys (leave blank if not using)
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
GEMINI_API_KEY=your_gemini_api_key

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379/0
```

#### 6️⃣ Database Setup
```bash
# Create initial migrations (if needed)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional - for admin access)
python manage.py createsuperuser
```

#### 7️⃣ Collect Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

#### 8️⃣ Test the Setup
```bash
# Run development server
python manage.py runserver

# Or specify port
python manage.py runserver 8000
```

🌐 **Access the website at:** http://127.0.0.1:8000/

### 🔧 Common Setup Issues & Solutions

#### ❌ Issue: "logs folder not found"
```bash
# ✅ Solution: Create the logs directory
mkdir logs
```

#### ❌ Issue: "No module named 'config'"
```bash
# ✅ Solution: Make sure you're in the project root directory
pwd  # Should show .../portfolio-v2.0
ls   # Should show manage.py
```

#### ❌ Issue: "Permission denied" on virtual environment (Windows)
```bash
# ✅ Solution: Enable script execution in PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv
venv\Scripts\Activate.ps1
```

#### ❌ Issue: "Port already in use"
```bash
# ✅ Solution: Use a different port
python manage.py runserver 8001

# Or find and kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux  
lsof -ti:8000 | xargs kill -9
```

#### ❌ Issue: Email configuration errors
```bash
# ✅ Solution: Generate Gmail App Password
# 1. Enable 2-Factor Authentication on Gmail
# 2. Go to Google Account Settings → Security → App Passwords
# 3. Generate password for "Mail"
# 4. Use this password in EMAIL_HOST_PASSWORD (not your regular password)
```

#### ❌ Issue: Static files not loading
```bash
# ✅ Solution: Collect static files again
python manage.py collectstatic --clear --noinput

# Ensure DEBUG=True in .env for development
```

### 🚀 Quick One-Liner Setup
For experienced developers:

**Windows:**
```powershell
git clone https://github.com/logicbyroshan/portfolio-v2.0.git; cd portfolio-v2.0; mkdir logs, media, static; python -m venv venv; venv\Scripts\Activate.ps1; pip install -r requirements.txt; python manage.py migrate; python manage.py runserver
```

**macOS/Linux:**
```bash
git clone https://github.com/logicbyroshan/portfolio-v2.0.git && cd portfolio-v2.0 && mkdir -p logs media static media/{achievements,avatars,blog_covers,project_covers,project_images,resume,tech_icons} && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```

### ✅ Verify Your Setup
After setup, you should be able to:
- [ ] Access the homepage at http://127.0.0.1:8000/
- [ ] Navigate through different sections (Projects, Blog, Experience, etc.)
- [ ] Access admin panel at http://127.0.0.1:8000/admin/ (if superuser created)
- [ ] See no error messages in terminal
- [ ] View static files loading correctly (CSS, images, icons)

### 🆘 Still Having Issues?
1. **Check Python Version:** `python --version` (should be 3.11+)
2. **Check Virtual Environment:** Your prompt should show `(venv)`
3. **Check Dependencies:** `pip list` should show Django and other packages
4. **Create an Issue:** If problems persist, create a GitHub issue with error details

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Programming language |
| **Django 5.2.5** | Backend framework |
| **MySQL / SQLite** | Database |
| **HTML5, CSS3, JS** | Frontend |
| **Redis** | Caching & async tasks |
| **Spotipy** | Spotify API integration |
| **Google Gemini API** | AI chatbot |
| **Django AllAuth** | Authentication & social login |
| **TinyMCE** | Rich text editor |
| **Whitenoise & Gunicorn** | Deployment |

---

## 📦 Key Dependencies

From [`requirements.txt`](./requirements.txt):

- `Django==5.2.5`  
- `django-allauth==65.4.0`  
- `django-cors-headers==4.8.0`  
- `django-tinymce==4.1.0`  
- `mysqlclient==2.2.7` / `PyMySQL==1.1.2`  
- `redis==6.4.0`  
- `spotipy==2.25.1`  
- `google-generativeai==0.8.5`  
- `google-ai-generativelanguage==0.6.15`  
- `gunicorn==23.0.0`  
- `whitenoise==6.10.0`  
- `python-dotenv==1.1.1`  
- `pillow==11.3.0`  

_(Full list available in `requirements.txt`.)_

---

## 🚀 Deployment Options
- **Render / Railway** — Easy cloud deployment.  
- **Dockerized Setup** — Coming soon.  
- **Custom VPS** with Nginx + Gunicorn + SSL.  

---

## 🎯 Recent Improvements

- ✅ **CSS Architecture Overhaul** — Consolidated 300+ lines of duplicate CSS into centralized components
- ✅ **Responsive Optimization** — Enhanced mobile experience with better spacing and typography
- ✅ **Blog System** — Completely separated blog functionality into dedicated Django app
- ✅ **Animation System** — Unified data-animation system across all pages
- ✅ **Component Consolidation** — Breadcrumbs, page headers, and grid layouts centralized in base.css
- ✅ **Performance Boost** — Reduced CSS bloat and improved maintainability

## 🤝 Contributing

We welcome contributions from developers of all skill levels! Whether you're fixing bugs, adding features, improving documentation, or enhancing security, your contributions make this project better.

### 📚 Documentation
Before contributing, please read our comprehensive guides:

- **[Contributing Guidelines](./CONTRIBUTING.md)** - Complete guide to contributing
- **[Code Quality Standards](./CODE_QUALITY.md)** - Coding standards and best practices  
- **[Security Policy](./SECURITY.md)** - Security guidelines and vulnerability reporting
- **[Setup Guide](./SETUP.md)** - Local development setup instructions

### 🚀 Quick Start for Contributors
1. **Fork & Clone**: Fork the repository and clone your fork
2. **Setup Environment**: Follow the [SETUP.md](./SETUP.md) guide  
3. **Choose an Issue**: Browse [open issues](https://github.com/logicbyroshan/portfolio-v2.0/issues) or create a new one
4. **Follow Standards**: Adhere to our [code quality guidelines](./CODE_QUALITY.md)
5. **Submit PR**: Create a pull request following our [contributing guidelines](./CONTRIBUTING.md)

### 🎯 Areas We Need Help With
- 🐛 Bug fixes and performance improvements
- 📱 Mobile responsiveness enhancements  
- ♿ Accessibility improvements
- 🧪 Test coverage expansion
- 📖 Documentation updates
- 🔒 Security enhancements
- 🎨 UI/UX improvements

### 🏷️ Good First Issues
Look for issues labeled `good first issue` - these are perfect for newcomers and first-time contributors.

---

## 🔒 Security

Security is a top priority for this project. Please read our [Security Policy](./SECURITY.md) for:
- Supported versions
- How to report vulnerabilities  
- Security best practices
- Incident response procedures

**Found a security issue?** Please report it responsibly by emailing security@roshandamor.me

---

## 📜 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> 💡 *Tip: Always keep your live demo link updated in this README to impress recruiters and collaborators instantly.*
