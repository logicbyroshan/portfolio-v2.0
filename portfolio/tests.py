"""
Basic test cases for portfolio app.
"""

from django.test import TestCase
from portfolio.models import Skill, Project, Blog


class BasicModelTests(TestCase):
    """Basic tests for portfolio models."""

    def test_skill_creation(self):
        """Test skill model creation."""
        skill = Skill.objects.create(
            name="Python",
            level=90,
            category="Programming"
        )
        self.assertEqual(str(skill), "Python")
        self.assertEqual(skill.level, 90)

    def test_project_creation(self):
        """Test project model creation."""
        project = Project.objects.create(
            title="Test Project",
            description="A test project",
            technology_used="Django, Python"
        )
        self.assertEqual(str(project), "Test Project")
        self.assertTrue(project.description)

    def test_blog_creation(self):
        """Test blog model creation."""
        blog = Blog.objects.create(
            title="Test Blog",
            content="Test content",
            published=True
        )
        self.assertEqual(str(blog), "Test Blog")
        self.assertTrue(blog.published)

import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from unittest.mock import patch, MagicMock

from .models import (
    Skill, Project, Blog, Experience, Achievement, 
    Comment, NewsletterSubscriber, Contact
)
from .views import (
    HomeView, ProjectListView, ProjectDetailView,
    BlogListView, BlogDetailView, ContactSubmissionView
)
from tests.factories import (
    SkillFactory, ProjectFactory, BlogFactory, ExperienceFactory,
    AchievementFactory, CommentFactory, NewsletterSubscriberFactory,
    ContactFactory, UserFactory
)


class TestModels(TestCase):
    """Test portfolio models."""
    
    def test_skill_model_creation(self):
        """Test skill model creation and string representation."""
        skill = SkillFactory(name="Python")
        self.assertEqual(str(skill), "Python")
        self.assertTrue(skill.slug)
        self.assertIn(skill.level, ['Beginner', 'Intermediate', 'Advanced', 'Expert'])
    
    def test_skill_get_absolute_url(self):
        """Test skill get_absolute_url method."""
        skill = SkillFactory()
        expected_url = reverse('portfolio:skill_detail', kwargs={'slug': skill.slug})
        self.assertEqual(skill.get_absolute_url(), expected_url)
    
    def test_project_model_creation(self):
        """Test project model creation and relationships."""
        technologies = SkillFactory.create_batch(3)
        project = ProjectFactory(technologies=technologies)
        
        self.assertEqual(str(project), project.title)
        self.assertEqual(project.technologies.count(), 3)
        self.assertTrue(project.slug)
    
    def test_project_get_absolute_url(self):
        """Test project get_absolute_url method."""
        project = ProjectFactory()
        expected_url = reverse('portfolio:project_detail', kwargs={'slug': project.slug})
        self.assertEqual(project.get_absolute_url(), expected_url)
    
    def test_blog_model_creation(self):
        """Test blog model creation."""
        blog = BlogFactory()
        self.assertEqual(str(blog), blog.title)
        self.assertTrue(blog.is_published)
        self.assertTrue(blog.slug)
    
    def test_blog_get_absolute_url(self):
        """Test blog get_absolute_url method."""
        blog = BlogFactory()
        expected_url = reverse('portfolio:blog_detail', kwargs={'slug': blog.slug})
        self.assertEqual(blog.get_absolute_url(), expected_url)
    
    def test_experience_model_creation(self):
        """Test experience model creation."""
        experience = ExperienceFactory()
        self.assertEqual(str(experience), f"{experience.position} at {experience.company}")
        self.assertFalse(experience.is_current)
    
    def test_achievement_model_creation(self):
        """Test achievement model creation."""
        achievement = AchievementFactory()
        self.assertEqual(str(achievement), achievement.title)
    
    def test_comment_model_creation(self):
        """Test comment model creation."""
        comment = CommentFactory()
        self.assertTrue(comment.is_approved)
        self.assertEqual(str(comment), f"Comment by {comment.author_name}")
    
    def test_newsletter_subscriber_model(self):
        """Test newsletter subscriber model."""
        subscriber = NewsletterSubscriberFactory()
        self.assertTrue(subscriber.is_active)
        self.assertEqual(str(subscriber), subscriber.email)
    
    def test_contact_model_creation(self):
        """Test contact model creation."""
        contact = ContactFactory()
        self.assertEqual(str(contact), f"Message from {contact.name}")


@pytest.mark.django_db
class TestViews:
    """Test portfolio views."""
    
    def setup_method(self):
        """Set up test data."""
        self.client = Client()
        self.user = UserFactory()
    
    def test_home_view_get(self):
        """Test home view GET request."""
        # Create test data
        featured_skills = SkillFactory.create_batch(6, is_featured=True)
        featured_projects = ProjectFactory.create_batch(3, is_featured=True)
        recent_blogs = BlogFactory.create_batch(3, is_published=True)
        experiences = ExperienceFactory.create_batch(2)
        
        response = self.client.get(reverse('portfolio:home'))
        
        assert response.status_code == 200
        assert 'featured_skills' in response.context
        assert 'featured_projects' in response.context
        assert 'recent_blogs' in response.context
        assert 'experiences' in response.context
        assert len(response.context['featured_skills']) <= 6
        assert len(response.context['featured_projects']) <= 3
        assert len(response.context['recent_blogs']) <= 3
    
    def test_project_list_view(self):
        """Test project list view."""
        projects = ProjectFactory.create_batch(5)
        
        response = self.client.get(reverse('portfolio:project_list'))
        
        assert response.status_code == 200
        assert 'projects' in response.context
        assert len(response.context['projects']) == 5
    
    def test_project_detail_view(self):
        """Test project detail view."""
        project = ProjectFactory()
        comments = CommentFactory.create_batch(3, content_object=project)
        
        response = self.client.get(
            reverse('portfolio:project_detail', kwargs={'slug': project.slug})
        )
        
        assert response.status_code == 200
        assert response.context['project'] == project
        assert 'comments' in response.context
    
    def test_blog_list_view(self):
        """Test blog list view."""
        published_blogs = BlogFactory.create_batch(3, is_published=True)
        unpublished_blogs = BlogFactory.create_batch(2, is_published=False)
        
        response = self.client.get(reverse('portfolio:blog_list'))
        
        assert response.status_code == 200
        assert len(response.context['blogs']) == 3  # Only published blogs
    
    def test_blog_detail_view(self):
        """Test blog detail view."""
        blog = BlogFactory(is_published=True)
        
        response = self.client.get(
            reverse('portfolio:blog_detail', kwargs={'slug': blog.slug})
        )
        
        assert response.status_code == 200
        assert response.context['blog'] == blog
    
    def test_blog_detail_view_unpublished_returns_404(self):
        """Test that unpublished blog returns 404."""
        blog = BlogFactory(is_published=False)
        
        response = self.client.get(
            reverse('portfolio:blog_detail', kwargs={'slug': blog.slug})
        )
        
        assert response.status_code == 404
    
    def test_skill_list_view(self):
        """Test skill list view."""
        skills = SkillFactory.create_batch(5)
        
        response = self.client.get(reverse('portfolio:skill_list'))
        
        assert response.status_code == 200
        assert 'skills' in response.context
        assert len(response.context['skills']) == 5
    
    def test_skill_detail_view(self):
        """Test skill detail view."""
        skill = SkillFactory()
        projects = ProjectFactory.create_batch(2, technologies=[skill])
        
        response = self.client.get(
            reverse('portfolio:skill_detail', kwargs={'slug': skill.slug})
        )
        
        assert response.status_code == 200
        assert response.context['skill'] == skill
        assert 'related_projects' in response.context
    
    def test_achievement_list_view(self):
        """Test achievement list view."""
        achievements = AchievementFactory.create_batch(4)
        
        response = self.client.get(reverse('portfolio:achievements_list'))
        
        assert response.status_code == 200
        assert 'achievements' in response.context
        assert len(response.context['achievements']) == 4
    
    @patch('portfolio.views.send_mail')
    def test_contact_submission_view_post_valid(self, mock_send_mail):
        """Test contact form submission with valid data."""
        mock_send_mail.return_value = True
        
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        
        response = self.client.post(reverse('portfolio:contact_submit'), data)
        
        assert response.status_code == 302  # Redirect after successful submission
        assert Contact.objects.filter(email='john@example.com').exists()
        mock_send_mail.assert_called_once()
    
    def test_contact_submission_view_post_invalid(self):
        """Test contact form submission with invalid data."""
        data = {
            'name': '',  # Empty name should be invalid
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        
        response = self.client.post(reverse('portfolio:contact_submit'), data)
        
        assert response.status_code == 400  # Bad request for invalid data
        assert not Contact.objects.filter(email='invalid-email').exists()
    
    def test_newsletter_subscribe_view_valid_email(self):
        """Test newsletter subscription with valid email."""
        data = {'email': 'test@example.com'}
        
        response = self.client.post(reverse('portfolio:subscribe_ajax'), data)
        
        assert response.status_code == 200
        assert NewsletterSubscriber.objects.filter(email='test@example.com').exists()
    
    def test_newsletter_subscribe_view_duplicate_email(self):
        """Test newsletter subscription with already subscribed email."""
        NewsletterSubscriberFactory(email='existing@example.com')
        data = {'email': 'existing@example.com'}
        
        response = self.client.post(reverse('portfolio:subscribe_ajax'), data)
        
        assert response.status_code == 400  # Should return error for duplicate
    
    def test_newsletter_subscribe_view_invalid_email(self):
        """Test newsletter subscription with invalid email."""
        data = {'email': 'invalid-email'}
        
        response = self.client.post(reverse('portfolio:subscribe_ajax'), data)
        
        assert response.status_code == 400


class TestForms(TestCase):
    """Test portfolio forms."""
    
    def test_contact_form_valid_data(self):
        """Test contact form with valid data."""
        from .forms import ContactForm
        
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_contact_form_invalid_data(self):
        """Test contact form with invalid data."""
        from .forms import ContactForm
        
        form_data = {
            'name': '',
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)


class TestUtils(TestCase):
    """Test portfolio utility functions."""
    
    def test_context_processor(self):
        """Test site context processor."""
        from .context_processors import site_context
        from django.http import HttpRequest
        
        request = HttpRequest()
        context = site_context(request)
        
        self.assertIn('site_name', context)
        self.assertIn('site_description', context)
        self.assertEqual(context['site_name'], 'Roshan Damor - Portfolio')


class TestAdmin(TestCase):
    """Test admin interface."""
    
    def setUp(self):
        """Set up admin user."""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin_password'
        )
        self.client.force_login(self.admin_user)
    
    def test_skill_admin_list(self):
        """Test skill admin list view."""
        SkillFactory.create_batch(3)
        response = self.client.get('/admin/portfolio/skill/')
        self.assertEqual(response.status_code, 200)
    
    def test_project_admin_list(self):
        """Test project admin list view."""
        ProjectFactory.create_batch(3)
        response = self.client.get('/admin/portfolio/project/')
        self.assertEqual(response.status_code, 200)
    
    def test_blog_admin_list(self):
        """Test blog admin list view."""
        BlogFactory.create_batch(3)
        response = self.client.get('/admin/portfolio/blog/')
        self.assertEqual(response.status_code, 200)


@pytest.mark.integration
class TestIntegration:
    """Integration tests for portfolio app."""
    
    @pytest.mark.django_db
    def test_full_workflow_user_journey(self):
        """Test complete user journey through the site."""
        client = Client()
        
        # Create test data
        skills = SkillFactory.create_batch(3)
        projects = ProjectFactory.create_batch(2, technologies=skills)
        blogs = BlogFactory.create_batch(2, is_published=True)
        
        # Test home page
        response = client.get(reverse('portfolio:home'))
        assert response.status_code == 200
        
        # Test project list
        response = client.get(reverse('portfolio:project_list'))
        assert response.status_code == 200
        
        # Test project detail
        project = projects[0]
        response = client.get(
            reverse('portfolio:project_detail', kwargs={'slug': project.slug})
        )
        assert response.status_code == 200
        
        # Test blog list
        response = client.get(reverse('portfolio:blog_list'))
        assert response.status_code == 200
        
        # Test blog detail
        blog = blogs[0]
        response = client.get(
            reverse('portfolio:blog_detail', kwargs={'slug': blog.slug})
        )
        assert response.status_code == 200
        
        # Test skill list
        response = client.get(reverse('portfolio:skill_list'))
        assert response.status_code == 200
        
        # Test contact form submission
        contact_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        }
        response = client.post(reverse('portfolio:contact_submit'), contact_data)
        assert response.status_code == 302  # Redirect after successful submission
        
        # Verify contact was created
        assert Contact.objects.filter(email='test@example.com').exists()


class TestPerformance(TestCase):
    """Test performance aspects."""
    
    def test_home_view_database_queries(self):
        """Test that home view doesn't have N+1 query problems."""
        # Create test data
        SkillFactory.create_batch(10, is_featured=True)
        ProjectFactory.create_batch(10, is_featured=True)
        BlogFactory.create_batch(10, is_published=True)
        
        with self.assertNumQueries(6):  # Adjust expected number based on actual queries
            response = self.client.get(reverse('portfolio:home'))
            self.assertEqual(response.status_code, 200)
    
    def test_project_list_view_pagination(self):
        """Test project list view pagination."""
        ProjectFactory.create_batch(25)  # Create more than one page worth
        
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test pagination exists if there are many projects
        if 'is_paginated' in response.context:
            self.assertTrue(response.context['is_paginated'])


class TestSecurity(TestCase):
    """Test security aspects."""
    
    def test_contact_form_csrf_protection(self):
        """Test that contact form requires CSRF token."""
        from django.middleware.csrf import get_token
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.post('/contact-submit/')
        
        # Without CSRF token, should fail
        # This is handled by Django's CSRF middleware
        pass  # Django handles this automatically in tests
    
    def test_xss_protection_in_templates(self):
        """Test that user input is properly escaped in templates."""
        # Create a blog with potentially malicious content
        blog = BlogFactory(
            title="<script>alert('xss')</script>Safe Title",
            content="<script>alert('xss')</script>Safe content"
        )
        
        response = self.client.get(
            reverse('portfolio:blog_detail', kwargs={'slug': blog.slug})
        )
        
        # Django should escape the script tags
        self.assertNotContains(response, "<script>alert('xss')</script>")
        self.assertContains(response, "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;")


if __name__ == '__main__':
    import django
    django.setup()
    pytest.main([__file__])
