from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Blog.objects.all().order_by('-created_date')

    def lastmod(self, obj):
        return obj.created_date

    def location(self, obj):
        return reverse('blog:blog_detail', kwargs={'slug': obj.slug})