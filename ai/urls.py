# ai/urls.py
from django.urls import path
from .views import AIQuerySubmitView

app_name = 'ai'

urlpatterns = [
    path('submit-query/', AIQuerySubmitView.as_view(), name='submit_ai_query'),
]