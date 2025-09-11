<div align="center">
  
# 🚀 Developer Portfolio 2.0

<p>
  <img src="https://img.shields.io/badge/Django-5.2.5-green?style=for-the-badge&logo=django" alt="Django"/>
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql" alt="MySQL"/>
  <img src="https://img.shields.io/badge/cPanel-Ready-success?style=for-the-badge" alt="cPanel"/>
</p>

<p>
  <img src="https://img.shields.io/github/stars/logicbyroshan/portfolio-v2.0?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/logicbyroshan/portfolio-v2.0?style=social" alt="Forks"/>
  <img src="https://img.shields.io/github/watchers/logicbyroshan/portfolio-v2.0?style=social" alt="Watchers"/>
</p>

**A modern, professional Django-powered portfolio website designed to showcase your skills, projects, and experience. Perfect for developers, engineers, and tech professionals seeking their next opportunity.**

[🌐 Live Demo](https://your-domain.com) • [📖 Documentation](CPANEL_DEPLOYMENT.md) • [🐛 Report Bug](https://github.com/logicbyroshan/portfolio-v2.0/issues) • [✨ Request Feature](https://github.com/logicbyroshan/portfolio-v2.0/issues)

</div>

---

## ✨ Features

<table>
<tr>
<td>

### 🎨 **Frontend Excellence**
- 📱 Fully responsive design
- 🌙 Modern UI/UX interface
- ⚡ Fast loading times
- 🎯 SEO optimized
- 🖼️ Interactive portfolio showcase

</td>
<td>

### 🔧 **Backend Power**
- 🐍 Django 5.2.5 framework
- 🗄️ MySQL production database
- 🔐 Secure authentication system
- 📧 Contact form with email integration
- 🤖 AI-powered chatbot feature

</td>
</tr>
<tr>
<td>

### 📊 **Content Management**
- ✍️ Dynamic blog system
- 💼 Project showcase with details
- 🎯 Skills and expertise display
- 🏆 Achievements and certifications
- 📈 Experience timeline

</td>
<td>

### 🚀 **Deployment Ready**
- 🌐 cPanel hosting optimized
- 📦 Simple file structure
- ⚙️ Environment-based configuration
- 🔧 Easy maintenance and updates
- 📝 Comprehensive documentation

</td>
</tr>
</table>

---

## 📁 Project Architecture

<details>
<summary><b>🏗️ Click to expand detailed project structure</b></summary>

```bash
portfolio-2.0/
│
├── 📁 ai/                          # AI Chatbot Application
│   ├── __init__.py
│   ├── admin.py                    # Admin configuration
│   ├── apps.py                     # App configuration
│   ├── llm_utills.py              # LLM utilities
│   ├── models.py                   # AI query models
│   ├── tests.py                    # Basic tests
│   ├── urls.py                     # URL patterns
│   ├── utils.py                    # Utility functions
│   ├── views.py                    # AI chat views
│   ├── migrations/                 # Database migrations
│   └── templates/ai/               # AI-specific templates
│
├── 📁 auth_app/                     # Authentication System
│   ├── __init__.py
│   ├── admin.py                    # User admin
│   ├── apps.py                     # App configuration
│   ├── models.py                   # User models
│   ├── tests.py                    # Auth tests
│   ├── urls.py                     # Auth URLs
│   ├── views.py                    # Login/logout views
│   └── migrations/                 # Auth migrations
│
├── 📁 config/                       # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py                     # ASGI configuration
│   ├── urls.py                     # Main URL router
│   ├── wsgi.py                     # WSGI configuration
│   └── settings/                   # Environment-based settings
│       ├── __init__.py
│       ├── base.py                 # Shared settings
│       ├── development.py          # Dev environment
│       └── production.py           # Production (cPanel)
│
├── 📁 portfolio/                    # Main Portfolio Application
│   ├── __init__.py
│   ├── admin.py                    # Portfolio admin
│   ├── apps.py                     # App configuration
│   ├── context_processors.py       # Template contexts
│   ├── forms.py                    # Contact & newsletter forms
│   ├── models.py                   # Portfolio models
│   ├── tests.py                    # Portfolio tests
│   ├── urls.py                     # Portfolio URLs
│   ├── utils.py                    # Helper utilities
│   ├── views.py                    # Portfolio views
│   ├── migrations/                 # Database migrations
│   └── templatetags/               # Custom template tags
│
├── 📁 templates/                    # HTML Templates
│   ├── base.html                   # Base template
│   ├── home.html                   # Homepage
│   ├── skills.html                 # Skills showcase
│   ├── skill-dtl.html             # Skill details
│   ├── projects.html               # Projects listing
│   ├── project-dtl.html           # Project details
│   ├── blogs.html                  # Blog listing
│   ├── blog-dtl.html              # Blog details
│   ├── experience.html             # Experience timeline
│   ├── experience-dtl.html         # Experience details
│   ├── achievements.html           # Achievements
│   ├── auth_app/                   # Auth templates
│   └── emails/                     # Email templates
│
├── 📁 static/                       # Static Assets
│   ├── css/                        # Stylesheets
│   │   ├── main.css               # Main styles
│   │   ├── responsive.css         # Mobile styles
│   │   └── admin.css              # Admin customization
│   ├── js/                         # JavaScript files
│   │   ├── main.js                # Core functionality
│   │   ├── animations.js          # UI animations
│   │   └── form-validation.js     # Form handling
│   └── images/                     # Static images
│       ├── logos/                 # Brand logos
│       ├── icons/                 # UI icons
│       └── backgrounds/           # Background images
│
├── 📁 media/                        # User Uploaded Content
│   ├── avatars/                    # Profile pictures
│   ├── project_images/             # Project screenshots
│   ├── blog_covers/                # Blog cover images
│   ├── achievements/               # Certificates & awards
│   ├── resume/                     # Resume files
│   └── tech_icons/                 # Technology icons
│
├── 📁 staticfiles/                  # Collected static files (production)
│
├── 📄 Configuration Files
├── .env.example                    # Environment variables template
├── .htaccess                       # Web server config (cPanel)
├── passenger_wsgi.py               # WSGI entry point (cPanel)
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── db.sqlite3                      # Development database
├── README.md                       # This file
├── CPANEL_DEPLOYMENT.md            # Deployment guide
└── .gitignore                      # Git ignore rules
```

</details>

---

## 🏃‍♂️ Quick Start Guide

### 📋 Prerequisites

<table>
<tr>
<td>

**Development**
- Python 3.11+
- pip package manager
- Git version control
- Code editor (VS Code recommended)

</td>
<td>

**Production (cPanel)**
- cPanel hosting account
- MySQL database access
- Domain name
- FTP/File Manager access

</td>
</tr>
</table>

### 🛠️ Local Development Setup

<details>
<summary><b>💻 Step-by-step development setup</b></summary>

#### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/logicbyroshan/portfolio-v2.0.git
cd portfolio-v2.0
```

#### 2️⃣ **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

#### 4️⃣ **Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
DJANGO_ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-super-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 5️⃣ **Database Setup**
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

#### 6️⃣ **Launch Development Server**
```bash
python manage.py runserver
```

🌐 **Access your site at:** http://127.0.0.1:8000/

</details>

---

## 💻 Tech Stack & Dependencies

<div align="center">

### 🔧 **Core Technologies**

<table>
<tr>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="48" height="48"/>
<br><strong>Python 3.11+</strong>
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="48" height="48"/>
<br><strong>Django 5.2.5</strong>
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" width="48" height="48"/>
<br><strong>MySQL</strong>
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="48" height="48"/>
<br><strong>HTML5</strong>
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="48" height="48"/>
<br><strong>CSS3</strong>
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="48" height="48"/>
<br><strong>JavaScript</strong>
</td>
</tr>
</table>

### 📦 **Key Python Packages**

| Package | Version | Purpose |
|---------|---------|---------|
| `Django` | 5.2.5 | Web framework |
| `PyMySQL` | 1.1.2 | MySQL database connector |
| `Pillow` | 11.3.0 | Image processing |
| `django-cors-headers` | 4.5.0 | CORS handling |
| `django-tinymce` | 4.1.0 | Rich text editor |
| `google-generativeai` | 0.8.3 | AI chatbot integration |
| `python-dotenv` | 1.1.1 | Environment variables |
| `whitenoise` | 6.9.0 | Static files serving |

</div>

---

## 🚀 Deployment Guide

<div align="center">

### 🌐 **cPanel Hosting Deployment**

<img src="https://img.shields.io/badge/Optimized%20for-cPanel-blue?style=for-the-badge&logo=cpanel" alt="cPanel Optimized"/>

</div>

<details>
<summary><b>📘 Complete cPanel deployment walkthrough</b></summary>

#### 🎯 **Deployment Checklist**

- [ ] ✅ **Domain Setup** - Point domain to hosting
- [ ] 🗄️ **MySQL Database** - Create database in cPanel
- [ ] 📁 **File Upload** - Upload project files
- [ ] ⚙️ **Configuration** - Set environment variables
- [ ] 🔧 **WSGI Setup** - Configure passenger_wsgi.py
- [ ] 🌐 **Web Config** - Set up .htaccess
- [ ] 🧪 **Testing** - Verify deployment

#### 📚 **Detailed Instructions**

For complete step-by-step deployment instructions, see:
📖 **[CPANEL_DEPLOYMENT.md](CPANEL_DEPLOYMENT.md)**

#### 🔧 **Quick Deploy Commands**

```bash
# 1. Prepare files for upload
zip -r portfolio-deploy.zip . -x "venv/*" ".git/*" "*.pyc" "__pycache__/*"

# 2. Upload to cPanel public_html

# 3. Set permissions
chmod 644 .htaccess
chmod 644 passenger_wsgi.py
chmod -R 755 portfolio-2.0/

# 4. Run migrations (via cPanel terminal or SSH)
python manage.py migrate
python manage.py collectstatic --noinput
```

</details>

---

## 📊 Features Showcase

<div align="center">

### 🎯 **Portfolio Sections**

<table>
<tr>
<td align="center">
<img src="https://img.icons8.com/fluency/48/home.png"/>
<br><strong>🏠 Home</strong>
<br>Hero section with intro
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/code.png"/>
<br><strong>💻 Skills</strong>
<br>Technical expertise showcase
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/project.png"/>
<br><strong>📂 Projects</strong>
<br>Portfolio of work
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/blog.png"/>
<br><strong>📝 Blog</strong>
<br>Technical articles
</td>
</tr>
<tr>
<td align="center">
<img src="https://img.icons8.com/fluency/48/work.png"/>
<br><strong>💼 Experience</strong>
<br>Career timeline
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/trophy.png"/>
<br><strong>🏆 Achievements</strong>
<br>Certifications & awards
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/chatbot.png"/>
<br><strong>🤖 AI Chat</strong>
<br>Interactive assistant
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/contact-card.png"/>
<br><strong>📞 Contact</strong>
<br>Get in touch form
</td>
</tr>
</table>

</div>

---

## 🛠️ Development & Contributing

<details>
<summary><b>🔧 Development Guidelines</b></summary>

### 📝 **Code Standards**
- Follow PEP 8 style guide
- Write meaningful commit messages
- Add docstrings to functions
- Keep functions small and focused

### 🧪 **Testing**
```bash
# Run basic tests
python manage.py test

# Check for issues
python manage.py check
```

### 🌟 **Contributing Steps**
1. 🍴 Fork the repository
2. 🌿 Create feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing-feature`)
5. 🔀 Open a Pull Request

</details>

---

## 📈 GitHub Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api/pin/?username=logicbyroshan&repo=portfolio-v2.0&theme=tokyonight&hide_border=true" />

<br>

<img src="https://github-readme-stats.vercel.app/api?username=logicbyroshan&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" />

<img src="https://github-readme-streak-stats.herokuapp.com/?user=logicbyroshan&theme=tokyonight&hide_border=true" />

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=logicbyroshan&layout=compact&theme=tokyonight&hide_border=true" />

</div>

---

## 📞 Support & Contact

<div align="center">

<table>
<tr>
<td align="center">
<img src="https://img.icons8.com/fluency/48/github.png"/>
<br><a href="https://github.com/logicbyroshan"><strong>GitHub</strong></a>
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/linkedin.png"/>
<br><a href="https://linkedin.com/in/yourprofile"><strong>LinkedIn</strong></a>
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/email.png"/>
<br><a href="mailto:your-email@example.com"><strong>Email</strong></a>
</td>
<td align="center">
<img src="https://img.icons8.com/fluency/48/domain.png"/>
<br><a href="https://your-portfolio.com"><strong>Portfolio</strong></a>
</td>
</tr>
</table>

**Need Help?**
- 📖 Check [CPANEL_DEPLOYMENT.md](CPANEL_DEPLOYMENT.md) for deployment help
- 🐛 [Report issues](https://github.com/logicbyroshan/portfolio-v2.0/issues) on GitHub
- 💬 Start a [discussion](https://github.com/logicbyroshan/portfolio-v2.0/discussions) for questions

</div>

---

## 📜 License & Credits

<div align="center">

<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/>

**This project is licensed under the MIT License**
<br>See [LICENSE](LICENSE) file for details

<br>

**Built with ❤️ by [Roshan Damor](https://github.com/logicbyroshan)**

<br>

---

<sub>⭐ **Star this repo if it helped you!** ⭐</sub>

</div>
