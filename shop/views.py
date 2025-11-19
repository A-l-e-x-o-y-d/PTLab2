from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['person', 'address', 'promo_code']

    def form_valid(self, form):
        # Получаем товар по ID из URL
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        form.instance.product = product

        # Получаем промокод и безопасно обрабатываем пустой или None
        promo_raw = form.cleaned_data.get('promo_code')
        promo = promo_raw.strip().lower() if promo_raw else ''

        # Словарь допустимых промокодов
        discount_map = {'discount5': 5, 'discount10': 10, 'discount15': 15}
        discount_percent = discount_map.get(promo, 0)

        # Рассчитываем финальную цену
        final_price = product.price * (100 - discount_percent) // 100
        form.instance.final_price = final_price

        self.object = form.save()

        # Сообщение для пользователя
        if discount_percent == 0 and promo != '':
            msg = f'Промокод "{promo}" неправильный. '
        else:
            msg = ''

        return HttpResponse(
            f'{msg}Спасибо за покупку, {self.object.person}! '
            f'Цена после скидки: {self.object.final_price}'
        )