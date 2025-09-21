from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

# Import all models from your models.py
from .models import (
    Skill, Experience, Project, Blog, FAQ, Category,
    NewsletterSubscriber, Comment, ProjectComment, Achievement, 
    SiteConfiguration, Resume, VideoResume, AboutMeConfiguration,
    CodeTogetherConfiguration, CollaborationProposal, Testimonial,
    Resource, Technology, ContactSubmission, ResourceView,
    CommentLike, ProjectCommentLike, ResourcesConfiguration, ResourceCategory
)

# Import all forms from your forms.py
from .forms import ContactForm, NewsletterForm, CollaborationProposalForm, ResourceFilterForm


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
        services = Skill.objects.order_by('order')
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
    """View for a single project detail page with comment functionality."""
    model = Project
    template_name = 'project-dtl.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get initial 5 comments for display
        initial_comments = project.comments.filter(is_approved=True).order_by('-created_date')[:5]
        context['comments'] = initial_comments
        
        # Add user's liked comments for proper state management
        if self.request.user.is_authenticated:
            user_liked_comments = ProjectCommentLike.objects.filter(
                user=self.request.user,
                comment__in=initial_comments
            ).values_list('comment_id', flat=True)
            context['user_liked_comments'] = list(user_liked_comments)
        else:
            context['user_liked_comments'] = []
        
        # Check if there are more comments beyond the initial 5
        total_comments_count = project.comments.filter(is_approved=True).count()
        context['has_more_comments'] = total_comments_count > 5
        context['total_comments'] = total_comments_count
        
        return context

    def post(self, request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            project = self.get_object()
            login_url = reverse('auth_app:login') + f'?next={reverse("portfolio:project_detail", kwargs={"slug": project.slug})}%23comments'
            return HttpResponseRedirect(login_url)
        
        project = self.get_object()
        body = request.POST.get('body')

        redirect_url = reverse('portfolio:project_detail', kwargs={'slug': project.slug}) + '#comments'
        response = HttpResponseRedirect(redirect_url)

        if body:
            # Create comment with authenticated user's name
            author_name = request.user.first_name or request.user.username
            ProjectComment.objects.create(project=project, author_name=author_name, body=body)
            messages.success(request, "Your comment has been posted and is awaiting approval.")
        else:
            messages.error(request, "Please enter your comment.")
            
        return response


def load_more_project_comments(request, slug):
    """AJAX view to load more project comments."""
    if request.method == 'GET':
        project = get_object_or_404(Project, slug=slug)
        offset = int(request.GET.get('offset', 0))
        
        # Load 10 comments starting from the offset
        comments = project.comments.filter(is_approved=True).order_by('-created_date')[offset:offset+10]
        total_comments = project.comments.filter(is_approved=True).count()
        
        # Get user's liked comments if authenticated
        user_liked_comments = []
        if request.user.is_authenticated:
            user_liked_comments = ProjectCommentLike.objects.filter(
                user=request.user,
                comment__in=comments
            ).values_list('comment_id', flat=True)
            user_liked_comments = list(user_liked_comments)
        
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'author_name': comment.author_name,
                'body': comment.body,
                'likes': comment.total_likes,  # Use the new property
                'is_liked': comment.id in user_liked_comments,
                'created_at': comment.created_date.strftime('%B %d, %Y at %I:%M %p'),
            })
        
        return JsonResponse({
            'comments': comments_data,
            'has_more': total_comments > (offset + 10)
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
        
        # Add user's liked comments for proper state management
        if self.request.user.is_authenticated:
            user_liked_comments = CommentLike.objects.filter(
                user=self.request.user,
                comment__in=context['comments']
            ).values_list('comment_id', flat=True)
            context['user_liked_comments'] = list(user_liked_comments)
        else:
            context['user_liked_comments'] = []
        
        post_categories = post.categories.all()
        context['suggested_posts'] = Blog.objects.filter(categories__in=post_categories)\
                                                 .exclude(pk=post.pk)\
                                                 .distinct()\
                                                 .order_by('-created_date')[:2]
        return context

    def post(self, request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            post = self.get_object()
            login_url = reverse('auth_app:login') + f'?next={reverse("portfolio:blog_detail", kwargs={"slug": post.slug})}%23comments'
            return HttpResponseRedirect(login_url)
            
        post = self.get_object()
        body = request.POST.get('body')

        redirect_url = reverse('portfolio:blog_detail', kwargs={'slug': post.slug}) + '#comments'
        response = HttpResponseRedirect(redirect_url)

        if body:
            # Create comment with authenticated user's name
            author_name = request.user.first_name or request.user.username
            Comment.objects.create(post=post, author_name=author_name, body=body)
            messages.success(request, "Your comment has been posted and is awaiting approval.")
        else:
            messages.error(request, "Please enter your comment.")
            
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


# =========================================================================
# ABOUT ME PAGE VIEW
# =========================================================================
class AboutMeView(TemplateView):
    """View for the About Me page with configuration content."""
    template_name = 'aboutme.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create AboutMe configuration
        config, created = AboutMeConfiguration.objects.get_or_create(
            defaults={
                'page_title': "A Bit More <span>About Me</span>",
                'intro_paragraph': "This is my story, my journey, and what drives me.",
                'action2_link': "https://risetogethr.tech"
            }
        )
        
        context['config'] = config
        return context


# =========================================================================
# CODE TOGETHER PAGE VIEW
# =========================================================================
class CodeTogetherView(TemplateView):
    """View for the Code Together page with form handling."""
    template_name = 'codeme.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create CodeTogether configuration
        config, created = CodeTogetherConfiguration.objects.get_or_create(
            defaults={
                'page_title': "Let's Build <span>Together</span>",
                'intro_paragraph': "I'm always excited to collaborate on innovative projects. Here's a look at what I'm passionate about building."
            }
        )
        
        # Get featured testimonials
        testimonials = Testimonial.objects.filter(is_featured=True).order_by('order', '-created_date')
        
        # Create form instance
        form = CollaborationProposalForm()
        
        context.update({
            'config': config,
            'testimonials': testimonials,
            'form': form,
        })
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission."""
        form = CollaborationProposalForm(request.POST)
        
        if form.is_valid():
            # Save the proposal
            form.save()
            
            # Add success message
            messages.success(
                request, 
                "Thank you for your proposal! I'll review it and get back to you soon."
            )
            
            # Redirect to avoid double submission
            return HttpResponseRedirect(reverse('portfolio:code_together'))
        else:
            # Form is invalid, re-render with errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


# =========================================================================
# RESOURCES PAGE VIEW
# =========================================================================
class ResourcesListView(ListView):
    """View for the Resources page with filtering and pagination."""
    model = Resource
    template_name = 'resources.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        """Filter resources based on query parameters."""
        queryset = Resource.objects.filter(is_active=True).select_related().prefetch_related(
            'categories', 'technologies'
        )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category and category != 'all':
            # Check if it's a category slug or ResourceType value
            if hasattr(Resource.ResourceType, category.upper()):
                queryset = queryset.filter(resource_type=category.upper())
            else:
                queryset = queryset.filter(categories__slug=category)
        
        # Filter by resource type
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__icontains=search) |
                Q(technologies__name__icontains=search)
            ).distinct()
        
        return queryset.order_by('order', '-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create Resources configuration
        config, created = ResourcesConfiguration.objects.get_or_create(
            defaults={
                'page_title': "My Curated <span>Resources</span>",
                'intro_paragraph': "A collection of valuable articles, tools, videos, and courses that have helped me in my development journey."
            }
        )
        
        # Get all resource types for filtering
        resource_types = Resource.ResourceType.choices
        
        # Get all resource categories for filtering
        categories = ResourceCategory.objects.all().order_by('order', 'name')
        
        # Create filter form
        filter_form = ResourceFilterForm(self.request.GET)
        
        # Track resource views (for analytics)
        self._track_page_view()
        
        context.update({
            'config': config,
            'resource_types': resource_types,
            'categories': categories,
            'filter_form': filter_form,
            'current_category': self.request.GET.get('category', 'all'),
            'current_type': self.request.GET.get('type', ''),
            'search_query': self.request.GET.get('search', ''),
        })
        return context

    def _track_page_view(self):
        """Track page views for analytics (optional)."""
        try:
            # You can implement page view tracking here if needed
            pass
        except Exception:
            # Silent fail for analytics
            pass


class ResourceDetailView(DetailView):
    """Detail view for individual resources with embed support."""
    model = Resource
    template_name = 'resource-detail.html'
    context_object_name = 'resource'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Only show active resources."""
        return Resource.objects.filter(is_active=True).select_related().prefetch_related(
            'categories', 'technologies'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Track resource view
        self._track_resource_view()
        
        # Get related resources (same categories or technologies)
        related_resources = self._get_related_resources()
        
        context.update({
            'related_resources': related_resources,
        })
        return context

    def _track_resource_view(self):
        """Track individual resource views."""
        try:
            ResourceView.objects.create(
                resource=self.object,
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')[:255]
            )
        except Exception:
            # Silent fail for analytics
            pass

    def _get_related_resources(self):
        """Get resources related to the current one."""
        try:
            # Get resources with same categories or technologies
            related = Resource.objects.filter(
                is_active=True
            ).filter(
                Q(categories__in=self.object.categories.all()) |
                Q(technologies__in=self.object.technologies.all())
            ).exclude(
                id=self.object.id
            ).distinct()[:4]
            
            return related
        except Exception:
            return Resource.objects.none()


# =========================================================================
# COMMENT LIKE VIEWS
# =========================================================================

@login_required
@require_POST
def toggle_comment_like(request, comment_id):
    """AJAX view to toggle like/unlike for blog comments."""
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=request.user
        )
        
        if not created:
            # Unlike - delete the like
            like.delete()
            liked = False
        else:
            # Like - like object was created
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'total_likes': comment.total_likes
        })
    
    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Comment not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST 
def toggle_project_comment_like(request, comment_id):
    """AJAX view to toggle like/unlike for project comments."""
    try:
        comment = get_object_or_404(ProjectComment, id=comment_id)
        like, created = ProjectCommentLike.objects.get_or_create(
            comment=comment,
            user=request.user
        )
        
        if not created:
            # Unlike - delete the like
            like.delete()
            liked = False
        else:
            # Like - like object was created
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'total_likes': comment.total_likes
        })
    
    except ProjectComment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Comment not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# =========================================================================
# LEGAL PAGES VIEWS
# =========================================================================
class PrivacyPolicyView(TemplateView):
    """View for the Privacy Policy page."""
    template_name = 'legal/privacy-policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Privacy Policy'
        context['meta_description'] = 'Privacy Policy for Roshan Damor\'s portfolio website. Learn how we collect, use, and protect your personal information.'
        return context


class TermsOfServiceView(TemplateView):
    """View for the Terms of Service page."""
    template_name = 'legal/terms-of-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Terms of Service'
        context['meta_description'] = 'Terms of Service for Roshan Damor\'s portfolio website. Please read these terms carefully before using our services.'
        return context