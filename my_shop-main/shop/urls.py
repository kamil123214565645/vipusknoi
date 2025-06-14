from django.urls import path
from . import views # Импортируем представления из текущего приложения (shop.views)

# Пространство имен для URL-шаблонов этого приложения.
# Позволяет использовать, например, {% url 'shop:product_list' %} в шаблонах.
app_name = 'shop'

# Список URL-шаблонов для приложения 'shop'.
# Django будет искать совпадения по порядку.
urlpatterns = [
    # URL-ы для информационных страниц (используют TemplateView)
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('contact-info/', views.ContactInfoView.as_view(), name='contact_info'),

    # URL-ы для корзины и купонов
    path('cart/', views.cart_detail, name='cart_detail'), # Страница с деталями корзины
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'), # Добавление товара в корзину
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'), # Удаление товара из корзины
    path('coupons/apply/', views.coupon_apply, name='coupon_apply'), # Применение купона

    # URL-ы для заказов
    path('order/create/', views.order_create, name='order_create'), # Страница оформления заказа
    path('order/created/', views.order_created, name='order_created'), # Страница подтверждения заказа
    # URL-ы для каталога товаров
    # Пустой путь '' для главной страницы каталога (также обрабатывает поиск)
    path('', views.product_list, name='product_list'), 
    # URL для отображения товаров по категории (например, /tovary-dlya-doma/)
    # <slug:category_slug> захватывает часть URL как переменную category_slug
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # URL для детальной страницы товара (например, /123/super-tovar/)
    # <int:id> захватывает числовой ID, <slug:slug> - слаг товара.
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
