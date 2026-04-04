import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "azbuka_math.settings")

application = get_wsgi_application()
