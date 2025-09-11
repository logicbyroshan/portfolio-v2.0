import sys
import os

# Add your project directory to Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'portfolio2.0'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
