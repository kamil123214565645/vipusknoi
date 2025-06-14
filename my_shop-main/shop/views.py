from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse # Для генерации URL-адресов по их именам
from django.views.decorators.http import require_POST # Декоратор, разрешающий только POST-запросы
from django.views.generic import TemplateView # Базовый класс для простых страниц с шаблоном
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Для пагинации
from django.core.mail import send_mail # Для отправки email
from django.conf import settings # Для доступа к настройкам проекта
from django.db.models import Q # Для создания сложных поисковых запросов (OR-условия)
from django.utils import timezone # Для работы с временем (например, для купонов)
from django.contrib import messages
from .forms import CouponApplyForm, OrderCreateForm

from shop.cart import Cart # Для отображения флеш-сообщений пользователю

from .models import Product, Category, Coupon, Order, OrderItem # Модели данных

# --- Информационные страницы (используют Class-Based View - TemplateView) ---

class AboutUsView(TemplateView):
    template_name = 'shop/about_us.html'

class ContactInfoView(TemplateView):
    template_name = 'shop/contact_info.html'

# --- Представления для Корзины и Купонов ---

# Представление для добавления товара в корзину.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1, update_quantity=False)
    messages.success(request, f'Товар {product.name} был добавлен в вашу корзину')
    return redirect('shop:cart_detail')
# Представление для удаления товара из корзины.
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Товар {product.name} был удален из корзины')
    return redirect('shop:cart_detail')
# Представление для отображения страницы с деталями корзины.
def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()

    context = {'cart':cart,
               'coupon_apply_form': coupon_apply_form}

    return render(request, 'shop/cart/detail.html', context )

# Представление для применения купона к корзине.
@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST) 
    if form.is_valid():
        code = form.cleaned_data['code'] #LETO2025
        try:
            coupon = Coupon.objects.get(code__iexact=code)
            if coupon.is_valid():
                request.session['coupon_id'] = coupon.id
                messages.success(request, f'Купон {coupon.code} успешно применен!')
            else:
                request.session['coupon_id'] = None
                messages.warning(request, 'Данный купон недействителен')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'Купон с таким кодом не найден')
    else:
        messages.error(request, 'Введите код купона')
    return redirect('shop:cart_detail')

# --- Представления для Каталога товаров ---

# Представление для отображения списка товаров (главная страница каталога, категории, результаты поиска).
def product_list(request, category_slug=None):
    category = None # Текущая категория (None, если не выбрана)
    categories = Category.objects.all() # Все категории для отображения в сайдбаре
    products_queryset = Product.objects.filter(available=True).order_by('name') # Начальный QuerySet всех доступных товаров
    
    # Обработка поискового запроса
    query = request.GET.get('query', '').strip()
    if query:
        products_queryset = products_queryset.filter (
            Q(name__icontains=query) |  Q(description__icontains=query)
        ).distinct()

    # Фильтрация по категории, если передан category_slug
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_queryset = products_queryset.filter(category=category)

    # Пагинация для разбивки списка товаров на отдельные страницы
    paginator = Paginator(products_queryset, 3)
    page_number = request.GET.get('page')

    try:
        products_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        products_page_obj = paginator.page(1)
    except EmptyPage:
        products_page_obj = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'products': products_page_obj,
        'query': query,
    }
    return render(request, 'shop/product/list.html', context)

# Представление для отображения детальной информации о товаре.
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,
    available=True).exclude(id=product.id).order_by('?')[:4]

    context = {'product':product,
               'related_products':related_products}

    return render(request, 'shop/product/detail.html', context)

# --- Представления для Заказов ---

# Представление для создания (оформления) заказа.
def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            active_coupon = cart.coupon
            if active_coupon:
                order.coupon = active_coupon
                order.discount = active_coupon.discount
            order.save()
        for item_cart in cart:
            OrderItem.objects.create(
                order = order,
                product = item_cart['product'],
                price = item_cart['price'],
                quantity = item_cart['quantity']
            )

        request.session['order_id'] = order.id

        cart.clear()

        return redirect('shop:order_created')
    else:
        form = OrderCreateForm()

    context = {
        'cart': cart,
        'form':form
    }

    return render(request, 'shop/order/create.html', {'form':form})

# Представление для страницы "Спасибо за заказ" (подтверждение заказа).
def order_created(request):
    order_id = request.session.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except:
            messages.error(request, 'Не удалось найти информацию о вашем заказе')
            pass
    
    return render(request, 'shop/order/created.html', {'order' : order})
