from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase
from shop.views import PurchaseCreate

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Стол", price=2000)

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_purchase_page_accessible(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_invalid_product(self):
        url = reverse('buy', kwargs={'product_id': 111})
        response = self.client.post(url, {
            'person': 'Иван Петров',
            'address': 'ул. Леонтьева, 1',
            'promo_code': ''
        })
        self.assertEqual(response.status_code, 404)

    def test_promo_discount5(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        self.client.post(url, {
            'person': 'Петр',
            'address': 'ул. Иванова, 71',
            'promo_code': 'discount5'
        })
        purchase = Purchase.objects.get(person="Петр")
        self.assertEqual(purchase.final_price, 1900)

    def test_promo_discount10(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        self.client.post(url, {
            'person': 'Олег Иванов',
            'address': 'ул. Ленина, 2',
            'promo_code': 'discount10'
        })
        purchase = Purchase.objects.get(person="Олег Иванов")
        self.assertEqual(purchase.final_price, 1800)

    def test_promo_discount15(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        self.client.post(url, {
            'person': 'Антон Петров',
            'address': 'ул. Петрова, 3',
            'promo_code': 'discount15'
        })
        purchase = Purchase.objects.get(person="Антон Петров")
        self.assertEqual(purchase.final_price, 1700)

    def test_invalid_promo(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        self.client.post(url, {
            'person': 'Максим Сидоренко',
            'address': 'ул. Огарёва, 4',
            'promo_code': 'qqqqqqqqqqq'
        })
        purchase = Purchase.objects.get(person="Максим Сидоренко")
        self.assertEqual(purchase.final_price, 2000)

    def test_empty_promo(self):
        url = reverse('buy', kwargs={'product_id': self.product.id})
        self.client.post(url, {
            'person': 'Анна Иванова',
            'address': 'ул. Ленина, 5',
            'promo_code': ''
        })
        purchase = Purchase.objects.get(person="Анна Иванова")
        self.assertEqual(purchase.final_price, 2000)