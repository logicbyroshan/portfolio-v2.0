from django.urls import path
from .views import (
    # Page Views
    HomeView, SkillListView,
    ProjectListView, ProjectDetailView,
    BlogListView, BlogDetailView,
    ExperienceListView, ExperienceDetailView,
    SkillDetailView, AchievementListView,
    AboutMeView, CodeTogetherView,
    ResourcesListView, ResourceDetailView,

    # Legal Pages
    PrivacyPolicyView, TermsOfServiceView,

    # Form/API Views
    ContactSubmissionView,
    NewsletterSubscribeHomeView,
    NewsletterSubscribeAjaxView,
    load_more_project_comments,
    
    # Like Toggle Views
    toggle_comment_like,
    toggle_project_comment_like
)

app_name = 'portfolio'

urlpatterns = [
    # Home Page
    path('', HomeView.as_view(), name='home'),
    
    # About Me Page
    path('about/', AboutMeView.as_view(), name='about_me'),
    
    # Code Together Page
    path('code-together/', CodeTogetherView.as_view(), name='code_together'),
    
    # Resources Pages
    path('resources/', ResourcesListView.as_view(), name='resource_list'),
    path('resources/<slug:slug>/', ResourceDetailView.as_view(), name='resource_detail'),

    # Project Pages
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<slug:slug>/load-more-comments/', load_more_project_comments, name='load_more_project_comments'),

    # Blog Pages
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),

    # Experience Pages
    path('experience/', ExperienceListView.as_view(), name='experience_list'),
    path('experience/<int:pk>/', ExperienceDetailView.as_view(), name='experience_detail'),
    
    # Skill Detail Page
    path('skills/', SkillListView.as_view(), name='skill_list'),
    path('skills/<slug:slug>/', SkillDetailView.as_view(), name='skill_detail'),

    # Form Submission URLs
    path('contact-submit/', ContactSubmissionView.as_view(), name='contact_submit'),
    path('subscribe-home/', NewsletterSubscribeHomeView.as_view(), name='subscribe_home'),
    path('subscribe/', NewsletterSubscribeAjaxView.as_view(), name='subscribe_ajax'),
    path('achievements/', AchievementListView.as_view(), name='achievements_list'),
    
    # Legal Pages
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    
    # Like Toggle URLs
    path('blog/comment/<int:comment_id>/like/', toggle_comment_like, name='toggle_comment_like'),
    path('project/comment/<int:comment_id>/like/', toggle_project_comment_like, name='toggle_project_comment_like'),

]