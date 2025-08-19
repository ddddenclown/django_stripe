from django.urls import path
from . import views
from .views_index import index

urlpatterns = [
	path('', index, name='index'),
	path('item/<int:id>/', views.item_detail, name='item_detail'),
	path('buy/<int:id>/', views.buy_item, name='buy_item'),
	path('order/<int:id>/buy/', views.buy_order, name='buy_order'),
	path('success', views.success, name='success'),
	path('cancel', views.cancel, name='cancel'),
]
