import os
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
import io
from portfolio.models import (
    Technology, Category, Project, ProjectImage, Blog, Comment,
    ProjectComment, Experience, Service
)

class Command(BaseCommand):
    help = 'Create comprehensive test data for the portfolio website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new test data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS('Creating test data...'))
        
        # Create data in order of dependencies
        self.create_technologies()
        self.create_categories()
        self.create_projects()
        self.create_blogs()
        self.create_experiences()
        self.create_services()
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))

    def clear_data(self):
        """Clear existing test data"""
        models_to_clear = [
            ProjectComment, Comment, ProjectImage, Project, Blog, 
            Experience, Service, Technology, Category
        ]
        
        for model in models_to_clear:
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(f'Cleared {count} {model.__name__} records')

    def create_placeholder_image(self, width=800, height=600, color=(100, 150, 200)):
        """Create a placeholder image"""
        img = Image.new('RGB', (width, height), color=color)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return ContentFile(buffer.read())

    def create_technologies(self):
        """Create technology entries"""
        technologies = [
            'Python', 'Django', 'JavaScript', 'React', 'Vue.js', 'Node.js',
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Docker', 'AWS',
            'HTML5', 'CSS3', 'Bootstrap', 'Tailwind CSS', 'Sass', 'TypeScript',
            'Git', 'GitHub', 'GitLab', 'Jenkins', 'Linux', 'Nginx',
            'TensorFlow', 'PyTorch', 'OpenAI', 'REST API', 'GraphQL', 'FastAPI',
            'React Native', 'WebSocket', 'Celery', 'Django Channels'
        ]
        
        for tech_name in technologies:
            tech, created = Technology.objects.get_or_create(name=tech_name)
            if created:
                self.stdout.write(f'Created technology: {tech_name}')

    def create_categories(self):
        """Create categories for projects and blogs"""
        project_categories = [
            'Web Development', 'Mobile App', 'AI/ML', 'E-commerce', 
            'API Development', 'DevOps', 'Open Source'
        ]
        
        blog_categories = [
            'Programming', 'Technology', 'AI & Machine Learning', 
            'Web Development', 'Career Tips', 'Project Updates'
        ]
        
        for cat_name in project_categories:
            cat, created = Category.objects.get_or_create(
                name=cat_name, 
                category_type=Category.CategoryType.PROJECT
            )
            if created:
                self.stdout.write(f'Created project category: {cat_name}')
        
        for cat_name in blog_categories:
            cat, created = Category.objects.get_or_create(
                name=cat_name, 
                category_type=Category.CategoryType.BLOG
            )
            if created:
                self.stdout.write(f'Created blog category: {cat_name}')

    def create_projects(self):
        """Create detailed project entries"""
        projects_data = [
            {
                'title': 'AI-Powered E-commerce Platform',
                'summary': 'A modern e-commerce platform with AI-driven product recommendations and intelligent search capabilities.',
                'content': '''
                <h3>Project Overview</h3>
                <p>This comprehensive e-commerce platform leverages artificial intelligence to provide personalized shopping experiences. Built with Django and React, it features advanced product recommendation algorithms and natural language search.</p>
                
                <h3>Key Features</h3>
                <ul>
                    <li>AI-powered product recommendations using collaborative filtering</li>
                    <li>Intelligent search with natural language processing</li>
                    <li>Real-time inventory management</li>
                    <li>Secure payment gateway integration</li>
                    <li>Responsive design for all devices</li>
                    <li>Admin dashboard with analytics</li>
                </ul>
                
                <h3>Technical Challenges</h3>
                <p>The main challenge was implementing real-time recommendation updates while maintaining optimal performance. We solved this using Redis caching and background task processing with Celery.</p>
                
                <h3>Results</h3>
                <p>The platform achieved a 40% increase in user engagement and 25% boost in conversion rates compared to traditional e-commerce solutions.</p>
                ''',
                'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Redis', 'TensorFlow'],
                'categories': ['Web Development', 'AI/ML', 'E-commerce'],
                'github_url': 'https://github.com/logicbyroshan/ai-ecommerce',
                'live_url': 'https://ai-shop-demo.vercel.app'
            },
            {
                'title': 'Real-time Chat Application',
                'summary': 'A scalable real-time messaging platform with WebSocket support, file sharing, and group chat functionality.',
                'content': '''
                <h3>Project Description</h3>
                <p>A full-featured chat application built with modern web technologies, supporting real-time messaging, file uploads, and group conversations.</p>
                
                <h3>Features Implemented</h3>
                <ul>
                    <li>Real-time messaging with WebSocket technology</li>
                    <li>Group chat creation and management</li>
                    <li>File and image sharing capabilities</li>
                    <li>Message search and history</li>
                    <li>User authentication and profiles</li>
                    <li>Mobile-responsive design</li>
                </ul>
                
                <h3>Architecture</h3>
                <p>The application uses Django Channels for WebSocket handling, Redis for message queuing, and PostgreSQL for data persistence. The frontend is built with Vue.js for reactive user interfaces.</p>
                
                <h3>Performance Optimizations</h3>
                <p>Implemented message pagination, image compression, and efficient database queries to ensure smooth performance even with thousands of concurrent users.</p>
                ''',
                'technologies': ['Python', 'Django', 'Vue.js', 'PostgreSQL', 'Redis', 'Django Channels'],
                'categories': ['Web Development', 'API Development'],
                'github_url': 'https://github.com/logicbyroshan/realtime-chat',
                'live_url': 'https://chat-app-demo.herokuapp.com'
            },
            {
                'title': 'Portfolio Website with CMS',
                'summary': 'A dynamic portfolio website with custom content management system, blog functionality, and project showcase.',
                'content': '''
                <h3>About This Project</h3>
                <p>A fully customizable portfolio website with an integrated content management system, allowing for easy updates of projects, blog posts, and personal information.</p>
                
                <h3>Key Components</h3>
                <ul>
                    <li>Dynamic project and blog management</li>
                    <li>Responsive design with modern UI/UX</li>
                    <li>SEO optimization and performance tuning</li>
                    <li>Contact form with email notifications</li>
                    <li>Admin panel for content management</li>
                    <li>Social media integration</li>
                </ul>
                
                <h3>Design Philosophy</h3>
                <p>The design focuses on clean aesthetics and user experience, with careful attention to typography, color schemes, and navigation flow.</p>
                
                <h3>Technical Implementation</h3>
                <p>Built with Django for robust backend functionality and vanilla JavaScript for frontend interactions, ensuring fast loading times and excellent SEO performance.</p>
                ''',
                'technologies': ['Python', 'Django', 'JavaScript', 'HTML5', 'CSS3', 'Bootstrap'],
                'categories': ['Web Development'],
                'github_url': 'https://github.com/logicbyroshan/portfolio-v2',
                'live_url': 'https://roshanprojects.site'
            },
            {
                'title': 'Machine Learning Model Deployment Platform',
                'summary': 'A cloud-based platform for deploying and managing machine learning models with API endpoints and monitoring.',
                'content': '''
                <h3>Project Vision</h3>
                <p>This platform simplifies the deployment of machine learning models by providing a user-friendly interface for model management, API generation, and performance monitoring.</p>
                
                <h3>Core Features</h3>
                <ul>
                    <li>Automated model deployment with Docker containers</li>
                    <li>RESTful API generation for deployed models</li>
                    <li>Real-time performance monitoring and logging</li>
                    <li>Model versioning and rollback capabilities</li>
                    <li>Load balancing for high-traffic scenarios</li>
                    <li>Security features with API key management</li>
                </ul>
                
                <h3>Technology Stack</h3>
                <p>The platform leverages FastAPI for high-performance APIs, Docker for containerization, and AWS for scalable cloud deployment.</p>
                
                <h3>Impact</h3>
                <p>Reduced model deployment time from days to minutes, enabling data science teams to iterate faster and deliver value more efficiently.</p>
                ''',
                'technologies': ['Python', 'FastAPI', 'Docker', 'AWS', 'TensorFlow', 'MongoDB'],
                'categories': ['AI/ML', 'API Development', 'DevOps'],
                'github_url': 'https://github.com/logicbyroshan/ml-deploy-platform',
                'live_url': 'https://ml-deploy.example.com'
            },
            {
                'title': 'Task Management Mobile App',
                'summary': 'A cross-platform mobile application for task management with team collaboration features and offline support.',
                'content': '''
                <h3>Application Overview</h3>
                <p>A comprehensive task management solution designed for teams and individuals, featuring intuitive interfaces and powerful collaboration tools.</p>
                
                <h3>Feature Highlights</h3>
                <ul>
                    <li>Cross-platform compatibility (iOS and Android)</li>
                    <li>Offline task creation and synchronization</li>
                    <li>Team collaboration with real-time updates</li>
                    <li>Project organization with custom categories</li>
                    <li>Push notifications for important deadlines</li>
                    <li>Time tracking and productivity analytics</li>
                </ul>
                
                <h3>Development Approach</h3>
                <p>Built using React Native for cross-platform development, with a Django REST API backend for data management and user authentication.</p>
                
                <h3>User Experience Focus</h3>
                <p>Extensive user testing was conducted to ensure intuitive navigation and efficient task management workflows, resulting in a 95% user satisfaction rate.</p>
                ''',
                'technologies': ['React', 'React Native', 'Django', 'REST API', 'PostgreSQL'],
                'categories': ['Mobile App', 'API Development'],
                'github_url': 'https://github.com/logicbyroshan/task-mobile-app',
                'live_url': 'https://play.google.com/store/apps/details?id=com.taskapp'
            },
            {
                'title': 'Open Source CSS Framework',
                'summary': 'A lightweight, utility-first CSS framework designed for rapid UI development with modern design principles.',
                'content': '''
                <h3>Framework Philosophy</h3>
                <p>This CSS framework was created to address the need for a lightweight yet powerful styling solution that promotes rapid development without sacrificing design quality.</p>
                
                <h3>Key Features</h3>
                <ul>
                    <li>Utility-first approach for maximum flexibility</li>
                    <li>Responsive design system with breakpoint utilities</li>
                    <li>Modern color palette and typography scale</li>
                    <li>Component library with common UI patterns</li>
                    <li>Dark mode support built-in</li>
                    <li>Minimal footprint (under 20KB gzipped)</li>
                </ul>
                
                <h3>Community Impact</h3>
                <p>The framework has been adopted by over 500 developers worldwide, with active contributions from the open-source community.</p>
                
                <h3>Documentation & Support</h3>
                <p>Comprehensive documentation with interactive examples and a supportive community forum for developers of all skill levels.</p>
                ''',
                'technologies': ['CSS3', 'Sass', 'JavaScript', 'Node.js', 'Git'],
                'categories': ['Open Source', 'Web Development'],
                'github_url': 'https://github.com/logicbyroshan/utility-css-framework',
                'live_url': 'https://css-framework-docs.netlify.app'
            }
        ]

        for project_data in projects_data:
            # Create project
            project = Project.objects.create(
                title=project_data['title'],
                summary=project_data['summary'],
                content=project_data['content'],
                github_url=project_data['github_url'],
                live_url=project_data['live_url'],
                created_date=timezone.now() - timedelta(days=random.randint(30, 365))
            )
            
            # Create and assign cover image
            cover_image = self.create_placeholder_image(
                800, 600, (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            )
            project.cover_image.save(f'{project.slug}_cover.jpg', cover_image, save=True)
            
            # Add technologies
            for tech_name in project_data['technologies']:
                try:
                    tech = Technology.objects.get(name=tech_name)
                    project.technologies.add(tech)
                except Technology.DoesNotExist:
                    self.stdout.write(f'Warning: Technology "{tech_name}" not found, skipping...')
            
            # Add categories
            for cat_name in project_data['categories']:
                cat = Category.objects.get(name=cat_name, category_type=Category.CategoryType.PROJECT)
                project.categories.add(cat)
            
            # Create additional project images
            for i in range(random.randint(2, 4)):
                img = self.create_placeholder_image(
                    800, 600, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                )
                project_image = ProjectImage.objects.create(
                    project=project,
                    caption=f"Screenshot {i+1} of {project.title}"
                )
                project_image.image.save(f'{project.slug}_image_{i+1}.jpg', img, save=True)
            
            # Add some comments
            for i in range(random.randint(1, 3)):
                ProjectComment.objects.create(
                    project=project,
                    author_name=random.choice(['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson']),
                    body=random.choice([
                        'Great project! The implementation is really clean and well-documented.',
                        'Love the user interface design. Very intuitive and modern.',
                        'Impressive technical implementation. Would love to contribute!',
                        'This project solved exactly what I was looking for. Thank you!'
                    ]),
                    likes=random.randint(0, 25),
                    created_date=timezone.now() - timedelta(days=random.randint(1, 90))
                )
            
            self.stdout.write(f'Created project: {project.title}')

    def create_blogs(self):
        """Create engaging blog posts"""
        blogs_data = [
            {
                'title': 'Building Scalable Web Applications with Django',
                'summary': 'A comprehensive guide to creating robust, scalable web applications using Django framework, covering best practices and optimization techniques.',
                'content': '''
                <p>Django has been my framework of choice for building web applications for several years now. In this article, I'll share the lessons I've learned about creating scalable, maintainable Django applications.</p>
                
                <h3>Setting Up for Scale</h3>
                <p>When starting a new Django project, it's crucial to think about scalability from day one. This doesn't mean over-engineering, but rather making thoughtful architectural decisions that will serve you well as your application grows.</p>
                
                <h4>Database Design</h4>
                <p>One of the most important aspects of a scalable Django application is proper database design. Here are some key principles I follow:</p>
                <ul>
                    <li>Use appropriate field types and constraints</li>
                    <li>Add database indexes for frequently queried fields</li>
                    <li>Consider database normalization vs. denormalization trade-offs</li>
                    <li>Plan for data archiving and cleanup strategies</li>
                </ul>
                
                <h4>Caching Strategies</h4>
                <p>Caching is essential for performance at scale. Django provides several caching options:</p>
                <ul>
                    <li>Per-page caching for static content</li>
                    <li>Template fragment caching for dynamic pages</li>
                    <li>Low-level cache API for custom caching logic</li>
                    <li>Database query caching with tools like Redis</li>
                </ul>
                
                <h3>Code Organization</h3>
                <p>As your Django project grows, maintaining clean, organized code becomes increasingly important. I recommend using a modular app structure and following Django's "fat models, thin views" principle.</p>
                
                <h3>Testing and Deployment</h3>
                <p>A comprehensive testing strategy is essential for maintaining quality at scale. This includes unit tests, integration tests, and end-to-end testing. For deployment, I prefer using Docker containers with orchestration tools like Kubernetes for production environments.</p>
                
                <p>Building scalable web applications is both an art and a science. By following these principles and continuously monitoring and optimizing your application, you can create Django applications that serve millions of users reliably.</p>
                ''',
                'categories': ['Web Development', 'Programming'],
                'author_name': 'Roshan Damor'
            },
            {
                'title': 'The Future of AI in Web Development',
                'summary': 'Exploring how artificial intelligence is transforming web development, from automated code generation to intelligent user experiences.',
                'content': '''
                <p>Artificial Intelligence is revolutionizing every industry, and web development is no exception. As someone who works at the intersection of AI and web technologies, I'm excited to share insights about where this field is heading.</p>
                
                <h3>AI-Powered Development Tools</h3>
                <p>The development process itself is being transformed by AI. We're seeing remarkable progress in several areas:</p>
                
                <h4>Code Generation and Completion</h4>
                <p>Tools like GitHub Copilot and ChatGPT are changing how we write code. These AI assistants can generate entire functions, suggest optimizations, and even help debug complex issues. While they're not perfect, they're incredibly useful for boosting productivity.</p>
                
                <h4>Automated Testing</h4>
                <p>AI is making automated testing more intelligent. Instead of just running predefined test cases, AI-powered testing tools can generate test scenarios based on user behavior patterns and identify potential edge cases that human testers might miss.</p>
                
                <h3>Intelligent User Experiences</h3>
                <p>On the user-facing side, AI is enabling more personalized and intuitive web experiences:</p>
                
                <ul>
                    <li><strong>Personalization Engines:</strong> AI algorithms analyze user behavior to deliver personalized content and recommendations</li>
                    <li><strong>Chatbots and Virtual Assistants:</strong> Natural language processing enables more sophisticated customer support</li>
                    <li><strong>Accessibility Improvements:</strong> AI helps make websites more accessible through automatic alt text generation and voice navigation</li>
                </ul>
                
                <h3>Challenges and Considerations</h3>
                <p>While AI brings exciting opportunities, it also presents challenges:</p>
                
                <ul>
                    <li>Ensuring AI-generated code is secure and maintainable</li>
                    <li>Balancing automation with human creativity and oversight</li>
                    <li>Addressing bias in AI algorithms</li>
                    <li>Managing the computational costs of AI-powered features</li>
                </ul>
                
                <h3>Looking Ahead</h3>
                <p>The future of AI in web development is bright. We can expect to see more sophisticated AI tools that understand context better, generate higher-quality code, and create more intuitive user experiences. However, the human element will remain crucial for creative problem-solving and strategic thinking.</p>
                
                <p>As developers, our role is evolving from writing every line of code to becoming AI-assisted problem solvers and experience designers. It's an exciting time to be in this field!</p>
                ''',
                'categories': ['AI & Machine Learning', 'Technology'],
                'author_name': 'Roshan Damor'
            },
            {
                'title': 'Career Tips for Junior Developers',
                'summary': 'Essential advice for new developers starting their career journey, including learning strategies, networking tips, and common pitfalls to avoid.',
                'content': '''
                <p>Starting a career in software development can be both exciting and overwhelming. Having mentored many junior developers over the years, I've compiled some essential tips that can help accelerate your growth and avoid common pitfalls.</p>
                
                <h3>Focus on Fundamentals</h3>
                <p>While it's tempting to jump into the latest frameworks and technologies, building a strong foundation is crucial for long-term success.</p>
                
                <h4>Core Programming Concepts</h4>
                <ul>
                    <li>Data structures and algorithms</li>
                    <li>Object-oriented programming principles</li>
                    <li>Database design and querying</li>
                    <li>Version control (Git)</li>
                    <li>Testing methodologies</li>
                </ul>
                
                <h4>Problem-Solving Skills</h4>
                <p>The ability to break down complex problems into smaller, manageable pieces is more valuable than knowing every framework. Practice on platforms like LeetCode, HackerRank, or by building personal projects.</p>
                
                <h3>Build a Portfolio</h3>
                <p>Your portfolio is often the first thing potential employers will see. Make sure it showcases:</p>
                
                <ul>
                    <li>Diverse projects demonstrating different skills</li>
                    <li>Clean, well-documented code</li>
                    <li>Live demos when possible</li>
                    <li>Your problem-solving process and learnings</li>
                </ul>
                
                <h3>Networking and Community</h3>
                <p>The developer community is incredibly supportive. Here's how to get involved:</p>
                
                <ul>
                    <li>Attend local meetups and conferences</li>
                    <li>Contribute to open-source projects</li>
                    <li>Share your learning journey on social media</li>
                    <li>Find mentors and peers for mutual support</li>
                </ul>
                
                <h3>Continuous Learning</h3>
                <p>Technology evolves rapidly, so developing a learning mindset is essential:</p>
                
                <ul>
                    <li>Follow industry blogs and newsletters</li>
                    <li>Take online courses and tutorials</li>
                    <li>Experiment with new technologies in side projects</li>
                    <li>Learn from code reviews and feedback</li>
                </ul>
                
                <h3>Common Mistakes to Avoid</h3>
                <p>Based on my experience, here are some pitfalls to watch out for:</p>
                
                <ul>
                    <li><strong>Tutorial Hell:</strong> Don't just follow tutorials endlessly; build original projects</li>
                    <li><strong>Perfectionism:</strong> Ship working software rather than perfect code</li>
                    <li><strong>Isolation:</strong> Don't try to learn everything alone; engage with the community</li>
                    <li><strong>Imposter Syndrome:</strong> Remember that everyone was a beginner once</li>
                </ul>
                
                <h3>Final Thoughts</h3>
                <p>Remember that becoming a skilled developer is a journey, not a destination. Be patient with yourself, celebrate small wins, and keep building. The software development field offers incredible opportunities for those who are passionate and persistent.</p>
                
                <p>If you're just starting out, feel free to reach out with questions. The developer community is here to support you!</p>
                ''',
                'categories': ['Career Tips', 'Programming'],
                'author_name': 'Roshan Damor'
            },
            {
                'title': 'Optimizing Frontend Performance: A Complete Guide',
                'summary': 'Learn how to make your web applications lightning fast with proven performance optimization techniques and modern best practices.',
                'content': '''
                <p>Website performance directly impacts user experience, SEO rankings, and conversion rates. In this comprehensive guide, I'll share the performance optimization techniques that have consistently delivered results in my projects.</p>
                
                <h3>Understanding Performance Metrics</h3>
                <p>Before optimizing, it's important to understand what to measure:</p>
                
                <h4>Core Web Vitals</h4>
                <ul>
                    <li><strong>Largest Contentful Paint (LCP):</strong> Measures loading performance</li>
                    <li><strong>First Input Delay (FID):</strong> Measures interactivity</li>
                    <li><strong>Cumulative Layout Shift (CLS):</strong> Measures visual stability</li>
                </ul>
                
                <h4>Additional Metrics</h4>
                <ul>
                    <li>First Contentful Paint (FCP)</li>
                    <li>Time to Interactive (TTI)</li>
                    <li>Total Blocking Time (TBT)</li>
                </ul>
                
                <h3>Image Optimization</h3>
                <p>Images often account for the majority of page weight. Here's how to optimize them:</p>
                
                <h4>Format Selection</h4>
                <ul>
                    <li><strong>WebP:</strong> Modern format with excellent compression</li>
                    <li><strong>AVIF:</strong> Next-generation format for even better compression</li>
                    <li><strong>JPEG:</strong> Good for photographs with fallback support</li>
                    <li><strong>PNG:</strong> Best for images with transparency</li>
                </ul>
                
                <h4>Responsive Images</h4>
                <p>Use the `srcset` attribute and `picture` element to serve appropriately sized images for different devices:</p>
                
                <pre><code>&lt;picture&gt;
  &lt;source media="(min-width: 800px)" srcset="large.webp" type="image/webp"&gt;
  &lt;source media="(min-width: 400px)" srcset="medium.webp" type="image/webp"&gt;
  &lt;img src="small.jpg" alt="Description" loading="lazy"&gt;
&lt;/picture&gt;</code></pre>
                
                <h3>JavaScript Optimization</h3>
                <p>JavaScript can significantly impact performance if not handled properly:</p>
                
                <h4>Code Splitting</h4>
                <p>Break your JavaScript into smaller chunks that load only when needed:</p>
                <ul>
                    <li>Route-based splitting for single-page applications</li>
                    <li>Component-based splitting for large components</li>
                    <li>Dynamic imports for feature-based splitting</li>
                </ul>
                
                <h4>Tree Shaking</h4>
                <p>Remove unused code from your bundles using modern build tools like Webpack or Vite.</p>
                
                <h3>CSS Optimization</h3>
                <p>CSS can also impact performance, especially on first paint:</p>
                
                <ul>
                    <li>Minimize and compress CSS files</li>
                    <li>Remove unused CSS with tools like PurgeCSS</li>
                    <li>Use critical CSS for above-the-fold content</li>
                    <li>Avoid CSS that blocks rendering</li>
                </ul>
                
                <h3>Caching Strategies</h3>
                <p>Effective caching can dramatically improve repeat visit performance:</p>
                
                <h4>Browser Caching</h4>
                <ul>
                    <li>Set appropriate cache headers for static assets</li>
                    <li>Use versioning for cache busting</li>
                    <li>Implement service workers for offline capability</li>
                </ul>
                
                <h4>CDN Usage</h4>
                <p>Content Delivery Networks reduce latency by serving content from geographically closer servers.</p>
                
                <h3>Performance Monitoring</h3>
                <p>Continuous monitoring is essential for maintaining performance:</p>
                
                <ul>
                    <li>Use Google PageSpeed Insights for audits</li>
                    <li>Implement Real User Monitoring (RUM)</li>
                    <li>Set up performance budgets</li>
                    <li>Monitor Core Web Vitals in production</li>
                </ul>
                
                <h3>Conclusion</h3>
                <p>Performance optimization is an ongoing process, not a one-time task. Start with the biggest wins (usually images and JavaScript), measure the impact, and iterate. Remember that the best optimization is often removing unnecessary features rather than making existing ones faster.</p>
                
                <p>Keep your users at the center of your optimization efforts – a fast, responsive website provides a better user experience and ultimately drives better business results.</p>
                ''',
                'categories': ['Web Development', 'Programming'],
                'author_name': 'Roshan Damor'
            },
            {
                'title': 'My Journey into Open Source Development',
                'summary': 'Personal reflections on contributing to open source projects, the challenges faced, lessons learned, and the impact on my development career.',
                'content': '''
                <p>Open source development has been one of the most rewarding aspects of my programming journey. It's not just about code – it's about community, learning, and giving back. Here's my story and what I've learned along the way.</p>
                
                <h3>The Beginning</h3>
                <p>My first open source contribution was intimidating. I found a small bug in a Python library I was using and spent weeks building up the courage to submit a pull request. The maintainers were incredibly welcoming, and that experience opened up a whole new world for me.</p>
                
                <h3>Why Open Source Matters</h3>
                <p>Contributing to open source has benefits that extend far beyond the code itself:</p>
                
                <h4>Skill Development</h4>
                <ul>
                    <li>Working with large, complex codebases</li>
                    <li>Learning from experienced developers</li>
                    <li>Understanding different coding styles and patterns</li>
                    <li>Improving documentation and communication skills</li>
                </ul>
                
                <h4>Career Growth</h4>
                <ul>
                    <li>Building a public portfolio of contributions</li>
                    <li>Networking with other developers</li>
                    <li>Gaining recognition in the developer community</li>
                    <li>Learning about project management and collaboration</li>
                </ul>
                
                <h3>Types of Contributions</h3>
                <p>Many people think open source is only about code, but there are many ways to contribute:</p>
                
                <ul>
                    <li><strong>Bug fixes:</strong> Often the best way to start</li>
                    <li><strong>Documentation:</strong> Always needed and highly appreciated</li>
                    <li><strong>Testing:</strong> Writing tests or reporting bugs</li>
                    <li><strong>Design:</strong> UI/UX improvements and assets</li>
                    <li><strong>Translation:</strong> Making projects accessible globally</li>
                    <li><strong>Community support:</strong> Helping other users and contributors</li>
                </ul>
                
                <h3>Finding Your First Project</h3>
                <p>Starting can be overwhelming with so many projects available. Here's my advice:</p>
                
                <ol>
                    <li><strong>Start with tools you use:</strong> Contribute to libraries or frameworks you're already familiar with</li>
                    <li><strong>Look for "good first issue" labels:</strong> Many projects tag beginner-friendly issues</li>
                    <li><strong>Check documentation:</strong> Often easier to improve than diving into complex code</li>
                    <li><strong>Attend events:</strong> Hacktoberfest and other events provide structured opportunities</li>
                </ol>
                
                <h3>Challenges and How to Overcome Them</h3>
                <p>Open source isn't always smooth sailing. Here are common challenges and solutions:</p>
                
                <h4>Imposter Syndrome</h4>
                <p>Feeling like you're not qualified to contribute is common. Remember that every expert was once a beginner, and maintainers appreciate help at all skill levels.</p>
                
                <h4>Difficult Feedback</h4>
                <p>Not all feedback is delivered kindly. Learn to separate constructive criticism from the delivery method, and don't take things personally.</p>
                
                <h4>Rejected Contributions</h4>
                <p>Not every pull request gets merged, and that's okay. Each attempt is a learning opportunity, and feedback helps you improve.</p>
                
                <h3>Best Practices</h3>
                <p>After years of contributing, here are my top tips:</p>
                
                <ul>
                    <li><strong>Read the contribution guidelines:</strong> Every project has different processes</li>
                    <li><strong>Start small:</strong> Small, focused contributions are easier to review and merge</li>
                    <li><strong>Communicate clearly:</strong> Explain your changes and why they're needed</li>
                    <li><strong>Be patient:</strong> Maintainers are often volunteers with limited time</li>
                    <li><strong>Follow up appropriately:</strong> Check in if your PR goes stale, but don't be pushy</li>
                </ul>
                
                <h3>My Notable Contributions</h3>
                <p>Over the years, I've contributed to various projects:</p>
                
                <ul>
                    <li>Added authentication features to a popular Django package</li>
                    <li>Improved documentation for React testing libraries</li>
                    <li>Created plugins for development tools</li>
                    <li>Helped translate software into multiple languages</li>
                </ul>
                
                <h3>Starting Your Own Projects</h3>
                <p>Eventually, you might want to create your own open source projects. Consider:</p>
                
                <ul>
                    <li>Solving a problem you personally face</li>
                    <li>Creating tools that improve your workflow</li>
                    <li>Contributing educational resources</li>
                    <li>Building community around shared interests</li>
                </ul>
                
                <h3>The Bigger Picture</h3>
                <p>Open source is about more than code – it's about building a more accessible, collaborative, and innovative world. Every contribution, no matter how small, makes a difference.</p>
                
                <p>If you haven't started contributing to open source yet, I encourage you to take that first step. The community is welcoming, the learning opportunities are endless, and the impact you can make is real.</p>
                
                <p>Feel free to reach out if you have questions about getting started. I'm always happy to help newcomers find their first contribution opportunity!</p>
                ''',
                'categories': ['Programming', 'Career Tips'],
                'author_name': 'Roshan Damor'
            }
        ]

        for blog_data in blogs_data:
            # Create blog
            blog = Blog.objects.create(
                title=blog_data['title'],
                summary=blog_data['summary'],
                content=blog_data['content'],
                author_name=blog_data['author_name'],
                created_date=timezone.now() - timedelta(days=random.randint(7, 180))
            )
            
            # Create and assign cover image
            cover_image = self.create_placeholder_image(
                800, 400, (random.randint(80, 180), random.randint(100, 200), random.randint(120, 220))
            )
            blog.cover_image.save(f'{blog.slug}_cover.jpg', cover_image, save=True)
            
            # Add categories
            for cat_name in blog_data['categories']:
                try:
                    cat = Category.objects.get(name=cat_name, category_type=Category.CategoryType.BLOG)
                    blog.categories.add(cat)
                except Category.DoesNotExist:
                    self.stdout.write(f'Warning: Blog category "{cat_name}" not found')
            
            # Add some comments
            for i in range(random.randint(2, 5)):
                Comment.objects.create(
                    post=blog,
                    author_name=random.choice([
                        'Sarah Chen', 'Michael Brown', 'Emma Watson', 'James Wilson',
                        'Lisa Anderson', 'Alex Rodriguez', 'Maya Patel', 'Chris Taylor'
                    ]),
                    body=random.choice([
                        'Excellent article! This really helped me understand the concepts better.',
                        'Thanks for sharing your experience. Very insightful and practical.',
                        'Great read! I especially appreciated the real-world examples.',
                        'This is exactly what I was looking for. Bookmarked for reference!',
                        'Well written and comprehensive. Looking forward to more content like this.',
                        'Your explanations are always so clear and easy to follow. Thank you!',
                        'Fantastic post! I learned a lot from your practical approach.',
                        'Really appreciate you taking the time to share these insights.'
                    ]),
                    likes=random.randint(0, 50),
                    created_date=timezone.now() - timedelta(days=random.randint(1, 30))
                )
            
            self.stdout.write(f'Created blog: {blog.title}')

    def create_experiences(self):
        """Create experience entries"""
        experiences_data = [
            {
                'company_name': 'TechCorp Solutions',
                'company_url': 'https://techcorp.example.com',
                'role': 'Senior Full Stack Developer',
                'start_date': datetime(2023, 1, 15).date(),
                'end_date': None,  # Current job
                'summary': 'Leading full-stack development projects and mentoring junior developers in modern web technologies.',
                'responsibilities': '''
                <ul>
                    <li>Architected and developed scalable web applications using Django and React</li>
                    <li>Led a team of 4 developers in delivering high-quality software solutions</li>
                    <li>Implemented CI/CD pipelines and improved deployment processes</li>
                    <li>Collaborated with product managers and designers to define technical requirements</li>
                    <li>Conducted code reviews and mentored junior developers</li>
                </ul>
                ''',
                'achievements': '''
                <ul>
                    <li>Reduced application load times by 40% through performance optimizations</li>
                    <li>Successfully delivered 5 major product features ahead of schedule</li>
                    <li>Improved team productivity by implementing automated testing workflows</li>
                    <li>Received "Outstanding Contributor" award for technical leadership</li>
                </ul>
                ''',
                'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker', 'AWS'],
                'experience_type': Experience.ExperienceType.FULL_TIME
            },
            {
                'company_name': 'StartupHub Inc',
                'company_url': 'https://startuphub.example.com',
                'role': 'Full Stack Developer',
                'start_date': datetime(2021, 6, 1).date(),
                'end_date': datetime(2022, 12, 31).date(),
                'summary': 'Developed and maintained multiple client projects in a fast-paced startup environment.',
                'responsibilities': '''
                <ul>
                    <li>Built responsive web applications from concept to deployment</li>
                    <li>Worked directly with clients to gather requirements and provide technical consultation</li>
                    <li>Developed RESTful APIs and integrated third-party services</li>
                    <li>Maintained and optimized existing applications for performance</li>
                    <li>Participated in agile development processes and sprint planning</li>
                </ul>
                ''',
                'achievements': '''
                <ul>
                    <li>Delivered 8 successful client projects with 100% satisfaction rate</li>
                    <li>Reduced development time by 30% by creating reusable component library</li>
                    <li>Implemented automated testing that caught 95% of bugs before production</li>
                    <li>Contributed to 50% increase in client retention through quality deliverables</li>
                </ul>
                ''',
                'technologies': ['Python', 'Django', 'JavaScript', 'Vue.js', 'MySQL', 'Git'],
                'experience_type': Experience.ExperienceType.FULL_TIME
            },
            {
                'company_name': 'Digital Innovations Lab',
                'company_url': 'https://digilab.example.com',
                'role': 'Python Developer Intern',
                'start_date': datetime(2021, 1, 15).date(),
                'end_date': datetime(2021, 5, 30).date(),
                'summary': 'Gained hands-on experience in web development and software engineering practices.',
                'responsibilities': '''
                <ul>
                    <li>Assisted in developing web applications using Python and Django</li>
                    <li>Wrote unit tests and participated in code reviews</li>
                    <li>Fixed bugs and implemented minor features under supervision</li>
                    <li>Created technical documentation for project features</li>
                    <li>Learned agile development methodologies and version control</li>
                </ul>
                ''',
                'achievements': '''
                <ul>
                    <li>Successfully completed all assigned tasks and projects</li>
                    <li>Received excellent feedback from senior developers and mentors</li>
                    <li>Contributed to improving internal development tools</li>
                    <li>Earned return offer for full-time position</li>
                </ul>
                ''',
                'technologies': ['Python', 'Django', 'HTML5', 'CSS3', 'JavaScript', 'Git'],
                'experience_type': Experience.ExperienceType.INTERNSHIP
            }
        ]

        for exp_data in experiences_data:
            experience = Experience.objects.create(
                company_name=exp_data['company_name'],
                company_url=exp_data['company_url'],
                role=exp_data['role'],
                start_date=exp_data['start_date'],
                end_date=exp_data['end_date'],
                summary=exp_data['summary'],
                responsibilities=exp_data['responsibilities'],
                achievements=exp_data['achievements'],
                experience_type=exp_data['experience_type']
            )
            
            # Add technologies
            for tech_name in exp_data['technologies']:
                try:
                    tech = Technology.objects.get(name=tech_name)
                    experience.technologies.add(tech)
                except Technology.DoesNotExist:
                    self.stdout.write(f'Warning: Technology "{tech_name}" not found, skipping...')
            
            self.stdout.write(f'Created experience: {experience.role} at {experience.company_name}')

    def create_services(self):
        """Create service entries"""
        services_data = [
            {
                'title': 'Web Development',
                'description': 'Full-stack web application development using modern frameworks and technologies.',
                'icon': 'fas fa-code',
                'order': 1
            },
            {
                'title': 'API Development',
                'description': 'RESTful and GraphQL API design and implementation for scalable applications.',
                'icon': 'fas fa-cogs',
                'order': 2
            },
            {
                'title': 'Database Design',
                'description': 'Efficient database architecture and optimization for high-performance applications.',
                'icon': 'fas fa-database',
                'order': 3
            },
            {
                'title': 'DevOps & Deployment',
                'description': 'CI/CD pipeline setup, containerization, and cloud deployment solutions.',
                'icon': 'fas fa-cloud',
                'order': 4
            },
            {
                'title': 'Technical Consulting',
                'description': 'Technology stack selection, architecture review, and performance optimization.',
                'icon': 'fas fa-lightbulb',
                'order': 5
            },
            {
                'title': 'Code Review & Mentoring',
                'description': 'Code quality assessment, best practices guidance, and developer mentoring.',
                'icon': 'fas fa-users',
                'order': 6
            }
        ]

        for service_data in services_data:
            service = Service.objects.create(**service_data)
            self.stdout.write(f'Created service: {service.title}')

    def manage_todo_list(self):
        """Update todo list status"""
        # Mark current todo as completed and next as in-progress
        pass