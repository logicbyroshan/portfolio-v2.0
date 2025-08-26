from django.core.management.base import BaseCommand
from portfolio.models import VideoResume

class Command(BaseCommand):
    help = 'Add or update video resume URL'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str, help='YouTube embed URL (e.g., https://www.youtube.com/embed/VIDEO_ID)')

    def handle(self, *args, **options):
        youtube_url = options['youtube_url']
        
        # Validate URL format
        if not youtube_url.startswith('https://www.youtube.com/embed/'):
            self.stdout.write(
                self.style.ERROR('Please provide a valid YouTube embed URL starting with "https://www.youtube.com/embed/"')
            )
            return
        
        # Create or update the video resume
        video_resume, created = VideoResume.objects.get_or_create(pk=1)
        video_resume.youtube_embed_url = youtube_url
        video_resume.save()
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created video resume with URL: {youtube_url}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated video resume with URL: {youtube_url}')
            )
