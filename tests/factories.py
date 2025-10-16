"""
Test factories for creating test data.
Using factory_boy to create realistic test objects.
"""

import factory
from django.contrib.auth.models import User
from django.utils.text import slugify
from faker import Faker
from portfolio.models import (
    SiteConfiguration,
    Project,
    Category,
    Skill,
    Experience,
    Achievement,
    ContactSubmission,
    ProjectImage,
)
from blog.models import Blog, Comment
from roshan.models import AboutMeConfiguration, Resource, ResourceCategory

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True


class SiteConfigurationFactory(factory.django.DjangoModelFactory):
    """Factory for creating SiteConfiguration instances."""

    class Meta:
        model = SiteConfiguration
        django_get_or_create = ("hero_name",)

    hero_name = "Test Portfolio Owner"
    hero_leetcode_rating = "1800+"
    hero_opensource_contributions = "50+"
    hero_hackathons_count = "12+"
    twitter_url = "https://twitter.com/testuser"
    github_url = "https://github.com/testuser"
    linkedin_url = "https://linkedin.com/in/testuser"


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating Category instances."""

    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    category_type = factory.Iterator(
        Category.CategoryType.choices, getter=lambda x: x[0]
    )
    icon = factory.Faker("file_name", extension="svg")


class SkillFactory(factory.django.DjangoModelFactory):
    """Factory for creating Skill instances."""

    class Meta:
        model = Skill

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    proficiency_level = factory.Iterator(
        Skill.ProficiencyLevel.choices, getter=lambda x: x[0]
    )
    years_of_experience = factory.Faker("random_int", min=1, max=10)
    description = factory.Faker("text", max_nb_chars=200)
    icon = factory.Faker("file_name", extension="svg")
    is_featured = factory.Faker("boolean", chance_of_getting_true=30)


class ProjectFactory(factory.django.DjangoModelFactory):
    """Factory for creating Project instances."""

    class Meta:
        model = Project

    title = factory.Faker("sentence", nb_words=3)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    summary = factory.Faker("text", max_nb_chars=200)
    description = factory.Faker("text", max_nb_chars=500)
    cover_image = factory.django.FileField(filename="project_cover.jpg")
    github_url = factory.LazyAttribute(
        lambda obj: f"https://github.com/testuser/{obj.slug}"
    )
    live_url = factory.LazyAttribute(lambda obj: f"https://{obj.slug}.example.com")
    start_date = factory.Faker("date_between", start_date="-2y", end_date="today")
    end_date = factory.LazyAttribute(
        lambda obj: (
            fake.date_between(start_date=obj.start_date, end_date="today")
            if fake.boolean(chance_of_getting_true=70)
            else None
        )
    )
    is_featured = factory.Faker("boolean", chance_of_getting_true=40)
    is_published = True
    order = factory.Sequence(lambda n: n)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            # Create default categories if none provided
            project_categories = CategoryFactory.create_batch(
                2, category_type=Category.CategoryType.PROJECT
            )
            for category in project_categories:
                self.categories.add(category)

    @factory.post_generation
    def technologies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tech in extracted:
                self.technologies.add(tech)
        else:
            # Create default technologies if none provided
            tech_skills = SkillFactory.create_batch(3)
            for skill in tech_skills:
                self.technologies.add(skill)


class ProjectImageFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProjectImage instances."""

    class Meta:
        model = ProjectImage

    project = factory.SubFactory(ProjectFactory)
    image = factory.django.FileField(filename="project_image.jpg")
    alt_text = factory.Faker("sentence", nb_words=5)
    order = factory.Sequence(lambda n: n)


class ExperienceFactory(factory.django.DjangoModelFactory):
    """Factory for creating Experience instances."""

    class Meta:
        model = Experience

    company_name = factory.Faker("company")
    position = factory.Faker("job")
    slug = factory.LazyAttribute(
        lambda obj: slugify(f"{obj.company_name}-{obj.position}")
    )
    description = factory.Faker("text", max_nb_chars=500)
    start_date = factory.Faker("date_between", start_date="-3y", end_date="today")
    end_date = factory.LazyAttribute(
        lambda obj: (
            fake.date_between(start_date=obj.start_date, end_date="today")
            if fake.boolean(chance_of_getting_true=50)
            else None
        )
    )
    location = factory.Faker("city")
    company_url = factory.Faker("url")
    is_current = factory.LazyAttribute(lambda obj: obj.end_date is None)
    order = factory.Sequence(lambda n: n)


class AchievementFactory(factory.django.DjangoModelFactory):
    """Factory for creating Achievement instances."""

    class Meta:
        model = Achievement

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=300)
    date_achieved = factory.Faker("date_between", start_date="-2y", end_date="today")
    certificate_image = factory.django.FileField(filename="certificate.jpg")
    certificate_url = factory.Faker("url")
    issuing_organization = factory.Faker("company")
    order = factory.Sequence(lambda n: n)


class ContactSubmissionFactory(factory.django.DjangoModelFactory):
    """Factory for creating ContactSubmission instances."""

    class Meta:
        model = ContactSubmission

    name = factory.Faker("name")
    email = factory.Faker("email")
    subject = factory.Faker("sentence", nb_words=5)
    message = factory.Faker("text", max_nb_chars=500)
    submitted_at = factory.Faker("date_time_this_year")
    is_read = factory.Faker("boolean", chance_of_getting_true=30)


class BlogFactory(factory.django.DjangoModelFactory):
    """Factory for creating Blog instances."""

    class Meta:
        model = Blog

    title = factory.Faker("sentence", nb_words=6)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    summary = factory.Faker("text", max_nb_chars=200)
    content = factory.Faker("text", max_nb_chars=1000)
    cover_image = factory.django.FileField(filename="blog_cover.jpg")
    created_date = factory.Faker("date_time_this_year")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            # Create default blog categories if none provided
            blog_categories = CategoryFactory.create_batch(
                2, category_type=Category.CategoryType.BLOG
            )
            for category in blog_categories:
                self.categories.add(category)


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for creating Comment instances."""

    class Meta:
        model = Comment

    blog = factory.SubFactory(BlogFactory)
    author_name = factory.Faker("name")
    author_email = factory.Faker("email")
    content = factory.Faker("text", max_nb_chars=300)
    created_at = factory.Faker("date_time_this_year")
    is_approved = factory.Faker("boolean", chance_of_getting_true=80)


class AboutMeConfigurationFactory(factory.django.DjangoModelFactory):
    """Factory for creating AboutMeConfiguration instances."""

    class Meta:
        model = AboutMeConfiguration
        django_get_or_create = ("intro_paragraph",)

    intro_paragraph = factory.Faker("text", max_nb_chars=300)
    years_of_experience = factory.Faker("random_int", min=1, max=15)
    projects_completed = factory.Faker("random_int", min=10, max=100)
    technologies_learned = factory.Faker("random_int", min=5, max=50)
    certifications_earned = factory.Faker("random_int", min=1, max=20)
    profile_image = factory.django.FileField(filename="profile.jpg")


class ResourceCategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating ResourceCategory instances."""

    class Meta:
        model = ResourceCategory

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("text", max_nb_chars=200)
    icon = factory.Faker("file_name", extension="svg")
    order = factory.Sequence(lambda n: n)


class ResourceFactory(factory.django.DjangoModelFactory):
    """Factory for creating Resource instances."""

    class Meta:
        model = Resource

    title = factory.Faker("sentence", nb_words=4)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker("text", max_nb_chars=300)
    category = factory.SubFactory(ResourceCategoryFactory)
    resource_type = factory.Iterator(
        Resource.ResourceType.choices, getter=lambda x: x[0]
    )
    file = factory.django.FileField(filename="resource.pdf")
    external_url = factory.Faker("url")
    is_featured = factory.Faker("boolean", chance_of_getting_true=30)
    is_public = True
    order = factory.Sequence(lambda n: n)
    created_at = factory.Faker("date_time_this_year")


# Convenience functions for creating complete test scenarios


def create_complete_portfolio():
    """Create a complete portfolio setup for testing."""
    # Site configuration
    site_config = SiteConfigurationFactory()

    # Categories
    project_categories = CategoryFactory.create_batch(
        3, category_type=Category.CategoryType.PROJECT
    )
    blog_categories = CategoryFactory.create_batch(
        2, category_type=Category.CategoryType.BLOG
    )

    # Skills
    skills = SkillFactory.create_batch(8)

    # Projects with images
    projects = []
    for i in range(5):
        project = ProjectFactory(
            categories=project_categories[:2], technologies=skills[:3]
        )
        # Add project images
        ProjectImageFactory.create_batch(3, project=project)
        projects.append(project)

    # Experience
    experiences = ExperienceFactory.create_batch(3)

    # Achievements
    achievements = AchievementFactory.create_batch(4)

    # Blog posts
    blogs = []
    for i in range(3):
        blog = BlogFactory(categories=blog_categories)
        # Add comments to each blog
        CommentFactory.create_batch(2, blog=blog)
        blogs.append(blog)

    # About me configuration
    about_me = AboutMeConfigurationFactory()

    # Resource categories and resources
    resource_categories = ResourceCategoryFactory.create_batch(2)
    resources = []
    for category in resource_categories:
        resources.extend(ResourceFactory.create_batch(3, category=category))

    # Contact submissions
    contacts = ContactSubmissionFactory.create_batch(5)

    return {
        "site_config": site_config,
        "categories": {
            "project": project_categories,
            "blog": blog_categories,
        },
        "skills": skills,
        "projects": projects,
        "experiences": experiences,
        "achievements": achievements,
        "blogs": blogs,
        "about_me": about_me,
        "resource_categories": resource_categories,
        "resources": resources,
        "contacts": contacts,
    }
