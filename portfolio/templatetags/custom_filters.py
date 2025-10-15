from django import template
import re

register = template.Library()

@register.filter
def initials(name):
    """Generate initials from a full name.
    
    Examples:
    - "Roshan Damor" -> "RD"
    - "John Smith Johnson" -> "JSJ"
    - "Madonna" -> "M"
    - "john doe" -> "JD"
    """
    if not name:
        return "?"
    
    # Split name by spaces and filter out empty strings
    words = [word.strip() for word in name.split() if word.strip()]
    
    if not words:
        return "?"
    
    # Get first letter of each word, limit to 3 letters max
    initials_list = []
    for word in words[:3]:  # Limit to first 3 words
        first_char = word[0].upper()
        # Only add alphabetic characters
        if first_char.isalpha():
            initials_list.append(first_char)
    
    # If no valid letters found, return first character or ?
    if not initials_list:
        first_char = name[0].upper() if name else "?"
        return first_char if first_char.isalpha() else "?"
    
    return "".join(initials_list)

@register.filter
def avatar_color(name):
    """Generate a consistent color for avatar based on name."""
    if not name:
        return "#6366f1"
    
    # Generate hash from name to ensure consistent colors
    hash_value = abs(hash(name.lower()))
    
    # Predefined color palette
    colors = [
        "#ef4444", # red
        "#f97316", # orange  
        "#eab308", # yellow
        "#22c55e", # green
        "#06b6d4", # cyan
        "#3b82f6", # blue
        "#6366f1", # indigo
        "#8b5cf6", # violet
        "#ec4899", # pink
        "#f59e0b", # amber
        "#10b981", # emerald
        "#6366f1", # indigo (duplicate for better distribution)
    ]
    
    return colors[hash_value % len(colors)]
