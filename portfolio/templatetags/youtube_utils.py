# myapp/templatetags/youtube_utils.py
from django import template
import re
register = template.Library()

@register.filter
def youtube_embed(url):

    if not url:
        return ''
    patterns = [
        r'(?:v=|/v/|embed/|youtu\.be/)([A-Za-z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            vid = m.group(1)
            return f'https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1'
    return ''
