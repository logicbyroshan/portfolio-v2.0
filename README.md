<h1 align="center">🌐 DevMitra — Intelligent Portfolio Website</h1>
<p align="center">
  <b>A next-gen portfolio platform built with Django, MySQL, APIs, and creativity — to showcase projects, skills, experiences, and more in an interactive and intelligent way.</b>
</p>
<p align="center">
  🌍 <b>Live Demo:</b> <a href="https://roshandamor.me" target="_blank">https://roshandamor.me</a>
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

---

## ✨ About DevMitra
**DevMitra** is not just a portfolio — it’s a **personal platform**.  
It goes beyond static resumes by offering dynamic features like blogs, projects, music playlists, AI chatbot, achievements, resources, and even collaboration tools.  

This project reflects my **journey, creativity, and technical growth**.  
I built DevMitra to document my work, share my learnings, and provide visitors with an **interactive experience** instead of just static information.

---

## 🚀 Features

### ✅ Current Features
- 🖥 **Responsive UI** — Fully mobile-friendly, smooth animations, dark/light mode with transitions.  
- 📂 **Projects & Experience** — Detail pages with filtering, sorting, and pagination.  
- ✍️ **Blogs** — Commenting, liking, newsletter subscription, and email notifications.  
- 🎵 **Music Playlists** — Integrated with **Spotify API**, includes music player.  
- 🏆 **Skills & Achievements** — Showcase with external links and downloads.  
- 📚 **Resources Section** — Useful materials, some downloadable.  
- 🤖 **AI Chatbot** — Built using **Gemini API**, answers in context of my portfolio.  
- ✉️ **Working Contact & Notifications** — Contact messages stored + emailed to me, with delivery confirmation sent to user.  
- 📄 **Resume Popups** — PDF preview and YouTube video resume embedded.  
- 🔒 **Authentication** — Signup, login, password reset with email support.  

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

## 📂 Project Structure

```bash
PORTFOLIO/
├── .github/            # GitHub workflows / CI
├── .vscode/            # VS Code workspace settings
├── ai/                 # AI assistant integration (Gemini API)
├── auth_app/           # Authentication app (signup, login, reset password)
├── config/             # Django project configuration
├── logs/               # Logs for debugging
├── media/              # Media uploads
├── music/              # Music playlists + Spotify integration
├── notifications/      # Notifications & email system
├── portfolio/          # Main app: projects, blogs, skills, resources
├── static/             # Static files (CSS, JS, Images)
├── templates/          # HTML templates
├── venv/               # Virtual environment
├── .env                # Environment variables
├── .gitignore          # Git ignore file
├── db.sqlite3          # Default SQLite DB (for dev)
├── manage.py           # Django CLI entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/logicbyroshan/portfolio-v2.0.git
cd portfolio-v2.0
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scriptsctivate
# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
```

### 5️⃣ Run Migrations
```bash
python manage.py migrate
```

### 6️⃣ Start Development Server
```bash
python manage.py runserver
```
Access at: **http://127.0.0.1:8000/**

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

## 🤝 Contributing
Contributions are welcome!  

Steps:
1. Fork the repo  
2. Create a new branch (`feature-branch`)  
3. Commit your changes  
4. Push to your fork  
5. Open a PR  

---

## 📜 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> 💡 *Tip: Always keep your live demo link updated in this README to impress recruiters and collaborators instantly.*
