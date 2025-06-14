from django.contrib import admin
from django.urls import path, include # include используется для подключения URL-ов из других приложений
from django.conf import settings # Для доступа к настройкам проекта (например, DEBUG, MEDIA_URL)
from django.conf.urls.static import static # Для обслуживания медиа-файлов в режиме разработки

# Список URL-шаблонов для всего проекта.
# Django просматривает этот список сверху вниз и использует первое совпадение.
urlpatterns = [
    # URL для административного интерфейса Django (например, http://127.0.0.1:8000/admin/)
    path('admin/', admin.site.urls),

    # Подключаем все URL-шаблоны из нашего приложения 'shop'.
    # Пустой префикс '' означает, что URL-ы из shop.urls будут доступны от корня сайта.
    # namespace='shop' позволяет однозначно ссылаться на URL-ы этого приложения
    # (например, {% url 'shop:product_list' %}).
    path('', include('shop.urls', namespace='shop')),
]

# Специальное правило для режима разработки (DEBUG = True).
# Позволяет Django-серверу разработки обслуживать медиа-файлы (загруженные пользователем изображения).
# В рабочем (production) режиме медиа-файлы обычно обслуживаются веб-сервером (например, Nginx).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Можно также добавить обслуживание статических файлов Django-сервером разработки,
    # если STATIC_ROOT определен, но обычно это не требуется, так как APP_DIRS=True в TEMPLATES
    # и `django.contrib.staticfiles` обрабатывают статику приложений.
    # if settings.STATIC_ROOT:
    #    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)