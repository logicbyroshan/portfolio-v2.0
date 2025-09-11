"""
Basic test cases for AI app.
"""

from django.test import TestCase
from ai.models import AIQuery


class BasicAITests(TestCase):
    """Basic tests for AI models."""

    def test_ai_query_creation(self):
        """Test AI query model creation."""
        query = AIQuery.objects.create(
            query_text="What is Python?",
            response_text="Python is a programming language."
        )
        self.assertEqual(str(query), "What is Python?")
        self.assertTrue(query.response_text)

import pytest
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import AIQuery
from .views import AIQuerySubmitView
from tests.factories import AIQueryFactory, UserFactory


class TestAIModels(TestCase):
    """Test AI app models."""
    
    def test_ai_query_model_creation(self):
        """Test AIQuery model creation and string representation."""
        query = AIQueryFactory(query_text="What is Python?")
        
        self.assertEqual(str(query), "What is Python?")
        self.assertTrue(query.created_at)
        self.assertTrue(query.user_ip)
    
    def test_ai_query_model_validation(self):
        """Test AIQuery model validation."""
        # Test empty query validation
        with self.assertRaises(ValidationError):
            query = AIQuery(query_text="", user_ip="127.0.0.1")
            query.full_clean()
    
    def test_ai_query_ordering(self):
        """Test AIQuery model ordering."""
        query1 = AIQueryFactory()
        query2 = AIQueryFactory()
        
        queries = AIQuery.objects.all()
        # Should be ordered by created_at descending
        self.assertEqual(queries.first().created_at >= queries.last().created_at, True)


@pytest.mark.django_db
class TestAIViews:
    """Test AI app views."""
    
    def setup_method(self):
        """Set up test data."""
        self.client = Client()
    
    @patch('ai.views.get_gemini_response')
    def test_ai_query_submit_view_post_valid(self, mock_gemini):
        """Test AI query submission with valid data."""
        mock_gemini.return_value = "This is a test response from Gemini"
        
        data = {
            'query': 'What is machine learning?'
        }
        
        response = self.client.post(
            reverse('ai:submit_ai_query'),
            data,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert AIQuery.objects.filter(query_text='What is machine learning?').exists()
        
        response_data = response.json()
        assert 'response' in response_data
        assert response_data['response'] == "This is a test response from Gemini"
        
        mock_gemini.assert_called_once_with('What is machine learning?')
    
    def test_ai_query_submit_view_post_invalid(self):
        """Test AI query submission with invalid data."""
        data = {
            'query': ''  # Empty query
        }
        
        response = self.client.post(
            reverse('ai:submit_ai_query'),
            data,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert not AIQuery.objects.filter(query_text='').exists()
    
    def test_ai_query_submit_view_get_not_allowed(self):
        """Test that GET requests are not allowed."""
        response = self.client.get(reverse('ai:submit_ai_query'))
        
        assert response.status_code == 405  # Method not allowed


@pytest.mark.integration
class TestAIIntegration:
    """Integration tests for AI app."""
    
    @pytest.mark.django_db
    @patch('ai.views.get_gemini_response')
    def test_complete_ai_workflow(self, mock_gemini):
        """Test complete AI query workflow."""
        client = Client()
        mock_gemini.return_value = "Detailed response about Python programming"
        
        # Submit AI query
        data = {
            'query': 'Explain Python programming to a beginner'
        }
        
        response = client.post(
            reverse('ai:submit_ai_query'),
            data,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        # Check response content
        response_data = response.json()
        assert 'response' in response_data
        assert response_data['response'] == "Detailed response about Python programming"
        
        # Verify query was saved to database
        assert AIQuery.objects.filter(
            query_text='Explain Python programming to a beginner'
        ).exists()


if __name__ == '__main__':
    import django
    django.setup()
    pytest.main([__file__])
