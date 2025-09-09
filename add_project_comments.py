import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project, ProjectComment
from datetime import datetime, timedelta

# Get some projects
projects = Project.objects.all()[:3]  # Get first 3 projects

sample_comments = [
    {
        'author_name': 'Alex Johnson',
        'body': 'This is an amazing project! The implementation is really clean and well-documented. I especially love the user interface design.',
        'likes': 15
    },
    {
        'author_name': 'Sarah Chen',
        'body': 'Great work on this! I\'ve been looking for something exactly like this. The features are comprehensive and the performance looks excellent.',
        'likes': 8
    },
    {
        'author_name': 'Mike Rodriguez',
        'body': 'Impressive project! The code architecture is well thought out. Would love to see more features like this in the future.',
        'likes': 12
    },
    {
        'author_name': 'Emily Davis',
        'body': 'This project solved exactly the problem I was facing. The documentation is clear and the setup process was smooth. Thank you!',
        'likes': 6
    },
    {
        'author_name': 'David Wilson',
        'body': 'Outstanding work! The attention to detail is remarkable. Looking forward to contributing to this project.',
        'likes': 10
    },
    {
        'author_name': 'Lisa Thompson',
        'body': 'Really well executed project. The user experience is intuitive and the functionality is robust. Keep up the great work!',
        'likes': 7
    }
]

# Add comments to each project
for project in projects:
    print(f"Adding comments to project: {project.title}")
    
    # Add 2-3 comments per project
    for i, comment_data in enumerate(sample_comments[:3]):
        comment = ProjectComment.objects.create(
            project=project,
            author_name=comment_data['author_name'],
            body=comment_data['body'],
            likes=comment_data['likes'],
            is_approved=True
        )
        print(f"  - Added comment by {comment.author_name}")
    
    # Rotate the sample comments for variety
    sample_comments = sample_comments[3:] + sample_comments[:3]

print("\nSample project comments added successfully!")
