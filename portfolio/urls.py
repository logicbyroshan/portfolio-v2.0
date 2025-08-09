from django.urls import path
from .views import (
    HomeView,
    ProjectListView, ProjectDetailView,
    BlogListView, BlogDetailView,
    ExperienceListView, ExperienceDetailView,
    SkillDetailView,
)

app_name = 'portfolio'  # Namespacing for clarity

urlpatterns = [
    # Home Page
    path('', HomeView.as_view(), name='home'),

    # Project Pages
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),

    # Blog Pages
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),

    # Experience Pages
    path('experience/', ExperienceListView.as_view(), name='experience_list'),
    path('experience/<int:pk>/', ExperienceDetailView.as_view(), name='experience_detail'),
    
    # Skill Detail Page
    path('skills/<slug:slug>/', SkillDetailView.as_view(), name='skill_detail'),
]