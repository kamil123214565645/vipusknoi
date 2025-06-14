from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Coupon # Импортируем все модели

# Регистрация модели Category с кастомными настройками для админки
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке категорий
    list_display = ['name', 'slug']
    # Поле 'slug' будет автоматически заполняться на основе значения поля 'name'
    # при создании новой категории (удобно для генерации URL-дружественных слагов).
    prepopulated_fields = {'slug': ('name',)}

# Регистрация модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля в списке товаров
    list_display = ['name', 'slug', 'category', 'price', 'available', 'created', 'updated']
    # Фильтры, которые будут доступны в боковой панели для фильтрации списка товаров
    list_filter = ['available', 'created', 'updated', 'category']
    # Поля, которые можно редактировать прямо в списке товаров (без перехода на страницу редактирования товара)
    list_editable = ['price', 'available']
    # Автозаполнение 'slug' из 'name'
    prepopulated_fields = {'slug': ('name',)}
    # Поля, по которым будет работать поиск в админке
    search_fields = ['name', 'description']

# Класс для встроенного отображения OrderItem на странице Order
class OrderItemInline(admin.TabularInline): # TabularInline отображает элементы в табличном виде
    model = OrderItem # Модель, которую будем отображать
    # raw_id_fields позволяет выбирать связанный товар через ввод ID,
    # что удобнее, чем выпадающий список, если товаров много.
    raw_id_fields = ['product']
    extra = 0 # Не показывать пустые строки для добавления новых OrderItem по умолчанию

# Регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Поля в списке заказов
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 
                    'coupon', 'discount', 'created', 'city']
    # Фильтры для списка заказов
    list_filter = ['paid', 'created', 'updated', 'coupon']
    # Поиск по заказам
    search_fields = ['id', 'first_name', 'last_name', 'email']
    # Включаем отображение OrderItemInline на странице редактирования заказа
    inlines = [OrderItemInline]
    # Поля, которые будут только для чтения (их нельзя будет изменить в админке)
    readonly_fields = ['created', 'updated', 'get_total_cost_display', 
                       'get_discount_amount_display', 'get_final_cost_display'] 
                       # Добавим кастомные поля для отображения стоимости

    # Кастомные поля для отображения в админке (не поля модели)
    def get_total_cost_display(self, obj):
        return f"${obj.get_total_cost_before_discount():.2f}"
    get_total_cost_display.short_description = 'Сумма (до скидки)'

    def get_discount_amount_display(self, obj):
        return f"${obj.get_discount_amount():.2f}"
    get_discount_amount_display.short_description = 'Скидка'

    def get_final_cost_display(self, obj):
        return f"${obj.get_total_cost():.2f}"
    get_final_cost_display.short_description = 'Итоговая сумма'

    # Добавляем кастомные методы в fieldsets или list_display, если нужно
    # fieldsets можно использовать для группировки полей на странице редактирования


# Регистрация модели Coupon
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    # Поля в списке купонов
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    # Фильтры для списка купонов
    list_filter = ['active', 'valid_from', 'valid_to']
    # Поиск по купонам
    search_fields = ['code']