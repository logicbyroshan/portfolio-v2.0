"""
Django settings package for portfolio project.
"""

import os

# Determine which settings to use based on environment
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'staging':
    from .production import *
    DEBUG = True
    ALLOWED_HOSTS = ['staging.roshandamor.me', 'staging.roshanproject.site']
else:
    from .development import *
