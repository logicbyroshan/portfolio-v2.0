# 🎯 Code Quality Guidelines

This document outlines the code quality standards, best practices, and guidelines for the DevMitra Portfolio project. Following these guidelines ensures maintainable, scalable, and robust code.

## 📋 Table of Contents

- [Code Quality Principles](#code-quality-principles)
- [Python/Django Standards](#pythondjango-standards)
- [Frontend Standards](#frontend-standards)
- [Testing Guidelines](#testing-guidelines)
- [Performance Guidelines](#performance-guidelines)
- [Security Guidelines](#security-guidelines)
- [Documentation Standards](#documentation-standards)
- [Code Review Checklist](#code-review-checklist)
- [Tools and Automation](#tools-and-automation)

## 🎪 Code Quality Principles

### SOLID Principles
- **Single Responsibility**: Each class/function should have one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Objects should be replaceable with instances of subtypes
- **Interface Segregation**: Many client-specific interfaces are better than one general-purpose interface
- **Dependency Inversion**: Depend on abstractions, not concretions

### Clean Code Principles
- **Readable**: Code should be self-documenting
- **Simple**: Avoid unnecessary complexity
- **Testable**: Write code that's easy to test
- **Maintainable**: Future developers should easily understand and modify
- **Consistent**: Follow established patterns and conventions

## 🐍 Python/Django Standards

### Code Style and Formatting

#### PEP 8 Compliance
```python
# ✅ Good - PEP 8 compliant
def calculate_project_rating(project_id: int) -> float:
    """Calculate the average rating for a project."""
    project = Project.objects.get(id=project_id)
    ratings = project.ratings.all()
    
    if not ratings.exists():
        return 0.0
    
    total_rating = sum(rating.score for rating in ratings)
    return total_rating / ratings.count()

# ❌ Bad - Not PEP 8 compliant
def calcProjRating(pid):
    proj=Project.objects.get(id=pid)
    rats=proj.ratings.all()
    if not rats.exists():return 0.0
    tot=sum(r.score for r in rats)
    return tot/rats.count()
```

#### Import Organization
```python
# ✅ Good - Proper import order
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
import requests
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

# Local application imports
from .models import Project, Skill
from .utils import calculate_rating
```

### Django Best Practices

#### Model Design
```python
# ✅ Good - Well-designed model
class Project(models.Model):
    """Model representing a portfolio project."""
    
    # Constants
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Fields with proper attributes
    title = models.CharField(
        max_length=200,
        help_text="Project title (max 200 characters)"
    )
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly version of title"
    )
    description = models.TextField(
        help_text="Detailed project description"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/projects/{self.slug}/"
    
    @property
    def is_published(self):
        return self.status == 'published'
```

#### View Design
```python
# ✅ Good - Class-based view with proper error handling
class ProjectListView(ListView):
    """Display list of published projects."""
    
    model = Project
    template_name = 'portfolio/projects.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        """Return only published projects."""
        return Project.objects.filter(
            status='published'
        ).select_related('category').prefetch_related('technologies')
    
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['page_title'] = 'My Projects'
        return context

# ✅ Good - Function-based view with proper validation
@require_http_methods(["POST"])
@csrf_protect
def submit_contact_form(request):
    """Handle contact form submission."""
    try:
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form
            contact = form.save()
            
            # Send notification
            send_contact_notification.delay(contact.id)
            
            messages.success(request, "Thank you for your message!")
            return redirect('contact_success')
        else:
            messages.error(request, "Please correct the errors below.")
            
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        messages.error(request, "An error occurred. Please try again.")
    
    return render(request, 'contact.html', {'form': form})
```

#### Error Handling
```python
# ✅ Good - Comprehensive error handling
def get_project_or_404(slug: str) -> Project:
    """Get project by slug or raise 404."""
    try:
        return Project.objects.select_related('category').get(
            slug=slug,
            status='published'
        )
    except Project.DoesNotExist:
        logger.warning(f"Project not found: {slug}")
        raise Http404("Project not found")
    except Exception as e:
        logger.error(f"Error fetching project {slug}: {str(e)}")
        raise
```

### Type Hints
```python
# ✅ Good - Proper type hints
from typing import List, Optional, Dict, Any
from django.http import HttpRequest, HttpResponse

def process_project_data(
    project_id: int,
    user: User,
    metadata: Optional[Dict[str, Any]] = None
) -> List[Dict[str, str]]:
    """Process project data and return formatted results."""
    pass
```

## 🎨 Frontend Standards

### HTML Best Practices
```html
<!-- ✅ Good - Semantic HTML with accessibility -->
<article class="project-card" role="article">
    <header class="project-card__header">
        <h2 class="project-card__title">
            <a href="/projects/portfolio-website/" 
               aria-label="View Portfolio Website project details">
                Portfolio Website
            </a>
        </h2>
    </header>
    
    <div class="project-card__content">
        <img src="/media/projects/portfolio.jpg" 
             alt="Portfolio website screenshot showing homepage"
             class="project-card__image"
             loading="lazy">
        
        <p class="project-card__description">
            A responsive portfolio website built with Django and modern web technologies.
        </p>
    </div>
    
    <footer class="project-card__footer">
        <ul class="project-card__technologies" aria-label="Technologies used">
            <li class="tech-tag tech-tag--python">Python</li>
            <li class="tech-tag tech-tag--django">Django</li>
            <li class="tech-tag tech-tag--javascript">JavaScript</li>
        </ul>
    </footer>
</article>
```

### CSS Best Practices
```css
/* ✅ Good - BEM methodology with proper organization */

/* Component: Project Card */
.project-card {
    background: var(--color-surface);
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-card);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    container-type: inline-size;
}

.project-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-card-hover);
}

.project-card__header {
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--color-border);
}

.project-card__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-tight);
    margin: 0;
}

.project-card__title a {
    color: var(--color-text-primary);
    text-decoration: none;
    transition: color 0.2s ease;
}

.project-card__title a:hover {
    color: var(--color-primary);
}

/* Responsive design with container queries */
@container (min-width: 300px) {
    .project-card__content {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: var(--spacing-md);
        align-items: start;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .project-card {
        background: var(--color-surface-dark);
        box-shadow: var(--shadow-card-dark);
    }
}
```

### JavaScript Best Practices
```javascript
// ✅ Good - Modern JavaScript with proper error handling

/**
 * Project management utilities
 */
class ProjectManager {
    constructor(apiEndpoint) {
        this.apiEndpoint = apiEndpoint;
        this.cache = new Map();
    }

    /**
     * Fetch project data with caching
     * @param {string} projectId - Project identifier
     * @returns {Promise<Object>} Project data
     */
    async fetchProject(projectId) {
        if (this.cache.has(projectId)) {
            return this.cache.get(projectId);
        }

        try {
            const response = await fetch(`${this.apiEndpoint}/projects/${projectId}/`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const project = await response.json();
            this.cache.set(projectId, project);
            
            return project;
        } catch (error) {
            console.error('Failed to fetch project:', error);
            throw new Error('Failed to load project data');
        }
    }

    /**
     * Display project in UI
     * @param {Object} project - Project data
     * @param {HTMLElement} container - Container element
     */
    displayProject(project, container) {
        if (!project || !container) {
            throw new Error('Invalid project data or container');
        }

        const template = document.getElementById('project-template');
        if (!template) {
            throw new Error('Project template not found');
        }

        const clone = template.content.cloneNode(true);
        
        // Safely update content
        this.updateElement(clone, '.project-title', project.title);
        this.updateElement(clone, '.project-description', project.description);
        this.updateImage(clone, '.project-image', project.image, project.title);

        container.appendChild(clone);
    }

    /**
     * Safely update element content
     * @private
     */
    updateElement(container, selector, content) {
        const element = container.querySelector(selector);
        if (element && content) {
            element.textContent = content;
        }
    }

    /**
     * Safely update image element
     * @private
     */
    updateImage(container, selector, src, alt) {
        const img = container.querySelector(selector);
        if (img && src) {
            img.src = src;
            img.alt = alt || '';
        }
    }
}

// Usage
document.addEventListener('DOMContentLoaded', () => {
    const projectManager = new ProjectManager('/api/v1');
    
    // Initialize project display
    projectManager.fetchProject('portfolio-website')
        .then(project => {
            const container = document.getElementById('project-container');
            projectManager.displayProject(project, container);
        })
        .catch(error => {
            console.error('Failed to initialize project:', error);
            // Show user-friendly error message
        });
});
```

## 🧪 Testing Guidelines

### Test Structure
```python
# ✅ Good - Comprehensive test class
class ProjectModelTest(TestCase):
    """Test cases for Project model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Web Development',
            slug='web-development'
        )
    
    def test_project_creation(self):
        """Test project creation with valid data."""
        project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            description='A test project description',
            category=self.category,
            author=self.user
        )
        
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.slug, 'test-project')
        self.assertTrue(project.is_published)
        self.assertEqual(str(project), 'Test Project')
    
    def test_project_absolute_url(self):
        """Test project URL generation."""
        project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            category=self.category,
            author=self.user
        )
        
        expected_url = '/projects/test-project/'
        self.assertEqual(project.get_absolute_url(), expected_url)
    
    def test_project_slug_uniqueness(self):
        """Test that project slugs must be unique."""
        Project.objects.create(
            title='First Project',
            slug='unique-slug',
            category=self.category,
            author=self.user
        )
        
        with self.assertRaises(IntegrityError):
            Project.objects.create(
                title='Second Project',
                slug='unique-slug',  # Duplicate slug
                category=self.category,
                author=self.user
            )
```

### View Testing
```python
class ProjectViewTest(TestCase):
    """Test cases for project views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            status='published'
        )
    
    def test_project_list_view(self):
        """Test project list view returns correct data."""
        response = self.client.get('/projects/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        self.assertIn('projects', response.context)
    
    def test_project_detail_view(self):
        """Test project detail view."""
        response = self.client.get(f'/projects/{self.project.slug}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], self.project)
    
    def test_project_404(self):
        """Test 404 for non-existent project."""
        response = self.client.get('/projects/non-existent/')
        self.assertEqual(response.status_code, 404)
```

## ⚡ Performance Guidelines

### Database Optimization
```python
# ✅ Good - Optimized queries
def get_projects_with_related_data():
    """Get projects with optimized queries."""
    return Project.objects.select_related(
        'category',
        'author'
    ).prefetch_related(
        'technologies',
        'images'
    ).filter(status='published')

# ✅ Good - Efficient pagination
class ProjectListView(ListView):
    queryset = Project.objects.select_related('category').filter(status='published')
    paginate_by = 12  # Reasonable page size
```

### Caching Strategy
```python
# ✅ Good - Proper caching
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def project_list_view(request):
    """Cached project list view."""
    pass

def get_featured_projects():
    """Get featured projects with caching."""
    cache_key = 'featured_projects'
    projects = cache.get(cache_key)
    
    if projects is None:
        projects = list(
            Project.objects.filter(
                is_featured=True,
                status='published'
            ).select_related('category')[:6]
        )
        cache.set(cache_key, projects, 60 * 30)  # Cache for 30 minutes
    
    return projects
```

## 🔐 Security Guidelines

### Input Validation
```python
# ✅ Good - Proper input validation
from django.core.exceptions import ValidationError
import bleach

def clean_user_content(content: str) -> str:
    """Clean and validate user-generated content."""
    if not content:
        return ""
    
    # Remove potentially dangerous HTML
    allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
    cleaned_content = bleach.clean(content, tags=allowed_tags, strip=True)
    
    # Additional validation
    if len(cleaned_content) > 10000:
        raise ValidationError("Content too long")
    
    return cleaned_content
```

### Authentication & Authorization
```python
# ✅ Good - Proper permission checking
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

def is_project_owner(user, project):
    """Check if user owns the project."""
    return user.is_authenticated and project.author == user

@login_required
def edit_project(request, project_id):
    """Edit project with proper authorization."""
    project = get_object_or_404(Project, id=project_id)
    
    if not is_project_owner(request.user, project):
        raise PermissionDenied("You don't have permission to edit this project")
    
    # Process edit logic
    pass
```

## 📚 Documentation Standards

### Code Comments
```python
# ✅ Good - Meaningful comments
class ProjectAnalytics:
    """
    Analytics service for tracking project interactions.
    
    This service handles:
    - View tracking
    - Engagement metrics
    - Performance analytics
    """
    
    def track_project_view(self, project_id: int, user_id: Optional[int] = None):
        """
        Track a project view event.
        
        Args:
            project_id: ID of the viewed project
            user_id: ID of the viewing user (None for anonymous)
            
        Raises:
            ProjectNotFound: If project doesn't exist
            AnalyticsError: If tracking fails
        """
        try:
            # Complex logic needs explanation
            # We batch analytics events to reduce database load
            # and process them asynchronously every 5 minutes
            self._queue_analytics_event('project_view', {
                'project_id': project_id,
                'user_id': user_id,
                'timestamp': timezone.now(),
                'session_id': self._get_session_id()
            })
        except Exception as e:
            logger.error(f"Failed to track project view: {e}")
            raise AnalyticsError("Tracking failed")
```

### API Documentation
```python
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of published projects",
    responses={
        200: openapi.Response(
            description="List of projects",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(ref='#/definitions/Project')
                    )
                }
            )
        )
    }
)
@api_view(['GET'])
def project_list_api(request):
    """API endpoint for project list."""
    pass
```

## ✅ Code Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Input validation present

### Code Quality
- [ ] Follows coding standards
- [ ] DRY principle applied
- [ ] SOLID principles followed
- [ ] Proper naming conventions

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Efficient algorithms
- [ ] Database indexes considered

### Security
- [ ] Input sanitized
- [ ] Authentication/authorization correct
- [ ] No sensitive data exposed
- [ ] CSRF protection in place

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Edge cases tested
- [ ] Test coverage adequate

### Documentation
- [ ] Code comments added
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Breaking changes documented

## 🛠 Tools and Automation

### Code Quality Tools

#### Pre-commit Configuration (`.pre-commit-config.yaml`)
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs]
```

#### Development Dependencies (`requirements-dev.txt`)
```
# Code Quality
black==23.7.0
isort==5.12.0
flake8==6.0.0
flake8-docstrings==1.7.0
mypy==1.5.1
django-stubs==4.2.3

# Testing
pytest==7.4.0
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.3.0

# Performance
django-debug-toolbar==4.1.0
django-silk==5.0.3

# Documentation
sphinx==7.1.2
sphinx-rtd-theme==1.3.0
```

### CI/CD Pipeline (`.github/workflows/ci.yml`)
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: portfolio_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linters
      run: |
        black --check .
        isort --check-only .
        flake8 .
        mypy .
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Quality Metrics
- **Code Coverage**: Minimum 80%
- **Cyclomatic Complexity**: Maximum 10 per function
- **Line Length**: Maximum 88 characters
- **Function Length**: Maximum 50 lines
- **Class Length**: Maximum 500 lines

## 📊 Monitoring and Metrics

### Performance Monitoring
```python
# monitoring.py
import time
import logging
from functools import wraps
from django.db import connection

logger = logging.getLogger(__name__)

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        query_count_start = len(connection.queries)
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            query_count_end = len(connection.queries)
            
            execution_time = end_time - start_time
            query_count = query_count_end - query_count_start
            
            if execution_time > 1.0:  # Log slow functions
                logger.warning(
                    f"Slow function: {func.__name__} took {execution_time:.2f}s "
                    f"with {query_count} queries"
                )
    
    return wrapper
```

### Code Quality Metrics Dashboard
Track and visualize:
- Test coverage trends
- Code complexity metrics
- Performance benchmarks
- Security scan results
- Dependency vulnerabilities

Remember: **Quality is not an act, it's a habit.** 

---

Following these guidelines ensures our codebase remains maintainable, secure, and performant as the project grows.