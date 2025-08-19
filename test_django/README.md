# Django + Stripe Checkout Shop

Простой магазин на Django с оплатой через Stripe Checkout.

## Требования
- Python >= 3.10
- Django 4.x

## Установка
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Создайте файл `.env` в корне `test_django/` по примеру:
```env
DEBUG=True
SECRET_KEY=django-insecure-change-me
ALLOWED_HOSTS=*
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## Миграции и суперпользователь
```bash
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
```

## Запуск
```bash
python manage.py runserver 0.0.0.0:8000
```

Откройте `http://localhost:8000/` — список товаров. Админка: `http://localhost:8000/admin/`.

## Модели
- Item: name, description, price (в минорных единицах), currency
- Order: items M2M, total_price, currency, discount_percent, tax_percent

## Эндпоинты
- GET `/` — список товаров
- GET `/item/{id}/` — страница товара с кнопкой Buy
- GET `/buy/{id}/` — создаёт Stripe Session и возвращает `{ id: sessionId }`
- GET `/order/{id}/buy/` — оплата заказа из нескольких товаров
- GET `/success` / `/cancel`

## Docker (опционально)
Будет добавлен при необходимости.
