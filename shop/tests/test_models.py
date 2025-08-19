from django.test import TestCase
from shop.models import Item, Order


class ItemModelTests(TestCase):
	def test_price_major_format(self):
		item = Item.objects.create(name='Test', price=1234, currency='usd')
		self.assertEqual(item.price_major, '12.34')


class OrderModelTests(TestCase):
	def setUp(self):
		self.item1 = Item.objects.create(name='A', price=1000, currency='usd')
		self.item2 = Item.objects.create(name='B', price=250, currency='usd')

	def test_calculate_totals_no_discounts(self):
		order = Order.objects.create(currency='usd')
		order.items.add(self.item1, self.item2)
		total = order.calculate_totals()
		self.assertEqual(total, 1250)
		self.assertEqual(order.total_price, 1250)

	def test_calculate_totals_with_discount_and_tax(self):
		order = Order.objects.create(currency='usd', discount_percent=10, tax_percent=20)
		order.items.add(self.item1)
		total = order.calculate_totals()
		# 1000 -> minus 10% = 900 -> plus 20% = 1080
		self.assertEqual(total, 1080)
		self.assertEqual(order.total_price, 1080)
