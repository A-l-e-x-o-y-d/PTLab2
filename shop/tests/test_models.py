from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Стул", price="1000")
        Product.objects.create(name="Кровать", price="400")

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="Стул").name, str)
        self.assertIsInstance(Product.objects.get(name="Стул").price, int)
        self.assertIsInstance(Product.objects.get(name="Кровать").name, str)
        self.assertIsInstance(Product.objects.get(name="Кровать").price, int)        

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="Стул").price == 1000)
        self.assertTrue(Product.objects.get(name="Кровать").price == 400)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="Шкаф", price="5000")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book,
                                person="Александр Ткачёв",
                                address="ул. Ленина 22",
                                promo_code="discount5",
                                final_price=4750)

    def test_correctness_types(self):
        purchase = Purchase.objects.get(product=self.product_book)
        self.assertIsInstance(purchase.person, str)
        self.assertIsInstance(purchase.address, str)
        self.assertIsInstance(purchase.date, datetime)
        self.assertIsInstance(purchase.promo_code, str)
        self.assertIsInstance(purchase.final_price, int)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Александр Ткачёв")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "ул. Ленина 22")
        self.assertTrue(Purchase.objects.get(product=self.product_book).promo_code == "discount5")
        self.assertTrue(Purchase.objects.get(product=self.product_book).final_price == 4750)
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == self.datetime.replace(microsecond=0))