import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project, ProjectComment

# Get the AI Chatbot project
project = Project.objects.get(slug='ai-chatbot')

# Add more comments to test pagination
additional_comments = [
    {
        'author_name': 'Jennifer Lee',
        'body': 'The AI responses are incredibly natural and contextual. This is exactly what I needed for my customer service automation project.',
        'likes': 9
    },
    {
        'author_name': 'Robert Taylor',
        'body': 'Fantastic implementation! The code is well-structured and the documentation makes it easy to understand and extend.',
        'likes': 14
    },
    {
        'author_name': 'Maria Garcia',
        'body': 'This chatbot has transformed how we handle customer inquiries. The integration was seamless and the performance is excellent.',
        'likes': 11
    },
    {
        'author_name': 'James Wilson',
        'body': 'Outstanding work on the natural language processing. The bot understands context remarkably well.',
        'likes': 7
    },
    {
        'author_name': 'Ashley Brown',
        'body': 'Really impressed with the conversation flow management. This is production-ready code!',
        'likes': 13
    },
    {
        'author_name': 'Kevin Martinez',
        'body': 'The chatbot\'s ability to maintain context across multiple exchanges is remarkable. Great architecture choices!',
        'likes': 8
    },
    {
        'author_name': 'Laura Davis',
        'body': 'Clean, efficient code with excellent error handling. This project demonstrates real expertise in AI development.',
        'likes': 16
    }
]

print(f"Adding more comments to: {project.title}")

for comment_data in additional_comments:
    comment = ProjectComment.objects.create(
        project=project,
        author_name=comment_data['author_name'],
        body=comment_data['body'],
        likes=comment_data['likes'],
        is_approved=True
    )
    print(f"  - Added comment by {comment.author_name}")

print(f"\nTotal comments for {project.title}: {project.comments.count()}")
