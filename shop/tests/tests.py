from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase

class ProductModelTests(TestCase):

    def setUp(self):
        self.product_1 = Product.objects.create(name="Стол", price=2000)
        self.product_2 = Product.objects.create(name="Стул", price=1000)
        self.product_3 = Product.objects.create(name="Табурет", price=500)

    def test_product_fields(self):
        # Проверяем имена
        self.assertEqual(self.product_1.name, "Стол")
        self.assertEqual(self.product_2.name, "Стул")
        # Проверяем цены
        self.assertEqual(self.product_1.price, 2000)
        self.assertEqual(self.product_2.price, 1000)
        self.assertEqual(self.product_3.price, 500)
        # Проверяем типы
        self.assertIsInstance(self.product_1.name, str)
        self.assertIsInstance(self.product_1.price, int)


class PurchaseModelTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Стол", price=2000)
        self.purchase = Purchase.objects.create(
            product=self.product,
            person="Иван",
            address="ул. Ленина, 1",
            promo_code="discount5",
            final_price=1900
        )

    def test_purchase_fields(self):
        self.assertEqual(self.purchase.person, "Иван")
        self.assertEqual(self.purchase.address, "ул. Ленина, 1")
        self.assertEqual(self.purchase.promo_code, "discount5")
        self.assertEqual(self.purchase.final_price, 1900)
        self.assertEqual(self.purchase.product, self.product)
        self.assertIsInstance(self.purchase.person, str)
        self.assertIsInstance(self.purchase.address, str)


class IndexViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product_1 = Product.objects.create(name="Стол", price=2000)
        self.product_2 = Product.objects.create(name="Стул", price=1000)

    def test_index_status_and_template(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Список", content)
        self.assertIn("Стол", content)

    def test_index_context_contains_products(self):
        url = reverse('index')
        response = self.client.get(url)
        products_in_context = response.context['products']
        self.assertIn(self.product_1, products_in_context)
        self.assertIn(self.product_2, products_in_context)

class PurchaseViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Табурет", price=500)

    def test_purchase_form_get(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('<form', content)
        self.assertIn('name="person"', content)

    def test_purchase_form_post_various_promos(self):
        test_cases = [
            ("", 500, "Спасибо за покупку"),
            ("discount5", 475, "Цена после скидки: 475"),
            ("discount10", 450, "Цена после скидки: 450"),
            ("discount15", 425, "Цена после скидки: 425"),
            ("invalid", 500, 'Промокод "invalid" неправильный'),
            ("Discount5", 475, "Цена после скидки: 475")
        ]
        for promo_code, expected_price, msg in test_cases:
            response = self.client.post(reverse('buy', kwargs={'product_id': self.product.id}), {
                'person': 'Тестовый пользователь',
                'address': 'ул. Примерная, 1',
                'promo_code': promo_code
            })
            purchase = Purchase.objects.get(person='Тестовый пользователь')
            self.assertEqual(purchase.final_price, expected_price)
            content = response.content.decode()
            self.assertIn(msg, content)
            purchase.delete()  # очищаем для следующего кейса

    def test_purchase_empty_promo(self):
        response = self.client.post(reverse('buy', kwargs={'product_id': self.product.id}), {
            'person': 'Анна',
            'address': 'ул. Пустая, 2',
            'promo_code': ''
        })
        purchase = Purchase.objects.get(person='Анна')
        self.assertEqual(purchase.final_price, self.product.price)
        content = response.content.decode()
        self.assertIn("Спасибо за покупку", content)

    def test_purchase_invalid_product(self):
        response = self.client.post(reverse('buy', kwargs={'product_id': 9999}), {
            'person': 'Тест',
            'address': 'ул. Тестовая, 1',
            'promo_code': ''
        })
        self.assertEqual(response.status_code, 404)