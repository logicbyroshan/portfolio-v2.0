# Contributing to Portfolio v2.0# 🤝 Contributing to Portfolio v2.0



Thank you for your interest in contributing to this Django portfolio project! This document provides guidelines and information for contributors.Thank you for your interest in contributing to Portfolio v2.0! This is an open-source Django portfolio project and we welcome contributions from developers of all skill levels. This document will guide you through the contribution process.



## 🚀 Getting Started## 📋 Table of Contents



### Prerequisites- [Code of Conduct](#code-of-conduct)

- Python 3.8 or higher- [Getting Started](#getting-started)

- Django 5.2.7- [Development Setup](#development-setup)

- Git- [Contribution Workflow](#contribution-workflow)

- Virtual environment (recommended)- [Coding Standards](#coding-standards)

- [Pull Request Guidelines](#pull-request-guidelines)

### Local Development Setup- [Issue Reporting](#issue-reporting)

- [Community](#community)

1. **Fork and Clone the Repository**

   ```bash## 📜 Code of Conduct

   git clone https://github.com/yourusername/portfolio-v2.0.git

   cd portfolio-v2.0By participating in this project, you agree to abide by our Code of Conduct:

   ```

### Our Pledge

2. **Create Virtual Environment**- Be respectful and inclusive to all contributors

   ```bash- Use welcoming and constructive language

   python -m venv venv- Focus on what's best for the community

   source venv/bin/activate  # On Windows: venv\Scripts\activate- Show empathy towards other community members

   ```- Accept constructive criticism gracefully



3. **Install Dependencies**### Unacceptable Behavior

   ```bash- Harassment, trolling, or discriminatory language

   pip install -r requirements.txt- Personal attacks or political arguments

   pip install -r requirements-test.txt  # For development/testing- Publishing private information without permission

   ```- Any behavior that would be inappropriate in a professional setting



4. **Environment Setup**## 🚀 Getting Started

   ```bash

   cp .env.example .env### Prerequisites

   # Edit .env with your configuration- Python 3.11+

   ```- Git

- Basic understanding of Django framework

5. **Database Setup**- Familiarity with HTML, CSS, JavaScript

   ```bash- Knowledge of database concepts (MySQL/SQLite)

   python manage.py migrate

   python manage.py collectstatic### Initial Setup

   python manage.py createsuperuser  # Optional1. Fork the repository on GitHub

   ```2. Clone your forked repository:

   ```bash

6. **Run Development Server**   git clone https://github.com/YOUR_USERNAME/portfolio-v2.0.git

   ```bash   cd portfolio-v2.0

   python manage.py runserver   ```

   ```3. Follow the [SETUP.md](./SETUP.md) guide for local development setup



## 📁 Project Structure## 🛠 Development Setup



```### Environment Setup

portfolio-v2.0/```bash

├── ai/               # AI-powered features (Gemini integration)# Create virtual environment

├── authentication/   # User authentication systempython -m venv venv

├── blog/            # Blog management and displayvenv\Scripts\activate  # Windows

├── music/           # Spotify integration and music featuressource venv/bin/activate  # macOS/Linux

├── notifications/   # Notification system

├── portfolio/       # Main portfolio app (projects, skills, etc.)# Install dependencies

├── roshan/         # Personal sections and configurationspip install -r requirements.txt

├── config/         # Django settings and URL configurationpip install -r requirements-dev.txt  # Development dependencies

├── templates/      # HTML templates```

├── static/         # CSS, JavaScript, images

├── media/          # User-uploaded files### Pre-commit Hooks

└── tests/          # Test files and utilitiesInstall pre-commit hooks to ensure code quality:

``````bash

pip install pre-commit

## 🛠️ Development Guidelinespre-commit install

```

### Code Style

- Follow PEP 8 standards### Database Setup

- Use meaningful variable and function names```bash

- Add docstrings to functions and classespython manage.py migrate

- Keep functions small and focusedpython manage.py createsuperuser  # Optional

```

### Django Best Practices

- Use Django's built-in features when possible### Running Tests

- Follow the Model-View-Template (MVT) pattern```bash

- Use Django forms for user input validation# Run all tests

- Implement proper error handling and user feedbackpython manage.py test



### Database# Run specific app tests

- Always create migrations for model changespython manage.py test portfolio

- Use descriptive migration namespython manage.py test blog

- Test migrations both forward and backward

# Run with coverage

### Securitycoverage run manage.py test

- Never commit sensitive information (API keys, passwords)coverage report

- Use environment variables for configuration```

- Validate and sanitize user input

- Follow Django security best practices## 🔄 Contribution Workflow



## 🧪 Testing### 1. Choose an Issue

- Check the [Issues](https://github.com/logicbyroshan/portfolio-v2.0/issues) page

### Running Tests- Look for issues labeled `good first issue` for beginners

```bash- Comment on the issue to let others know you're working on it

# Run all tests

python manage.py test### 2. Create a Branch

```bash

# Run tests with pytest# Create and switch to a new branch

pytestgit checkout -b feature/your-feature-name

# or

# Run specific test filegit checkout -b fix/issue-description

python manage.py test portfolio.tests```



# Run with coverage### Branch Naming Convention:

pytest --cov=. --cov-report=html- `feature/feature-name` - New features

```- `fix/bug-description` - Bug fixes

- `docs/documentation-update` - Documentation updates

### Writing Tests- `refactor/component-name` - Code refactoring

- Write tests for new features and bug fixes- `test/test-description` - Adding tests

- Use Django's TestCase for database-related tests

- Use factories for creating test data### 3. Make Changes

- Test both positive and negative scenarios- Write clean, readable code

- Follow the coding standards (see below)

### Test Structure- Add tests for new features

```python- Update documentation if necessary

from django.test import TestCase

from django.contrib.auth.models import User### 4. Commit Changes

from portfolio.models import Project```bash

# Stage changes

class ProjectTestCase(TestCase):git add .

    def setUp(self):

        self.user = User.objects.create_user(# Commit with descriptive message

            username='testuser',git commit -m "feat: add user authentication system"

            password='testpass123'```

        )

        ### Commit Message Convention:

    def test_project_creation(self):- `feat:` - New feature

        project = Project.objects.create(- `fix:` - Bug fix

            title='Test Project',- `docs:` - Documentation changes

            summary='A test project',- `style:` - Formatting changes

            content='<p>Test content</p>'- `refactor:` - Code refactoring

        )- `test:` - Adding tests

        self.assertEqual(project.title, 'Test Project')- `chore:` - Maintenance tasks

        self.assertTrue(project.slug)

```### 5. Push and Create PR

```bash

## 📝 Contribution Process# Push to your fork

git push origin feature/your-feature-name

### 1. Choose an Issue```

- Check the [Issues](https://github.com/logicbyroshan/portfolio-v2.0/issues) pageThen create a Pull Request on GitHub.

- Look for issues labeled `good first issue` for beginners

- Comment on the issue to let others know you're working on it## 📝 Coding Standards



### 2. Create a Branch### Python/Django Standards

```bash

git checkout -b feature/your-feature-name#### Code Style

# or- Follow [PEP 8](https://pep8.org/) style guide

git checkout -b fix/your-bug-fix- Use [Black](https://black.readthedocs.io/) for code formatting

```- Line length: 88 characters maximum

- Use meaningful variable and function names

### 3. Make Changes

- Write clean, documented code#### Django Best Practices

- Follow the existing code style```python

- Add tests for new functionality# ✅ Good

- Update documentation if neededclass ProjectViewSet(viewsets.ModelViewSet):

    """ViewSet for managing portfolio projects."""

### 4. Test Your Changes    queryset = Project.objects.all()

```bash    serializer_class = ProjectSerializer

python manage.py test    permission_classes = [IsAuthenticatedOrReadOnly]

python manage.py check

python manage.py check --deploy  # For deployment readiness    def get_queryset(self):

```        """Filter projects based on user permissions."""

        return Project.objects.filter(is_published=True)

### 5. Commit Your Changes

```bash# ❌ Bad

git add .class PrjVS(viewsets.ModelViewSet):

git commit -m "Add: brief description of your changes"    q = Project.objects.all()

```    s = ProjectSerializer

```

**Commit Message Format:**

- `Add:` for new features#### Model Guidelines

- `Fix:` for bug fixes```python

- `Update:` for modifications# ✅ Good

- `Remove:` for deletionsclass Project(models.Model):

- `Docs:` for documentation changes    """Model representing a portfolio project."""

    

### 6. Push and Create Pull Request    title = models.CharField(

```bash        max_length=200, 

git push origin your-branch-name        help_text="Project title"

```    )

Then create a Pull Request on GitHub with:    created_at = models.DateTimeField(auto_now_add=True)

- Clear description of changes    

- Reference to related issues    class Meta:

- Screenshots for UI changes        ordering = ['-created_at']

        verbose_name = "Project"

## 🎨 Frontend Guidelines        verbose_name_plural = "Projects"

    

### HTML/Templates    def __str__(self):

- Use semantic HTML elements        return self.title

- Follow Django template best practices```

- Include proper meta tags for SEO

- Ensure accessibility (ARIA labels, alt text)#### View Guidelines

- Use class-based views when possible

### CSS- Handle exceptions properly

- Use consistent naming conventions- Add proper logging

- Follow mobile-first responsive design- Validate user input

- Optimize for performance

- Use CSS Grid/Flexbox for layouts### Frontend Standards



### JavaScript#### HTML/CSS

- Write vanilla JavaScript when possible- Use semantic HTML5 elements

- Use ES6+ features- Follow BEM methodology for CSS classes

- Add comments for complex logic- Ensure responsive design (mobile-first)

- Ensure cross-browser compatibility- Optimize for accessibility (WCAG guidelines)



## 🔧 Apps Overview#### JavaScript

- Use ES6+ features

### Portfolio App- Follow consistent naming conventions

Main application containing:- Add JSDoc comments for functions

- Projects showcase- Avoid global variables

- Skills management

- Experience timeline### Database Guidelines

- Achievements display- Use descriptive field names

- Contact form handling- Add proper indexes for performance

- Use foreign keys appropriately

### Blog App- Add help_text to model fields

Blog functionality including:

- Article creation and management## 📋 Pull Request Guidelines

- Comment system with moderation

- Category organization### Before Submitting

- SEO optimization- [ ] Code follows the style guidelines

- [ ] Tests pass locally

### AI App- [ ] New tests added for new features

AI-powered features:- [ ] Documentation updated

- Chatbot integration with Gemini API- [ ] No console errors or warnings

- Content generation assistance- [ ] Performance impact considered

- Smart recommendations

### PR Description Template

### Authentication App```markdown

User management system:## Description

- User registration and loginBrief description of changes

- Password reset functionality

- Profile management## Type of Change

- [ ] Bug fix

### Music App- [ ] New feature

Spotify integration:- [ ] Documentation update

- Currently playing display- [ ] Performance improvement

- Playlist management- [ ] Other (please describe)

- Music recommendations

## Testing

### Notifications App- [ ] Tests pass

Notification system:- [ ] Manual testing completed

- Email notifications

- In-app messaging## Screenshots (if applicable)

- Alert managementAdd screenshots for UI changes



## 🐛 Bug Reports## Additional Notes

Any additional information or context

When reporting bugs, please include:```

- Python/Django version

- Browser and version (for frontend issues)### Review Process

- Steps to reproduce1. Automated checks must pass

- Expected vs actual behavior2. At least one maintainer review required

- Error messages or screenshots3. Address feedback promptly

- Environment details4. Keep PR focused and atomic



## 💡 Feature Requests## 🐛 Issue Reporting



For new features:### Bug Reports

- Describe the problem you're solvingUse the bug report template and include:

- Explain your proposed solution- Clear description of the issue

- Consider backwards compatibility- Steps to reproduce

- Discuss potential alternatives- Expected vs actual behavior

- Environment details (OS, Python version, etc.)

## 📚 Resources- Screenshots/error messages



### Documentation### Feature Requests

- [Django Documentation](https://docs.djangoproject.com/)Use the feature request template and include:

- [Python Style Guide (PEP 8)](https://pep8.org/)- Clear description of the feature

- [Git Best Practices](https://git-scm.com/book/en/v2)- Use cases and benefits

- Possible implementation ideas

### APIs Used- Alternative solutions considered

- [Google Gemini AI](https://ai.google.dev/)

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)### Security Issues

- [TinyMCE](https://www.tiny.cloud/docs/)For security vulnerabilities, please email directly instead of creating public issues.



## 🤝 Community Guidelines## 🎯 Areas for Contribution



- Be respectful and inclusive### High Priority

- Help others learn and grow- [ ] Performance optimization

- Provide constructive feedback- [ ] Mobile responsiveness improvements

- Follow the code of conduct- [ ] Accessibility enhancements

- Ask questions if you're unsure- [ ] Test coverage improvements



## 📄 License### Medium Priority

- [ ] New integrations (APIs, services)

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.- [ ] UI/UX improvements

- [ ] Documentation updates

## 📞 Contact- [ ] Code refactoring



- **Project Maintainer**: Roshan Damor### Good First Issues

- **Email**: [Your Email]- [ ] Fix typos in documentation

- **GitHub**: [@logicbyroshan](https://github.com/logicbyroshan)- [ ] Add missing tests

- [ ] Improve error messages

## 🙏 Acknowledgments- [ ] Update dependencies



Thank you to all contributors who help make this project better! Your contributions, whether they're code, documentation, bug reports, or feature suggestions, are greatly appreciated.## 🏷 Labels Guide



---- `bug` - Something isn't working

- `enhancement` - New feature or request

**Happy Contributing! 🚀**- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `documentation` - Improvements to documentation
- `performance` - Performance related
- `security` - Security related
- `ui/ux` - User interface/experience

## 🤔 Getting Help

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Project Setup Guide](./SETUP.md)
- [Code Quality Guidelines](./CODE_QUALITY.md)

### Communication
- Create an issue for questions
- Join our discussions on GitHub
- Check existing issues and PRs first

### Mentoring
New contributors can request mentoring by:
1. Commenting on a `good first issue`
2. Asking specific questions in issues
3. Requesting code review guidance

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special mention for first-time contributors

## 📊 Development Metrics

We track:
- Code coverage (target: >80%)
- Performance metrics
- Security vulnerabilities
- Documentation completeness

Thank you for contributing to DevMitra Portfolio! 🚀

---

For questions about contributing, please create an issue or reach out to the maintainers.