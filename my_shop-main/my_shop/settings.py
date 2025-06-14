from pathlib import Path
import os # Иногда используется для BASE_DIR, но Path более современно

# BASE_DIR определяет абсолютный путь к корневой директории проекта.
# Path(__file__) - текущий файл (settings.py)
# .resolve() - получает полный путь
# .parent - родительская директория (my_shop/)
# .parent - еще раз родительская директория (корневая папка проекта)
BASE_DIR = Path(__file__).resolve().parent.parent

# КЛЮЧ СЕКРЕТНОСТИ - ВАЖНО!
# Используется для криптографической подписи (например, сессий, CSRF токенов).
# В реальном проекте (production) его нужно хранить в секрете и не выкладывать в репозиторий.
# Для разработки можно использовать сгенерированный автоматически.
SECRET_KEY = 'django-insecure-your-very-secret-key-here-change-me!' # !!! ЗАМЕНИ ЭТО НА СВОЙ УНИКАЛЬНЫЙ КЛЮЧ !!!

# РЕЖИМ ОТЛАДКИ (DEBUG)
# DEBUG = True - в режиме разработки. Показывает подробные страницы ошибок.
# DEBUG = False - в рабочем (production) режиме. Никогда не используй True в production!
DEBUG = True

# СПИСОК РАЗРЕШЕННЫХ ХОСТОВ/ДОМЕНОВ
# Если DEBUG = False, Django будет обслуживать запросы только для хостов из этого списка.
# В режиме разработки (DEBUG = True) обычно можно оставить пустым,
# Django по умолчанию разрешает '127.0.0.1', 'localhost'.
# Для production сюда нужно добавить доменное имя твоего сайта, например, ['www.myshop.com', 'myshop.com']
ALLOWED_HOSTS = []


# СПИСОК УСТАНОВЛЕННЫХ ПРИЛОЖЕНИЙ
# Здесь перечислены все Django-приложения, которые используются в проекте.
# Некоторые из них - встроенные (django.contrib...), другие - твои собственные (shop).
INSTALLED_APPS = [
    'django.contrib.admin',       # Административный интерфейс Django
    'django.contrib.auth',        # Система аутентификации (пользователи, группы, права)
    'django.contrib.contenttypes',# Фреймворк для типов контента (используется другими приложениями)
    'django.contrib.sessions',    # Фреймворк для работы с сессиями (например, для корзины)
    'django.contrib.messages',    # Фреймворк для отображения одноразовых сообщений (например, "Товар добавлен")
    'django.contrib.staticfiles', # Для управления статическими файлами (CSS, JS, изображения дизайна)
    'shop',                       # Наше приложение магазина
]

# ПРОМЕЖУТОЧНОЕ ПО (MIDDLEWARE)
# Middleware - это компоненты, которые обрабатывают запрос/ответ на разных стадиях.
# Порядок Middleware важен!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Защитные механизмы (XSS, Clickjacking и т.д.)
    'django.contrib.sessions.middleware.SessionMiddleware',   # Включает поддержку сессий
    'django.middleware.common.CommonMiddleware',              # Общие операции (например, обработка URL со слешем в конце)
    'django.middleware.csrf.CsrfViewMiddleware',              # Защита от CSRF-атак (подделка межсайтовых запросов)
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Связывает пользователя с запросом (request.user)
    'django.contrib.messages.middleware.MessageMiddleware',   # Включает поддержку сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от кликджекинга
]

# КОРНЕВОЙ URLCONF
# Указывает Django, какой Python-модуль использовать в качестве главного файла URL-маршрутизации.
ROOT_URLCONF = 'my_shop.urls'

# НАСТРОЙКИ ШАБЛОНОВ
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Используемый шаблонизатор
        'DIRS': [BASE_DIR / 'templates'], # Список директорий, где Django будет искать шаблоны на уровне проекта (если есть)
        'APP_DIRS': True, # Указывает Django искать шаблоны в папке 'templates' каждого приложения из INSTALLED_APPS
        'OPTIONS': {
            'context_processors': [ # Функции, добавляющие переменные в контекст каждого шаблона
                'django.template.context_processors.debug',   # Переменные для отладки (DEBUG, sql_queries)
                'django.template.context_processors.request', # Объект HttpRequest (request)
                'django.contrib.auth.context_processors.auth',    # Пользователь (user) и права (perms)
                'django.contrib.messages.context_processors.messages',# Сообщения (messages)
                'shop.context_processors.cart',                   # Наш процессор для доступа к корзине во всех шаблонах
                'shop.context_processors.search_form_context',    # Наш процессор для формы поиска
            ],
        },
    },
]

# WSGI ПРИЛОЖЕНИЕ
# Указывает путь к WSGI-совместимому приложению, которое веб-сервер будет использовать для запуска проекта.
WSGI_APPLICATION = 'my_shop.wsgi.application'


# НАСТРОЙКИ БАЗЫ ДАННЫХ
# По умолчанию используется SQLite, что удобно для разработки.
# Для production обычно используют PostgreSQL, MySQL или другие.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Тип базы данных
        'NAME': BASE_DIR / 'db.sqlite3',       # Имя файла базы данных (для SQLite)
    }
}


# ВАЛИДАТОРЫ ПАРОЛЕЙ
# Набор правил для проверки сложности паролей пользователей.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',}, # Пароль не должен быть слишком похож на другие данные пользователя
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},          # Минимальная длина пароля
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},           # Пароль не должен быть из списка слишком распространенных
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},          # Пароль не должен состоять только из цифр
]


# ИНТЕРНАЦИОНАЛИЗАЦИЯ И ЛОКАЛИЗАЦИЯ (I18N, L10N)
LANGUAGE_CODE = 'ru-ru' # Язык по умолчанию для проекта (русский)

TIME_ZONE = 'Asia/Bishkek' # Ваш часовой пояс (например, для Кыргызстана). Важно для корректного отображения времени.

USE_I18N = True # Включает систему перевода Django.

USE_TZ = True   # Включает поддержку часовых поясов. Django будет хранить дату/время в UTC в базе данных
                # и конвертировать в локальное время при отображении.


# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JavaScript, изображения дизайна)
STATIC_URL = 'static/' # URL-префикс для статических файлов (например, /static/css/base.css)

# Куда собирать все статические файлы при выполнении команды `collectstatic` (для production).
# В режиме разработки (DEBUG=True) Django сам находит статику в папках 'static' приложений.
# STATIC_ROOT = BASE_DIR / 'staticfiles' 

# Дополнительные пути к статическим файлам на уровне проекта (если есть).
# STATICFILES_DIRS = [BASE_DIR / 'static',]


# МЕДИА ФАЙЛЫ (загружаемые пользователем, например, изображения товаров)
MEDIA_URL = '/media/' # URL-префикс для медиа-файлов
MEDIA_ROOT = BASE_DIR / 'media' # Абсолютный путь в файловой системе, где будут храниться медиа-файлы


# ТИП ПЕРВИЧНОГО КЛЮЧА ПО УМОЛЧАНИЮ
# Для новых приложений и моделей, если не указан явно тип первичного ключа.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Использует 64-битное целое число

# КЛЮЧ ДЛЯ КОРЗИНЫ В СЕССИИ
# Имя ключа, под которым данные корзины будут храниться в сессии пользователя.
CART_SESSION_ID = 'cart'

# НАСТРОЙКИ EMAIL
# Для разработки удобно выводить письма в консоль, а не отправлять реально.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Для реальной отправки почты (production) нужно будет настроить SMTP-сервер:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'  # Адрес вашего SMTP-сервера
# EMAIL_PORT = 587                 # Порт SMTP-сервера (587 для TLS, 465 для SSL)
# EMAIL_USE_TLS = True             # Использовать TLS (True для порта 587)
# EMAIL_USE_SSL = False            # Использовать SSL (True для порта 465)
# EMAIL_HOST_USER = 'your_email@example.com'  # Ваш email для входа на SMTP-сервер
# EMAIL_HOST_PASSWORD = 'your_email_password' # Пароль от вашего email
# DEFAULT_FROM_EMAIL = 'noreply@myshop.example.com' # Email отправителя по умолчанию