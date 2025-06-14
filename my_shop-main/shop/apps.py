from django.apps import AppConfig

class ShopConfig(AppConfig):
    # Тип поля для автоинкрементных первичных ключей в моделях этого приложения.
    # BigAutoField использует 64-битное целое число.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Имя приложения. Должно совпадать с именем директории приложения.
    name = 'shop'
    
    # verbose_name = "Магазин" # Можно задать человекочитаемое имя для админки