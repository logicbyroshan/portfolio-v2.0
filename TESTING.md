# Testing Documentation

This document provides comprehensive information about running and understanding the test suite for the Django portfolio project.

## 📋 Table of Contents

- [Testing Overview](#testing-overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Coverage Reports](#coverage-reports)
- [Writing Tests](#writing-tests)
- [Troubleshooting](#troubleshooting)

## 🎯 Testing Overview

This project uses **pytest** and **pytest-django** for comprehensive testing. The test suite covers:

- **Model tests** - Data validation and relationships
- **View tests** - HTTP responses and templates
- **Form tests** - Data validation and processing
- **API tests** - External integrations (Spotify, Gemini AI)
- **Integration tests** - Cross-app functionality
- **Security tests** - Authentication and data protection
- **Performance tests** - Load handling and optimization

## 🏗️ Test Structure

```
tests/
├── __init__.py
├── factories.py          # Test data factories
├── utils.py             # Test utilities and base classes
requirements-test.txt     # Testing dependencies
pytest.ini              # Pytest configuration

# App-specific tests
portfolio/tests.py       # Portfolio functionality
blog/tests.py           # Blog and commenting system
ai/tests.py             # AI assistant features
music/tests.py          # Spotify integration
auth_app/tests.py       # Authentication system
notifications/tests.py  # Email and notifications
roshan/tests.py         # Resources and bookmarks
```

## 🚀 Running Tests

### Prerequisites

1. **Install test dependencies:**
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Ensure virtual environment is activated:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

### Basic Commands

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=.

# Run specific app tests
pytest portfolio/tests.py
pytest blog/tests.py
pytest ai/tests.py

# Run tests by category (markers)
pytest -m models      # Only model tests
pytest -m views       # Only view tests
pytest -m api         # Only API integration tests
pytest -m security    # Only security tests
pytest -m performance # Only performance tests
```

### Advanced Usage

```bash
# Run tests and generate HTML coverage report
pytest --cov=. --cov-report=html

# Run tests with specific markers
pytest -m "models and not performance"

# Run tests and stop on first failure
pytest -x

# Run tests in parallel (faster)
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run tests matching name pattern
pytest -k "test_model"
```

## 📊 Test Categories

### 🏷️ Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.models` - Model validation and database tests
- `@pytest.mark.views` - View functionality and HTTP responses
- `@pytest.mark.forms` - Form validation and processing
- `@pytest.mark.api` - External API integration tests
- `@pytest.mark.integration` - Cross-app functionality tests
- `@pytest.mark.security` - Security and authentication tests
- `@pytest.mark.performance` - Performance and optimization tests
- `@pytest.mark.unit` - Unit tests for utilities and helpers
- `@pytest.mark.signals` - Django signals and triggers

### 📱 App-Specific Test Coverage

#### Portfolio App (`portfolio/tests.py`)
- ✅ **Models:** SiteConfiguration, Project, Category, Skill, Experience, Achievement
- ✅ **Views:** Home, about, projects, skills, experience, achievements
- ✅ **Forms:** Contact submission, admin forms
- ✅ **Integration:** Cross-app data display, caching
- ✅ **Performance:** Page load times, database queries
- ✅ **Security:** Input validation, access controls

#### Blog App (`blog/tests.py`)
- ✅ **Models:** Blog, Comment, BlogCategory with relationships
- ✅ **Views:** Blog list, detail, comment submission, RSS feeds
- ✅ **Features:** Comment moderation, search, pagination
- ✅ **SEO:** Meta tags, sitemaps, structured data
- ✅ **Performance:** Query optimization, caching strategies
- ✅ **Admin:** Content management interface

#### AI App (`ai/tests.py`)
- ✅ **API Integration:** Gemini API communication and error handling
- ✅ **Models:** AI conversations, message history, settings
- ✅ **Views:** Chat interface, conversation management
- ✅ **Security:** Input sanitization, rate limiting, token protection
- ✅ **Performance:** Response times, concurrent requests
- ✅ **Error Handling:** API failures, fallback mechanisms

#### Music App (`music/tests.py`)
- ✅ **Spotify Integration:** Current playing, playlists, recent tracks
- ✅ **Models:** Playlists, tracks, listening history, preferences
- ✅ **Real-time Updates:** Live music status, WebSocket connections
- ✅ **Caching:** API response caching, performance optimization
- ✅ **Security:** Token management, user privacy controls
- ✅ **Performance:** Large playlist handling, concurrent API calls

#### Auth App (`auth_app/tests.py`)
- ✅ **Authentication:** Login, logout, registration flows
- ✅ **User Management:** Profile creation, password changes
- ✅ **Social Auth:** Django-allauth integration (Google, GitHub)
- ✅ **Security:** Password strength, CSRF protection, session security
- ✅ **Permissions:** Role-based access, staff requirements
- ✅ **Rate Limiting:** Login attempt protection

#### Notifications App (`notifications/tests.py`)
- ✅ **Email System:** Contact forms, automated notifications
- ✅ **Models:** Notifications, email queue, user preferences
- ✅ **Integration:** Blog comments, contact forms, user actions
- ✅ **Security:** Email injection protection, spam filtering
- ✅ **Performance:** Bulk notifications, email queue processing
- ✅ **Templates:** Email rendering, multi-format support

#### Roshan App (`roshan/tests.py`)
- ✅ **Resource Management:** Bookmarks, learning resources, file uploads
- ✅ **Models:** Resources, notes, bookmarks, file storage
- ✅ **Security:** File upload validation, URL sanitization, access controls
- ✅ **Content Management:** Categorization, search, privacy settings
- ✅ **Performance:** Large content sets, search optimization
- ✅ **Integration:** Portfolio display, cross-app content

## 📈 Coverage Reports

### Generating Coverage Reports

```bash
# Terminal coverage report
pytest --cov=.

# HTML coverage report (detailed)
pytest --cov=. --cov-report=html
open htmlcov/index.html  # View in browser

# XML coverage report (for CI/CD)
pytest --cov=. --cov-report=xml

# Coverage with minimum threshold
pytest --cov=. --cov-fail-under=80
```

### Coverage Targets

- **Minimum Coverage:** 80% overall
- **Critical Areas:** 95% for models, forms, security functions
- **Integration Tests:** 70% for view coverage
- **API Tests:** 85% for external integrations

### Interpreting Coverage

```
Name                 Stmts   Miss  Cover
----------------------------------------
portfolio/models.py     45      2    96%
portfolio/views.py      67      8    88%
portfolio/forms.py      23      1    96%
blog/models.py          38      0   100%
ai/utils.py             29      5    83%
----------------------------------------
TOTAL                  892     67    92%
```

## ✍️ Writing Tests

### Test Structure

```python
"""
App-specific tests following the established pattern.
"""

import pytest
from django.test import TestCase
from tests.factories import UserFactory
from tests.utils import BaseTestCase

@pytest.mark.models
class MyModelTest(BaseTestCase):
    """Test model functionality."""
    
    def test_model_creation(self):
        """Test creating model instance."""
        # Test implementation
        pass

@pytest.mark.views
class MyViewTest(BaseTestCase):
    """Test view functionality."""
    
    def test_view_response(self):
        """Test view returns correct response."""
        # Test implementation
        pass
```

### Using Factories

```python
from tests.factories import UserFactory, BlogFactory, ProjectFactory

# Create test data
user = UserFactory(username='testuser')
blog = BlogFactory(author=user, title='Test Blog')
project = ProjectFactory(category__name='Web Development')
```

### Mocking External APIs

```python
from unittest.mock import patch, Mock

@patch('music.spotify_service.spotipy.Spotify')
def test_spotify_integration(self, mock_spotify):
    mock_spotify.return_value.current_playback.return_value = {
        'item': {'name': 'Test Song'}
    }
    # Test implementation
```

### Test Database

Tests use an in-memory SQLite database for speed:

```python
# pytest.ini configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Error: ModuleNotFoundError
# Solution: Check PYTHONPATH and ensure apps are in INSTALLED_APPS
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. Database Issues

```bash
# Error: Database table doesn't exist
# Solution: Ensure migrations are current
python manage.py makemigrations
python manage.py migrate
```

#### 3. Missing Dependencies

```bash
# Error: No module named 'pytest_django'
# Solution: Install test dependencies
pip install -r requirements-test.txt
```

#### 4. API Test Failures

```python
# Error: External API calls in tests
# Solution: Mock external services
@patch('ai.utils.genai')
def test_ai_functionality(self, mock_genai):
    # Mock implementation
    pass
```

### Performance Issues

```bash
# Slow test runs
pytest -n auto  # Run tests in parallel

# Skip slow tests during development
pytest -m "not performance"

# Use pytest-benchmark for detailed timing
pip install pytest-benchmark
```

### CI/CD Integration

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
```

## 📚 Additional Resources

### Testing Best Practices

1. **Arrange-Act-Assert:** Structure tests clearly
2. **Independent Tests:** Each test should be isolated
3. **Descriptive Names:** Use clear, descriptive test names
4. **Mock External Services:** Don't rely on external APIs in tests
5. **Test Edge Cases:** Cover both happy path and error scenarios

### Useful Commands

```bash
# Debug failing test
pytest -s -v tests/test_specific.py::TestClass::test_method

# Profile slow tests
pytest --durations=10

# Check test collection without running
pytest --collect-only

# Run tests with specific settings
pytest --ds=config.test_settings
```

### Documentation Links

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)

---

## 🎉 Conclusion

This comprehensive test suite ensures your Django portfolio project is:

- ✅ **Reliable** - Catches bugs before deployment
- ✅ **Maintainable** - Safe refactoring with test coverage
- ✅ **Secure** - Validates security measures
- ✅ **Performant** - Identifies performance bottlenecks
- ✅ **Deployment Ready** - Confidence in production deployments

Run the tests regularly during development and before any deployment to maintain code quality and catch issues early.

```bash
# Quick test run for development
pytest -x --ff

# Full test suite for deployment
pytest --cov=. --cov-fail-under=80
```

Happy testing! 🚀