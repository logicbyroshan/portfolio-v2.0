# ai/utils.py
from portfolio.models import (
    Project, Blog, Experience, Skill, Service, Achievement,
    SiteConfiguration
)

def get_portfolio_context():
    """
    Gathers portfolio data to provide context for AI responses.
    """
    try:
        # Get site configuration
        config = SiteConfiguration.objects.first()
        
        # Get recent projects
        projects = Project.objects.filter(is_featured=True)[:5]
        
        # Get recent blogs
        blogs = Blog.objects.filter(is_published=True)[:3]
        
        # Get experiences
        experiences = Experience.objects.all()[:3]
        
        # Get skills
        skills = Skill.objects.all()[:10]
        
        # Get services
        services = Service.objects.all()[:5]
        
        # Get achievements
        achievements = Achievement.objects.all()[:5]
        
        # Build context string
        context = f"""
        ABOUT ROSHAN:
        Name: Roshan Damor
        """
        
        if config:
            context += f"""
        Bio: {config.about_me or 'Full-Stack Developer and AI Enthusiast'}
        Email: {config.email or 'roshan@example.com'}
        Location: {config.location or 'India'}
        """
        
        # Add projects
        if projects.exists():
            context += "\n\nFEATURED PROJECTS:\n"
            for project in projects:
                context += f"- {project.title}: {project.description[:100]}...\n"
                if project.technologies.exists():
                    techs = ", ".join([tech.name for tech in project.technologies.all()[:5]])
                    context += f"  Technologies: {techs}\n"
        
        # Add blog posts
        if blogs.exists():
            context += "\n\nRECENT BLOG POSTS:\n"
            for blog in blogs:
                context += f"- {blog.title}: {blog.content[:100]}...\n"
        
        # Add experiences
        if experiences.exists():
            context += "\n\nWORK EXPERIENCE:\n"
            for exp in experiences:
                context += f"- {exp.title} at {exp.company} ({exp.start_date} - {exp.end_date or 'Present'})\n"
                context += f"  {exp.description[:100]}...\n"
        
        # Add skills
        if skills.exists():
            context += "\n\nSKILLS:\n"
            skill_names = [skill.name for skill in skills]
            context += f"- {', '.join(skill_names)}\n"
        
        # Add services
        if services.exists():
            context += "\n\nSERVICES OFFERED:\n"
            for service in services:
                context += f"- {service.title}: {service.description[:100]}...\n"
        
        # Add achievements
        if achievements.exists():
            context += "\n\nACHIEVEMENTS:\n"
            for achievement in achievements:
                context += f"- {achievement.title}: {achievement.description[:100]}...\n"
        
        return context
        
    except Exception as e:
        return """
        ABOUT ROSHAN:
        Name: Roshan Damor
        Bio: Full-Stack Developer and AI Enthusiast
        Skills: Python, Django, JavaScript, React, Machine Learning
        """
