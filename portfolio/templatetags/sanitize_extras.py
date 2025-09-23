from django import template
import bleach
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    "b", "i", "strong", "em", "u", "a", "br", "p",
    "ul", "ol", "li", "span", "h1", "h2", "h3", "h4"
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "span": ["style"],
}

@register.filter(name="sanitize_html")
def sanitize_html_filter(value):
    if value:
        cleaned = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
        return mark_safe(cleaned)   # ✅ ensures HTML is rendered, not escaped
    return value
