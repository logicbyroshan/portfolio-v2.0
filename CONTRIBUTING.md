# 🤝 Contributing to DevMitra Portfolio

Thank you for your interest in contributing to the DevMitra Portfolio project! We welcome contributions from developers of all skill levels. This document will guide you through the contribution process.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

### Our Pledge
- Be respectful and inclusive to all contributors
- Use welcoming and constructive language
- Focus on what's best for the community
- Show empathy towards other community members
- Accept constructive criticism gracefully

### Unacceptable Behavior
- Harassment, trolling, or discriminatory language
- Personal attacks or political arguments
- Publishing private information without permission
- Any behavior that would be inappropriate in a professional setting

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- Basic understanding of Django framework
- Familiarity with HTML, CSS, JavaScript
- Knowledge of database concepts (MySQL/SQLite)

### Initial Setup
1. Fork the repository on GitHub
2. Clone your forked repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/portfolio-v2.0.git
   cd portfolio-v2.0
   ```
3. Follow the [SETUP.md](./SETUP.md) guide for local development setup

## 🛠 Development Setup

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Pre-commit Hooks
Install pre-commit hooks to ensure code quality:
```bash
pip install pre-commit
pre-commit install
```

### Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test portfolio
python manage.py test blog

# Run with coverage
coverage run manage.py test
coverage report
```

## 🔄 Contribution Workflow

### 1. Choose an Issue
- Check the [Issues](https://github.com/logicbyroshan/portfolio-v2.0/issues) page
- Look for issues labeled `good first issue` for beginners
- Comment on the issue to let others know you're working on it

### 2. Create a Branch
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### Branch Naming Convention:
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation updates
- `refactor/component-name` - Code refactoring
- `test/test-description` - Adding tests

### 3. Make Changes
- Write clean, readable code
- Follow the coding standards (see below)
- Add tests for new features
- Update documentation if necessary

### 4. Commit Changes
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add user authentication system"
```

### Commit Message Convention:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Formatting changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 5. Push and Create PR
```bash
# Push to your fork
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub.

## 📝 Coding Standards

### Python/Django Standards

#### Code Style
- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Line length: 88 characters maximum
- Use meaningful variable and function names

#### Django Best Practices
```python
# ✅ Good
class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing portfolio projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter projects based on user permissions."""
        return Project.objects.filter(is_published=True)

# ❌ Bad
class PrjVS(viewsets.ModelViewSet):
    q = Project.objects.all()
    s = ProjectSerializer
```

#### Model Guidelines
```python
# ✅ Good
class Project(models.Model):
    """Model representing a portfolio project."""
    
    title = models.CharField(
        max_length=200, 
        help_text="Project title"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title
```

#### View Guidelines
- Use class-based views when possible
- Handle exceptions properly
- Add proper logging
- Validate user input

### Frontend Standards

#### HTML/CSS
- Use semantic HTML5 elements
- Follow BEM methodology for CSS classes
- Ensure responsive design (mobile-first)
- Optimize for accessibility (WCAG guidelines)

#### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Add JSDoc comments for functions
- Avoid global variables

### Database Guidelines
- Use descriptive field names
- Add proper indexes for performance
- Use foreign keys appropriately
- Add help_text to model fields

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows the style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No console errors or warnings
- [ ] Performance impact considered

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Additional Notes
Any additional information or context
```

### Review Process
1. Automated checks must pass
2. At least one maintainer review required
3. Address feedback promptly
4. Keep PR focused and atomic

## 🐛 Issue Reporting

### Bug Reports
Use the bug report template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots/error messages

### Feature Requests
Use the feature request template and include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation ideas
- Alternative solutions considered

### Security Issues
For security vulnerabilities, please email directly instead of creating public issues.

## 🎯 Areas for Contribution

### High Priority
- [ ] Performance optimization
- [ ] Mobile responsiveness improvements
- [ ] Accessibility enhancements
- [ ] Test coverage improvements

### Medium Priority
- [ ] New integrations (APIs, services)
- [ ] UI/UX improvements
- [ ] Documentation updates
- [ ] Code refactoring

### Good First Issues
- [ ] Fix typos in documentation
- [ ] Add missing tests
- [ ] Improve error messages
- [ ] Update dependencies

## 🏷 Labels Guide

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `good first issue` - Good for newcomers
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