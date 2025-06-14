"""
ASGI config for my_shop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Указывает Django путь к файлу настроек проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_shop.settings')

# Получает ASGI-приложение для проекта.
application = get_asgi_application()