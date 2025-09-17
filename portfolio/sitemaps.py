from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog, Project


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'portfolio:home',
            'portfolio:about_me',
            'portfolio:project_list',
            'portfolio:blog_list',
            'portfolio:skill_list',
            'portfolio:experience_list',
            'portfolio:achievements_list',
            'portfolio:code_together',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Blog.objects.all().order_by('-created_date')

    def lastmod(self, obj):
        return obj.created_date

    def location(self, obj):
        return reverse('portfolio:blog_detail', kwargs={'slug': obj.slug})


class ProjectSitemap(Sitemap):
    """Sitemap for projects"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.all().order_by('-created_date')

    def lastmod(self, obj):
        return obj.created_date

    def location(self, obj):
        return reverse('portfolio:project_detail', kwargs={'slug': obj.slug})