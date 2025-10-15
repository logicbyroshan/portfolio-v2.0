from django.urls import path
from .views import BlogListView, BlogDetailView, toggle_comment_like

app_name = 'blog'

urlpatterns = [
    # Blog Pages
    path('', BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    
    # AJAX endpoints
    path('comment/<int:comment_id>/like/', toggle_comment_like, name='toggle_comment_like'),
]