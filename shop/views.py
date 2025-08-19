from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
import stripe

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_GET
def item_detail(request, id: int):
	item = get_object_or_404(Item, pk=id)
	context = {
		'item': item,
		'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
	}
	return render(request, 'shop/item_detail.html', context)


@require_GET
def buy_item(request, id: int):
	item = get_object_or_404(Item, pk=id)

	try:
		session = stripe.checkout.Session.create(
			mode='payment',
			payment_method_types=['card'],
			line_items=[
				{
					'price_data': {
						'currency': item.currency,
						'product_data': {
							'name': item.name,
							'description': item.description,
						},
						'unit_amount': item.price,
					},
					'quantity': 1,
				}
			],
			success_url=request.build_absolute_uri('/success'),
			cancel_url=request.build_absolute_uri('/cancel'),
		)
		return JsonResponse({'id': session.id})
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=400)


@require_GET
def buy_order(request, id: int):
	order = get_object_or_404(Order, pk=id)
	order.calculate_totals()

	line_items = []
	for item in order.items.all():
		line_items.append(
			{
				'price_data': {
					'currency': order.currency or item.currency,
					'product_data': {
						'name': item.name,
						'description': item.description,
					},
					'unit_amount': item.price,
				},
				'quantity': 1,
			}
		)

	try:
		create_kwargs = {
			"mode": 'payment',
			"payment_method_types": ['card'],
			"line_items": line_items,
			"success_url": request.build_absolute_uri('/success'),
			"cancel_url": request.build_absolute_uri('/cancel'),
		}
		if order.discount_percent:
			coupon = stripe.Coupon.create(percent_off=order.discount_percent, duration='once')
			create_kwargs["discounts"] = [{"coupon": coupon.id}]
		session = stripe.checkout.Session.create(**create_kwargs)
		return JsonResponse({'id': session.id})
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=400)


@require_GET
def success(request):
	return render(request, 'shop/success.html')


@require_GET
def cancel(request):
	return render(request, 'shop/cancel.html')
