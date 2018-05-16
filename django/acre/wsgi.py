"""
WSGI config for acre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

path = '/var/websites/personal/acre/'
if path not in sys.path:
    sys.path.append(path)

path = '/var/websites/personal/acre/django/'
if path not in sys.path:
    sys.path.append(path)


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acre.settings")

application = get_wsgi_application()
