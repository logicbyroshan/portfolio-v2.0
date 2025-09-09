from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.db import models

# Import all models from your models.py
from .models import (
    Skill, Experience, Project, Blog, FAQ, Category, Technology, 
    NewsletterSubscriber, Comment, Service, Achievement, 
    SiteConfiguration, Resume, VideoResume
)

# Import all forms from your forms.py
from .forms import ContactForm, NewsletterForm


# =========================================================================
# HOME PAGE VIEW
# =========================================================================
class HomeView(TemplateView):
    """View for the homepage. Gathers context from multiple models."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Note: config, resume, and video_resume are now available globally 
        # via the site_context context processor

        # =================================================================
        # NEW & UPDATED: Services with Dynamic Animation Delay
        # =================================================================
        services = Service.objects.order_by('order')
        services_col1 = list(services[:2]) # Convert queryset slice to list
        services_col2 = list(services[2:4])

        # Add the calculated delay to each service object in the first column
        for i, service in enumerate(services_col1):
            service.animation_delay = (i + 1) * 200 # Results in 200, 400, 600

        for i, service in enumerate(services_col2):
            service.animation_delay = (i + 1) * 200 # Results in 200, 400, 600
        
        context['services_col1'] = services_col1
        context['services_col2'] = services_col2


        # =================================================================
        # Fetch data for the rest of the homepage sections
        # =================================================================
        context['skills'] = Skill.objects.all()
        context['experiences'] = Experience.objects.order_by('-start_date')[:2]
        context['projects'] = Project.objects.order_by('-created_date')[:3]
        context['blogs'] = Blog.objects.order_by('-created_date')[:3]
        context['faqs'] = FAQ.objects.order_by('order')
        
        return context

# =========================================================================
# PROJECT VIEWS
# =========================================================================
class ProjectListView(ListView):
    """View for the main projects list page with filtering and pagination."""
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(categories__slug=category_slug, categories__category_type='PRO')
        
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_date')
        else:
            queryset = queryset.order_by('-created_date')
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(category_type=Category.CategoryType.PROJECT)
        return context

class ProjectDetailView(DetailView):
    """View for a single project detail page."""
    model = Project
    template_name = 'project-dtl.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# =========================================================================
# BLOG VIEWS
# =========================================================================
class BlogListView(ListView):
    """View for the main blog list page with filtering and pagination."""
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(categories__slug=category_slug, categories__category_type='BLG')
        
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_date')
        else:
            queryset = queryset.order_by('-created_date')
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(category_type=Category.CategoryType.BLOG)
        return context

class BlogDetailView(DetailView):
    """Handles GET for viewing and POST for commenting."""
    model = Blog
    template_name = 'blog-dtl.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(is_approved=True)
        post_categories = post.categories.all()
        context['suggested_posts'] = Blog.objects.filter(categories__in=post_categories)\
                                                 .exclude(pk=post.pk)\
                                                 .distinct()\
                                                 .order_by('-created_date')[:2]
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        author_name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')

        redirect_url = reverse('portfolio:blog_detail', kwargs={'slug': post.slug}) + '#comments'
        response = HttpResponseRedirect(redirect_url)

        if author_name and email and body:
            # Create comment directly without newsletter subscription requirement
            Comment.objects.create(post=post, author_name=author_name, body=body)
            messages.success(request, "Your comment has been posted and is awaiting approval.")
        else:
            messages.error(request, "Please fill in all the required fields to comment.")
            
        return response


# =========================================================================
# EXPERIENCE VIEWS
# =========================================================================
class ExperienceListView(ListView):
    """View for the main experience list page."""
    model = Experience
    template_name = 'experience.html'
    context_object_name = 'experiences'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        exp_type = self.request.GET.get('category')
        if exp_type and exp_type != 'all':
            queryset = queryset.filter(experience_type=exp_type)

        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('start_date')
        else:
            queryset = queryset.order_by('-start_date')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experience_types'] = Experience.ExperienceType.choices
        return context

class ExperienceDetailView(DetailView):
    """View for a single experience dtl page."""
    model = Experience
    template_name = 'experience-dtl.html'
    context_object_name = 'experience'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experience = self.get_object()
        # Get related experiences (excluding current one, limit to 3)
        context['related_experiences'] = Experience.objects.exclude(
            id=experience.id
        ).order_by('-start_date')[:3]
        return context


# =========================================================================
# SKILL DETAIL VIEW
# =========================================================================
class SkillDetailView(DetailView):
    """View for a single skill dtl page, showing related projects."""
    model = Skill
    template_name = 'skill-dtl.html'
    context_object_name = 'skill'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = self.get_object()
        skill_technologies = skill.technologies.all()
        context['related_projects'] = Project.objects.filter(technologies__in=skill_technologies)\
                                                      .distinct()\
                                                      .order_by('-created_date')[:2]
        return context


# =========================================================================
# FORM HANDLING & API-LIKE VIEWS
# =========================================================================
class ContactSubmissionView(View):
    """Handles the submission of the main contact form."""
    def post(self, request, *args, **kwargs):
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success', 
                    'message': "Thank you for your message! I'll get back to you soon."
                })
            else:
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        errors.append(f"{field}: {error}")
                return JsonResponse({
                    'status': 'error', 
                    'message': "Please check the fields: " + ", ".join(errors)
                }, status=400)
        else:
            # Fallback for non-AJAX requests
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you for your message! I'll get back to you soon.")
            else:
                messages.error(request, "There was an error. Please check the fields and try again.")
            return redirect(reverse('portfolio:home') + '#contact')

class NewsletterSubscribeHomeView(View):
    """Handles the submission of the newsletter form on the homepage."""
    def post(self, request, *args, **kwargs):
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = NewsletterForm(request.POST)
            if form.is_valid():
                subscriber, created = NewsletterSubscriber.objects.get_or_create(email=form.cleaned_data['email'])
                if created:
                    return JsonResponse({
                        'status': 'success', 
                        'message': "Thanks for subscribing! You'll receive updates soon."
                    })
                else:
                    return JsonResponse({
                        'status': 'info', 
                        'message': "You are already subscribed!"
                    })
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': "Please provide a valid email address."
                }, status=400)
        else:
            # Fallback for non-AJAX requests
            form = NewsletterForm(request.POST)
            if form.is_valid():
                subscriber, created = NewsletterSubscriber.objects.get_or_create(email=form.cleaned_data['email'])
                if created:
                    messages.success(request, "Thanks for subscribing!")
                else:
                    messages.info(request, "You are already subscribed!")
            else:
                messages.error(request, "Please provide a valid email address.")
            return redirect(reverse('portfolio:home') + '#newsletter')

class NewsletterSubscribeAjaxView(View):
    """Handles AJAX requests for newsletter subscriptions from the modal."""
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if not email or '@' not in email or '.' not in email:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        
        if created:
            message = 'Thank you for subscribing!'
        else:
            message = 'You are already subscribed!'
            
        return JsonResponse({'success': True, 'message': message})

class AchievementListView(ListView):
    model = Achievement
    template_name = 'achievements.html'
    context_object_name = 'achievements'
    paginate_by = 6  # Show 6 achievements per page

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering by category
        category = self.request.GET.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)
            
        # Sorting
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('date_issued')
        else: # Default to newest
            queryset = queryset.order_by('-date_issued')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the category choices to the template for the filter toolbar
        context['achievement_types'] = Achievement.AchievementType.choices
        return context


class SkillListView(ListView):
    model = Skill
    template_name = 'skills.html'
    context_object_name = 'skills'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering by category (if specified)
        category = self.request.GET.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)
            
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(summary__icontains=search)
            )
            
        # Sorting
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by == 'newest':
            queryset = queryset.order_by('-id', 'title')  # Using id as proxy for creation date
        else: # Default to alphabetical
            queryset = queryset.order_by('title')
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add available skill categories for filtering
        context['skill_categories'] = Skill.SkillCategory.choices
        return context