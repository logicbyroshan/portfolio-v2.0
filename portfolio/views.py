from django.views.generic import TemplateView, ListView, DetailView
from .models import Skill, Experience, Project, Blog, FAQ, Category, Technology

# =========================================================================
# HOME PAGE VIEW
# =========================================================================

class HomeView(TemplateView):
    """
    View for the homepage. Gathers context from multiple models.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetching data for various sections of the homepage
        context['skills'] = Skill.objects.all()
        context['experiences'] = Experience.objects.order_by('-start_date')[:2] # Show latest 2
        context['projects'] = Project.objects.order_by('-created_date')[:3]   # Show latest 3
        context['blogs'] = Blog.objects.order_by('-created_date')[:3]         # Show latest 3
        context['faqs'] = FAQ.objects.order_by('order')[:5]
        return context


# =========================================================================
# PROJECT VIEWS
# =========================================================================

class ProjectListView(ListView):
    """
    View for the main projects list page with filtering and pagination.
    """
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    paginate_by = 6 # Show 6 projects per page

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering by category
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'newest') # Default to newest
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_date')
        else: # 'newest'
            queryset = queryset.order_by('-created_date')
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProjectDetailView(DetailView):
    """
    View for a single project detail page.
    """
    model = Project
    template_name = 'project-detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# =========================================================================
# BLOG VIEWS
# =========================================================================

class BlogListView(ListView):
    """
    View for the main blog list page with filtering and pagination.
    """
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(categories__slug=category_slug)
        
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_date')
        else:
            queryset = queryset.order_by('-created_date')
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BlogDetailView(DetailView):
    """
    View for a single blog post, including comments and suggested posts.
    """
    model = Blog
    template_name = 'blog-detail.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Fetch approved comments for the post
        context['comments'] = post.comments.filter(is_approved=True)
        
        # Fetch suggested posts from the same category, excluding the current one
        post_categories = post.categories.all()
        context['suggested_posts'] = Blog.objects.filter(categories__in=post_categories)\
                                                 .exclude(pk=post.pk)\
                                                 .distinct()\
                                                 .order_by('-created_date')[:2]
        return context


# =========================================================================
# EXPERIENCE VIEWS
# =========================================================================

class ExperienceListView(ListView):
    """
    View for the main experience list page.
    """
    model = Experience
    template_name = 'experience.html'
    context_object_name = 'experiences'
    paginate_by = 4 # Fewer items as they take more vertical space

    def get_queryset(self):
        queryset = super().get_queryset()
        exp_type = self.request.GET.get('category') # e.g., 'FT', 'IN'
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
    """
    View for a single experience detail page.
    """
    model = Experience
    template_name = 'experience-detail.html'
    context_object_name = 'experience'


# =========================================================================
# SKILL DETAIL VIEW
# =========================================================================

class SkillDetailView(DetailView):
    """
    View for a single skill detail page, showing related projects.
    """
    model = Skill
    template_name = 'skill-detail.html'
    context_object_name = 'skill'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = self.get_object()
        
        # Fetch all technologies associated with this skill
        skill_technologies = skill.technologies.all()
        
        # Fetch projects that use any of these technologies
        context['related_projects'] = Project.objects.filter(technologies__in=skill_technologies)\
                                                      .distinct()\
                                                      .order_by('-created_date')[:2]
        return context