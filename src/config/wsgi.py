"""
WSGI config for ogani-e-commerce-site project.
Exposes WSGI callable as `application`.
"""

import os
import sys
from pathlib import Path

# Add src to sys.path
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
