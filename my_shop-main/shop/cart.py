from decimal import Decimal # Для точной работы с денежными суммами
from django.conf import settings # Для доступа к настройкам проекта (CART_SESSION_ID)
from .models import Product, Coupon # Импортируем модели Товара и Купона
from django.utils import timezone # Для проверки срока действия купона

class Cart:
    # Конструктор класса Cart. Вызывается при создании объекта корзины.
    # Принимает объект request, чтобы получить доступ к сессии.
    def __init__(self, request):
        self.session = request.session # Сохраняем сессию пользователя
        # Пытаемся получить данные корзины из сессии по ключу CART_SESSION_ID.
        cart_data = self.session.get(settings.CART_SESSION_ID)
        if not cart_data:
            # Если корзины в сессии нет, создаем пустой словарь для нее.
            cart_data = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart_data # Это основной словарь корзины {product_id: {'quantity': Q, 'price': P}}
        
        # Получаем ID примененного купона из сессии, если он есть.
        self.coupon_id = self.session.get('coupon_id')

    # Метод для добавления товара в корзину или обновления его количества.
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id) # Ключи в JSON (используется для сессий) должны быть строками.
        
        # Если товара еще нет в корзине, инициализируем его с ценой на момент добавления.
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if update_quantity:
            # Если update_quantity=True, просто устанавливаем новое количество.
            self.cart[product_id]['quantity'] = quantity
        else:
            # Иначе добавляем указанное количество к существующему.
            self.cart[product_id]['quantity'] += quantity
        
        # Сохраняем изменения в сессии.
        self.save()

    # Метод для сохранения состояния корзины в сессии.
    def save(self):
        # Помечаем сессию как измененную, чтобы Django сохранил ее.
        self.session.modified = True

    # Метод для удаления товара из корзины.
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # "Магический" метод, который позволяет итерироваться по объекту Cart (например, в цикле for в шаблоне).
    # Он будет возвращать каждый товар в корзине вместе с его данными (цена, количество, объект Product).
    def __iter__(self):
        product_ids = self.cart.keys() # Получаем ID всех товаров в корзине.
        
        # Получаем все объекты Product из базы данных одним запросом для эффективности.
        products = Product.objects.filter(id__in=product_ids)
        # Создаем словарь {product_id: product_object} для быстрого доступа к объектам Product.
        product_map = {str(p.id): p for p in products}

        cart_for_iteration = self.cart.copy() # Работаем с копией, чтобы не изменять self.cart напрямую

        for product_id, item_data_from_session in cart_for_iteration.items():
            product_object = product_map.get(product_id)
            if product_object: # Убедимся, что товар с таким ID все еще существует в БД
                # Создаем новый словарь для каждого элемента, чтобы безопасно добавлять объект 'product'
                current_item_details = item_data_from_session.copy()
                current_item_details['product'] = product_object # Добавляем сам объект Product
                current_item_details['price'] = Decimal(current_item_details['price']) # Преобразуем цену в Decimal
                current_item_details['total_price'] = current_item_details['price'] * current_item_details['quantity']
                yield current_item_details # Возвращаем подготовленный элемент корзины

    # "Магический" метод, который позволяет использовать len(cart) для получения общего кол-ва единиц товаров.
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Метод для получения общей стоимости всех товаров в корзине (до применения скидки).
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # Property для получения объекта Coupon, если он применен и валиден.
    # @property позволяет обращаться к методу как к атрибуту (cart.coupon).
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                coupon_obj = Coupon.objects.get(id=self.coupon_id)
                # Дополнительно проверяем валидность купона здесь,
                # так как он мог стать невалидным после добавления в сессию.
                if coupon_obj.is_valid():
                    return coupon_obj
                else:
                    # Если купон стал невалидным, удаляем его из сессии.
                    self.session['coupon_id'] = None
                    self.save()
            except Coupon.DoesNotExist:
                # Если купон с таким ID был удален из БД, очищаем его из сессии.
                self.session['coupon_id'] = None
                self.save()
        return None # Если купона нет или он невалиден

    # Метод для расчета суммы скидки по купону.
    def get_discount_amount(self):
        active_coupon = self.coupon # Получаем текущий валидный купон через property
        if active_coupon:
            # Рассчитываем скидку от общей суммы товаров (до скидки).
            return (Decimal(active_coupon.discount) / Decimal('100')) * self.get_subtotal_price()
        return Decimal('0') # Если купона нет, скидка 0.

    # Метод для получения итоговой стоимости корзины (с учетом скидки).
    def get_total_price(self):
        return self.get_subtotal_price() - self.get_discount_amount()

    # Метод для полной очистки корзины (удаление товаров и купона из сессии).
    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        if 'coupon_id' in self.session:
            del self.session['coupon_id']
        self.save() # Сохраняем сессию после удаления ключей.