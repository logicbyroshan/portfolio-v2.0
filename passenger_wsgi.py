import sys
import os

# Add your project directory to Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'portfolio-2.0'))

# Set Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
