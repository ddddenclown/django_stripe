from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock

from shop.models import Item, Order


class ViewTests(TestCase):
	def setUp(self):
		self.item = Item.objects.create(name='X', price=500, currency='usd', description='desc')

	def test_item_detail_renders(self):
		resp = self.client.get(reverse('item_detail', args=[self.item.id]))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, self.item.name)
		self.assertContains(resp, 'Buy')

	@patch('shop.views.stripe.checkout.Session.create')
	def test_buy_item_returns_session_id(self, mock_create):
		mock_create.return_value = MagicMock(id='cs_test_123')
		resp = self.client.get(reverse('buy_item', args=[self.item.id]))
		self.assertEqual(resp.status_code, 200)
		self.assertJSONEqual(resp.content, {"id": "cs_test_123"})
		# ensure called with expected line_items
		args, kwargs = mock_create.call_args
		self.assertIn('line_items', kwargs)
		self.assertEqual(kwargs['line_items'][0]['price_data']['unit_amount'], 500)

	@patch('shop.views.stripe.Coupon.create')
	@patch('shop.views.stripe.checkout.Session.create')
	def test_buy_order_with_discount(self, mock_session_create, mock_coupon_create):
		mock_coupon_create.return_value = MagicMock(id='coupon_123')
		mock_session_create.return_value = MagicMock(id='cs_test_order')

		order = Order.objects.create(currency='usd', discount_percent=15)
		order.items.add(self.item)

		resp = self.client.get(reverse('buy_order', args=[order.id]))
		self.assertEqual(resp.status_code, 200)
		self.assertJSONEqual(resp.content, {"id": "cs_test_order"})
		# coupon created
		mock_coupon_create.assert_called_once()
		# discounts passed to session
		_, kwargs = mock_session_create.call_args
		self.assertIn('discounts', kwargs)
		self.assertEqual(kwargs['discounts'][0]['coupon'], 'coupon_123')
