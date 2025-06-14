from django.db import models
from django.urls import reverse # Для генерации URL-адресов объектов (метод get_absolute_url)
from django.core.validators import MinValueValidator, MaxValueValidator # Для валидации числовых полей
from django.utils import timezone # Для работы с датой/временем (например, для купонов)
from decimal import Decimal # Для точных денежных расчетов

# Модель для категорий товаров
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')
    # Slug - это URL-дружественная версия названия (например, "smartfony-apple" для "Смартфоны Apple").
    # unique=True гарантирует, что слаги не будут повторяться.
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-слаг')

    # Meta-класс для настройки поведения модели
    class Meta:
        ordering = ['name'] # Порядок сортировки категорий по умолчанию (по имени)
        verbose_name = 'категория' # Имя модели в единственном числе (для админки)
        verbose_name_plural = 'категории' # Имя модели во множественном числе (для админки)

    # Строковое представление объекта Category (например, в админке или при выводе)
    def __str__(self):
        return self.name

    # Метод для получения канонического URL-адреса объекта категории.
    # Используется в шаблонах для создания ссылок на страницы категорий.
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

# Модель для товаров
class Product(models.Model):
    # Связь "один-ко-многим" с моделью Category (одна категория - много товаров).
    # related_name='products' позволяет обращаться из категории к ее товарам (category.products.all()).
    # on_delete=models.CASCADE означает, что при удалении категории удалятся все связанные с ней товары.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-слаг товара')
    # Поле для изображения товара.
    # upload_to указывает путь для сохранения изображений (относительно MEDIA_ROOT).
    # %Y/%m/%d - создаст подпапки по году/месяцу/дню.
    # blank=True означает, что поле необязательное (товар может быть без картинки).
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    # DecimalField используется для денег, чтобы избежать проблем с точностью float.
    # max_digits - общее кол-во цифр, decimal_places - кол-во знаков после запятой.
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='В наличии') # Доступен ли товар для продажи
    # auto_now_add=True - дата/время будет установлено автоматически при создании объекта.
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # auto_now=True - дата/время будет обновляться автоматически при каждом сохранении объекта.
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['name'] # Сортировка товаров по умолчанию
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        # Индексы для slug (unique=True) и id (primary_key=True) создаются автоматически.
        # Если часто ищутся товары по имени, можно добавить: models.Index(fields=['name'])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

# Модель для купонов на скидку
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код купона')
    valid_from = models.DateTimeField(verbose_name='Действителен с') # Дата начала действия купона
    valid_to = models.DateTimeField(verbose_name='Действителен до')   # Дата окончания действия купона
    # Скидка в процентах. Валидаторы проверяют, что значение от 0 до 100.
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Скидка в %')
    active = models.BooleanField(default=True, verbose_name='Активен') # Активен ли купон

    class Meta:
        verbose_name = 'купон'
        verbose_name_plural = 'купоны'
        ordering = ['-valid_to'] # Сначала купоны, которые скоро закончатся или недавно закончились

    def __str__(self):
        return self.code

    # Метод для проверки, является ли купон действительным на текущий момент
    def is_valid(self):
        now = timezone.now() # Текущее время с учетом часового пояса
        return self.active and self.valid_from <= now <= self.valid_to

# Модель для заказов
class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен') # Статус оплаты заказа
    
    # Связь с купоном (если он был применен к заказу)
    # null=True, blank=True - купон необязателен
    # on_delete=models.SET_NULL - если купон удалят, в заказе это поле станет NULL (связь не удалит заказ)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True,
                               on_delete=models.SET_NULL, verbose_name='Купон')
    # Процент скидки, который был применен к этому заказу (копируется из купона)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Скидка по купону в %')

    class Meta:
        ordering = ['-created'] # Новые заказы первыми
        indexes = [ # Индекс для ускорения выборки заказов по дате создания
            models.Index(fields=['-created']),
        ]
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    # Общая стоимость товаров в заказе (до применения скидки по купону)
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    # Сумма скидки по купону для этого заказа
    def get_discount_amount(self):
        if self.coupon and self.discount > 0: # Убеждаемся, что купон применен и скидка есть
            return (Decimal(self.discount) / Decimal('100')) * self.get_total_cost_before_discount()
        return Decimal('0') # Если нет купона или скидки, возвращаем 0

    # Итоговая стоимость заказа (с учетом скидки)
    def get_total_cost(self):
        total_cost_before_discount = self.get_total_cost_before_discount()
        return total_cost_before_discount - self.get_discount_amount()

    # Метод для генерации темы email-сообщения
    def get_email_subject(self):
        return f'Заказ №{self.id} в "Мой магазин" успешно оформлен'

    # Метод для генерации тела email-сообщения (список строк)
    def get_email_body_lines(self):
        lines = [
            f'Уважаемый {self.first_name},',
            f'', # Пустая строка для абзаца
            f'Ваш заказ №{self.id} на сумму ${self.get_total_cost():.2f} успешно оформлен и принят в обработку.',
            f'Статус оплаты: {"Оплачен" if self.paid else "Ожидает оплаты"}.',
            f'',
            'Детали заказа:'
        ]
        # self.items - это related_name='items' из модели OrderItem
        for item in self.items.all():
            lines.append(f"- {item.product.name} (x{item.quantity}): ${item.get_cost():.2f}")
        
        lines.append(f"")
        lines.append(f"Общая стоимость товаров (до скидки): ${self.get_total_cost_before_discount():.2f}")
        if self.coupon: # Если был применен купон
            lines.append(f"Применен купон: {self.coupon.code} (скидка {self.discount}%)")
            lines.append(f"Сумма скидки: -${self.get_discount_amount():.2f}")
        lines.append(f"Итого к оплате: ${self.get_total_cost():.2f}")
        lines.append(f"")
        lines.append(f"Адрес доставки: {self.city}, {self.address}, {self.postal_code}")
        lines.append(f"")
        lines.append('Спасибо за покупку!')
        lines.append('С уважением, команда "Мой магазин".')
        return lines

# Модель для отдельной позиции (товара) в заказе
class OrderItem(models.Model):
    # Связь с заказом, к которому относится эта позиция
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Связь с товаром, который был куплен
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    # Цена товара на момент покупки (важно, т.к. цена на сайте может измениться)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена (на момент покупки)')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'позиции заказа'

    def __str__(self):
        return str(self.id) # Или f'{self.product.name} (x{self.quantity})'

    # Стоимость данной позиции заказа (цена * количество)
    def get_cost(self):
        return self.price * self.quantity