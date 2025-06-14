"""
WSGI config for my_shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Указывает Django путь к файлу настроек проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_shop.settings')

# Получает WSGI-приложение для проекта.
application = get_wsgi_application()