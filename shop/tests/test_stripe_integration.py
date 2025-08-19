import os
import re
from unittest import skipUnless
from django.test import TestCase
from django.urls import reverse
import stripe

from shop.models import Item, Order


HAS_STRIPE_TEST_KEY = os.getenv('STRIPE_SECRET_KEY', '').startswith('sk_test_')


@skipUnless(HAS_STRIPE_TEST_KEY, 'No STRIPE_SECRET_KEY provided; skipping Stripe integration tests')
class StripeIntegrationTests(TestCase):
	def setUp(self):
		stripe.api_key = os.environ['STRIPE_SECRET_KEY']
		self.item = Item.objects.create(name='RealX', price=700, currency='usd', description='integration')

	def test_real_checkout_session_for_single_item(self):
		resp = self.client.get(reverse('buy_item', args=[self.item.id]))
		self.assertEqual(resp.status_code, 200)
		session_id = resp.json().get('id')
		self.assertIsNotNone(session_id)
		self.assertTrue(re.match(r'^cs_(test_|live_)?[A-Za-z0-9]+$', session_id))

	def test_real_checkout_session_for_order_with_discount(self):
		order = Order.objects.create(currency='usd', discount_percent=5)
		order.items.add(self.item)
		resp = self.client.get(reverse('buy_order', args=[order.id]))
		self.assertEqual(resp.status_code, 200)
		session_id = resp.json().get('id')
		self.assertIsNotNone(session_id)
		self.assertTrue(re.match(r'^cs_(test_|live_)?[A-Za-z0-9]+$', session_id))
