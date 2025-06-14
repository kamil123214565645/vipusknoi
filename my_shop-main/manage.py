#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Устанавливает переменную окружения 'DJANGO_SETTINGS_MODULE',
    # чтобы Django знал, где искать файл настроек вашего проекта.
    # 'my_shop.settings' означает, что файл settings.py находится в папке my_shop.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_shop.settings')
    try:
        # Пытаемся импортировать функцию execute_from_command_line,
        # которая отвечает за выполнение команд Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Если Django не установлен или не доступен, будет вызвана ошибка ImportError.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Передает аргументы командной строки (например, 'runserver', 'makemigrations')
    # функции execute_from_command_line для их выполнения.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Эта стандартная конструкция Python гарантирует, что функция main()
    # будет вызвана только тогда, когда скрипт выполняется напрямую,
    # а не когда он импортируется как модуль в другой скрипт.
    main()