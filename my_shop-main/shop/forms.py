from django import forms
from .models import Order # Модель Order используется для OrderCreateForm

# Форма для создания заказа, основанная на модели Order.
# ModelForm автоматически создает поля формы на основе полей модели.
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order # Указываем, какую модель использовать
        # Список полей модели, которые должны быть включены в форму.
        # Поля 'created', 'updated', 'paid', 'coupon', 'discount' не включаются,
        # так как они устанавливаются автоматически или не предназначены для ввода пользователем на этом этапе.
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
        # Можно настроить виджеты для полей, если нужно изменить их стандартное отображение
        # Например, добавить плейсхолдеры:
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
        #     'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
        #     'email': forms.EmailInput(attrs={'placeholder': 'example@mail.com'}),
        #     'address': forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}),
        #     'postal_code': forms.TextInput(attrs={'placeholder': '123456'}),
        #     'city': forms.TextInput(attrs={'placeholder': 'Город'}),
        # }

# Форма для применения купона на скидку.
# Это простая форма, не связанная с моделью напрямую (forms.Form).
class CouponApplyForm(forms.Form):
    # Одно поле для ввода кода купона.
    code = forms.CharField(
        label='Код купона', # Метка поля, отображаемая в шаблоне
        required=True,      # Поле обязательно для заполнения
        widget=forms.TextInput(attrs={'placeholder': 'Введите код купона'}) # HTML-атрибуты виджета
    )

# Форма для поиска товаров.
class SearchForm(forms.Form):
    # Одно поле для ввода поискового запроса.
    query = forms.CharField(
        label=False, # Не отображать стандартную метку поля (используем placeholder)
        required=False, # Поиск может быть пустым (тогда отобразятся все товары)
        widget=forms.TextInput(attrs={'placeholder': 'Поиск товаров...'})
    )