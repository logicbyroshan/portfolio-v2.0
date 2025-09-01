from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import datetime, timedelta
import os
from PIL import Image
import io

from portfolio.models import (
    SiteConfiguration, Technology, Category, Experience, 
    Project, Blog, Achievement, Skill, Resume, VideoResume,
    NewsletterSubscriber, ContactSubmission
)


class Command(BaseCommand):
    help = 'Populate the database with mock data for development'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database with mock data...')
        
        # Create Site Configuration
        self.create_site_config()
        
        # Create Technologies
        self.create_technologies()
        
        # Create Categories
        self.create_categories()
        
        # Create Skills
        self.create_skills()
        
        # Create Experiences
        self.create_experiences()
        
        # Create Projects
        self.create_projects()
        
        # Create Blogs
        self.create_blogs()
        
        # Create Achievements
        self.create_achievements()
        
        # Create Resume data
        self.create_resume()
        
        # Create Video Resume
        self.create_video_resume()
        
        # Create some newsletter subscribers
        self.create_newsletter_subscribers()
        
        # Create some contact submissions
        self.create_contact_submissions()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with mock data!')
        )

    def create_site_config(self):
        """Create or update site configuration"""
        config, created = SiteConfiguration.objects.get_or_create()
        
        # Update with comprehensive data
        config.hero_greeting = "HIII, IT'S ME"
        config.hero_name = "Roshan Damor"
        config.hero_tagline = "I am a AI Enthusiast"
        config.hero_bio = "GREETINGS, ALL DIGITAL EXPLORERS! I AM ROSHAN, A PASSIONATE AND INNOVATIVE DEVELOPER BUILDING AI-POWERED SOLUTIONS & SCALABLE WEB APPS — SDE & AI ENGINEER"
        
        # Hero stats
        config.hero_projects_stat = "25+"
        config.hero_internships_stat = "3+"
        config.hero_articles_stat = "15+"
        
        # Section titles
        config.about_title = "About Me"
        config.about_description = "A passionate developer dedicated to building beautiful, functional, and user-centric digital experiences."
        
        config.skills_title = "My Tech Stack"
        config.skills_description = "Technologies and tools I work with to build amazing projects."
        
        config.experience_title = "Where I've Worked"
        config.experience_description = "A glimpse into my professional journey, contributing to impactful projects."
        
        # Social media links
        config.twitter_url = "https://x.com/logicbyroshan"
        config.github_url = "https://github.com/logicbyroshan"
        config.linkedin_url = "https://www.linkedin.com/in/logicbyroshan"
        config.youtube_url = "https://www.youtube.com/channel/logicbyroshan"
        
        # Contact info
        config.email = "contact@roshanproject.site"
        config.phone = "+91 12345 67890"
        config.location = "Mumbai, India"
        
        config.save()
        
        action = "Created" if created else "Updated"
        self.stdout.write(f'{action} Site Configuration')

    def create_technologies(self):
        """Create technology entries"""
        technologies = [
            'Python', 'Django', 'JavaScript', 'React', 'Node.js',
            'PostgreSQL', 'MongoDB', 'Docker', 'AWS', 'Git',
            'TensorFlow', 'PyTorch', 'OpenCV', 'Pandas', 'NumPy',
            'FastAPI', 'Redis', 'Nginx', 'Linux', 'VS Code'
        ]
        
        created_count = 0
        for tech_name in technologies:
            tech, created = Technology.objects.get_or_create(name=tech_name)
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new technologies')

    def create_categories(self):
        """Create categories for different content types"""
        categories_data = [
            # Project categories
            ('Web Development', 'PRO'),
            ('AI/ML', 'PRO'),
            ('Mobile App', 'PRO'),
            ('API Development', 'PRO'),
            ('DevOps', 'PRO'),
            
            # Blog categories
            ('Technology', 'BLG'),
            ('AI & Machine Learning', 'BLG'),
            ('Web Development', 'BLG'),
            ('Career Tips', 'BLG'),
            ('Tutorials', 'BLG'),
            
            # Experience categories
            ('Full-time', 'EXP'),
            ('Internship', 'EXP'),
            ('Freelance', 'EXP'),
        ]
        
        created_count = 0
        for name, cat_type in categories_data:
            category, created = Category.objects.get_or_create(
                name=name, 
                category_type=cat_type
            )
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new categories')

    def create_skills(self):
        """Create skill entries"""
        skills_data = [
            {
                'name': 'Python Development',
                'category': 'Programming',
                'proficiency_level': 90,
                'description': 'Expert in Python programming with Django, FastAPI, and data science libraries.',
                'is_featured': True
            },
            {
                'name': 'Machine Learning',
                'category': 'AI/ML',
                'proficiency_level': 85,
                'description': 'Experienced in building ML models with TensorFlow, PyTorch, and scikit-learn.',
                'is_featured': True
            },
            {
                'name': 'Web Development',
                'category': 'Frontend',
                'proficiency_level': 80,
                'description': 'Full-stack web development with React, Django, and modern web technologies.',
                'is_featured': True
            },
            {
                'name': 'Database Design',
                'category': 'Backend',
                'proficiency_level': 75,
                'description': 'Proficient in SQL and NoSQL databases including PostgreSQL and MongoDB.',
                'is_featured': False
            },
            {
                'name': 'Cloud Computing',
                'category': 'DevOps',
                'proficiency_level': 70,
                'description': 'Experience with AWS, Docker, and cloud deployment strategies.',
                'is_featured': False
            }
        ]
        
        # Get technologies for skills
        python = Technology.objects.filter(name='Python').first()
        django = Technology.objects.filter(name='Django').first()
        react = Technology.objects.filter(name='React').first()
        
        created_count = 0
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            
            if created:
                # Add some technologies to skills
                if 'Python' in skill_data['name'] and python:
                    skill.technologies.add(python)
                if 'Web' in skill_data['name']:
                    if django:
                        skill.technologies.add(django)
                    if react:
                        skill.technologies.add(react)
                
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new skills')

    def create_experiences(self):
        """Create experience entries"""
        experiences_data = [
            {
                'role': 'Senior AI Engineer',
                'company_name': 'TechCorp Solutions',
                'location': 'Mumbai, India',
                'start_date': datetime(2023, 6, 1).date(),
                'end_date': None,  # Current job
                'summary': 'Leading AI initiatives and developing machine learning solutions for enterprise clients. Built scalable ML pipelines and deployed models in production.',
                'achievements': [
                    'Improved model accuracy by 25%',
                    'Led a team of 5 developers',
                    'Deployed 10+ ML models to production'
                ],
                'is_featured': True
            },
            {
                'role': 'Full Stack Developer',
                'company_name': 'StartupXYZ',
                'location': 'Remote',
                'start_date': datetime(2022, 3, 1).date(),
                'end_date': datetime(2023, 5, 31).date(),
                'summary': 'Developed full-stack web applications using Django and React. Collaborated with cross-functional teams to deliver high-quality products.',
                'achievements': [
                    'Built 5 major web applications',
                    'Reduced page load time by 40%',
                    'Implemented CI/CD pipelines'
                ],
                'is_featured': True
            },
            {
                'role': 'Software Development Intern',
                'company_name': 'BigTech Company',
                'location': 'Bangalore, India',
                'start_date': datetime(2021, 6, 1).date(),
                'end_date': datetime(2021, 8, 31).date(),
                'summary': 'Internship focused on backend development and API design. Gained experience with large-scale systems and best practices.',
                'achievements': [
                    'Designed RESTful APIs',
                    'Optimized database queries',
                    'Contributed to open source projects'
                ],
                'is_featured': False
            }
        ]
        
        # Get categories and technologies
        fulltime_cat = Category.objects.filter(name='Full-time', category_type='EXP').first()
        internship_cat = Category.objects.filter(name='Internship', category_type='EXP').first()
        python = Technology.objects.filter(name='Python').first()
        django = Technology.objects.filter(name='Django').first()
        
        created_count = 0
        for i, exp_data in enumerate(experiences_data):
            # Convert achievements list to string
            exp_data['achievements'] = '\\n'.join([f"• {achievement}" for achievement in exp_data['achievements']])
            
            experience, created = Experience.objects.get_or_create(
                role=exp_data['role'],
                company_name=exp_data['company_name'],
                defaults=exp_data
            )
            
            if created:
                # Add category
                if i == 2:  # Internship
                    if internship_cat:
                        experience.categories.add(internship_cat)
                else:  # Full-time
                    if fulltime_cat:
                        experience.categories.add(fulltime_cat)
                
                # Add technologies
                if python:
                    experience.technologies.add(python)
                if django and 'Full Stack' in exp_data['role']:
                    experience.technologies.add(django)
                
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new experiences')

    def create_projects(self):
        """Create project entries"""
        projects_data = [
            {
                'title': 'AI-Powered Portfolio Website',
                'description': 'A dynamic portfolio website with AI query capabilities, built using Django and modern web technologies.',
                'detailed_description': 'This project showcases a comprehensive portfolio website with integrated AI capabilities for answering visitor queries about my background and experience.',
                'github_url': 'https://github.com/logicbyroshan/portfolio-v2.0',
                'live_url': 'https://roshanproject.site',
                'is_featured': True,
                'status': 'COM'
            },
            {
                'title': 'Machine Learning Pipeline',
                'description': 'End-to-end ML pipeline for automated data processing and model deployment.',
                'detailed_description': 'Built a scalable machine learning pipeline that automates data ingestion, preprocessing, model training, and deployment using MLOps best practices.',
                'github_url': 'https://github.com/logicbyroshan/ml-pipeline',
                'live_url': '',
                'is_featured': True,
                'status': 'COM'
            },
            {
                'title': 'E-commerce API',
                'description': 'RESTful API for e-commerce platform with advanced features.',
                'detailed_description': 'Developed a comprehensive e-commerce API with features like user authentication, product management, order processing, and payment integration.',
                'github_url': 'https://github.com/logicbyroshan/ecommerce-api',
                'live_url': '',
                'is_featured': False,
                'status': 'IP'
            }
        ]
        
        # Get categories and technologies
        web_cat = Category.objects.filter(name='Web Development', category_type='PRO').first()
        ai_cat = Category.objects.filter(name='AI/ML', category_type='PRO').first()
        api_cat = Category.objects.filter(name='API Development', category_type='PRO').first()
        
        python = Technology.objects.filter(name='Python').first()
        django = Technology.objects.filter(name='Django').first()
        
        created_count = 0
        for i, proj_data in enumerate(projects_data):
            project, created = Project.objects.get_or_create(
                title=proj_data['title'],
                defaults=proj_data
            )
            
            if created:
                # Add categories
                if i == 0:  # Portfolio website
                    if web_cat:
                        project.categories.add(web_cat)
                elif i == 1:  # ML Pipeline
                    if ai_cat:
                        project.categories.add(ai_cat)
                elif i == 2:  # E-commerce API
                    if api_cat:
                        project.categories.add(api_cat)
                
                # Add technologies
                if python:
                    project.technologies.add(python)
                if django and i != 1:  # All except ML pipeline
                    project.technologies.add(django)
                
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new projects')

    def create_blogs(self):
        """Create blog entries"""
        blogs_data = [
            {
                'title': 'Getting Started with Django and AI Integration',
                'meta_description': 'Learn how to integrate AI capabilities into your Django applications.',
                'content': 'In this comprehensive guide, we explore how to integrate AI and machine learning capabilities into Django applications...',
                'excerpt': 'A comprehensive guide on integrating AI capabilities into Django applications.',
                'read_time': 8,
                'is_featured': True,
                'status': 'PUB'
            },
            {
                'title': 'Building Scalable APIs with FastAPI',
                'meta_description': 'Best practices for building high-performance APIs using FastAPI.',
                'content': 'FastAPI has become one of the most popular choices for building modern APIs. In this article, we discuss best practices...',
                'excerpt': 'Learn best practices for building high-performance APIs with FastAPI.',
                'read_time': 6,
                'is_featured': True,
                'status': 'PUB'
            },
            {
                'title': 'Machine Learning Model Deployment Strategies',
                'meta_description': 'Different approaches to deploying ML models in production.',
                'content': 'Deploying machine learning models to production requires careful consideration of various factors...',
                'excerpt': 'Explore different strategies for deploying ML models in production environments.',
                'read_time': 10,
                'is_featured': False,
                'status': 'DRF'
            }
        ]
        
        # Get categories
        tech_cat = Category.objects.filter(name='Technology', category_type='BLG').first()
        ai_cat = Category.objects.filter(name='AI & Machine Learning', category_type='BLG').first()
        web_cat = Category.objects.filter(name='Web Development', category_type='BLG').first()
        
        created_count = 0
        for i, blog_data in enumerate(blogs_data):
            blog, created = Blog.objects.get_or_create(
                title=blog_data['title'],
                defaults=blog_data
            )
            
            if created:
                # Add categories
                if i == 0:  # Django AI
                    if web_cat:
                        blog.categories.add(web_cat)
                    if ai_cat:
                        blog.categories.add(ai_cat)
                elif i == 1:  # FastAPI
                    if tech_cat:
                        blog.categories.add(tech_cat)
                elif i == 2:  # ML Deployment
                    if ai_cat:
                        blog.categories.add(ai_cat)
                
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new blogs')

    def create_achievements(self):
        """Create achievement entries"""
        achievements_data = [
            {
                'title': 'Best AI Project Award',
                'organization': 'TechFest 2023',
                'description': 'Won first place for developing an innovative AI-powered solution for predictive analytics.',
                'achievement_date': datetime(2023, 11, 15).date(),
                'is_featured': True
            },
            {
                'title': 'Open Source Contributor',
                'organization': 'GitHub',
                'description': 'Active contributor to multiple open source projects with over 100 contributions.',
                'achievement_date': datetime(2023, 8, 1).date(),
                'is_featured': True
            },
            {
                'title': 'Certified AWS Solutions Architect',
                'organization': 'Amazon Web Services',
                'description': 'Successfully completed AWS Solutions Architect certification demonstrating cloud expertise.',
                'achievement_date': datetime(2023, 5, 20).date(),
                'is_featured': False
            }
        ]
        
        created_count = 0
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                title=achievement_data['title'],
                defaults=achievement_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new achievements')

    def create_resume(self):
        """Create resume data"""
        resume, created = Resume.objects.get_or_create()
        
        if created or not resume.title:
            resume.title = "Roshan Damor - AI Engineer & Full Stack Developer"
            resume.description = "Download my latest resume to learn more about my experience in AI, machine learning, and full-stack development."
            resume.years_experience = "3+"
            resume.total_projects = "25+"
            resume.technologies_used = "15+"
            resume.save()
        
        action = "Created" if created else "Updated"
        self.stdout.write(f'{action} Resume data')

    def create_video_resume(self):
        """Create video resume data"""
        video_resume, created = VideoResume.objects.get_or_create()
        
        if created or not video_resume.youtube_embed_url:
            video_resume.youtube_embed_url = "https://www.youtube.com/embed/dQw4w9WgXcQ"  # Placeholder
            video_resume.save()
        
        action = "Created" if created else "Updated"
        self.stdout.write(f'{action} Video Resume data')

    def create_newsletter_subscribers(self):
        """Create sample newsletter subscribers"""
        subscribers_data = [
            'john.doe@example.com',
            'jane.smith@example.com',
            'developer@techcorp.com',
            'student@university.edu',
            'entrepreneur@startup.io'
        ]
        
        created_count = 0
        for email in subscribers_data:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new newsletter subscribers')

    def create_contact_submissions(self):
        """Create sample contact submissions"""
        submissions_data = [
            {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'subject': 'Project Collaboration',
                'message': 'Hi Roshan, I would like to discuss a potential collaboration on an AI project.'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'subject': 'Freelance Opportunity',
                'message': 'We have a freelance opportunity that matches your skills. Are you available?'
            },
            {
                'name': 'Tech Startup',
                'email': 'contact@techstartup.com',
                'subject': 'Job Opportunity',
                'message': 'We are looking for a senior developer to join our team. Would you be interested?'
            }
        ]
        
        created_count = 0
        for submission_data in submissions_data:
            submission, created = ContactSubmission.objects.get_or_create(
                email=submission_data['email'],
                defaults=submission_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} new contact submissions')
