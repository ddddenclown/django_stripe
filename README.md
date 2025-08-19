# Django + Stripe Checkout (Shop)

Простой сервер на Django с оплатой товаров через Stripe Checkout. Есть админка, страница товара с кнопкой Buy и оплата заказа из нескольких товаров.

## Стек
- Python >= 3.10, Django 4.2
- Stripe Python SDK
- sqlite3 по умолчанию

## Быстрый старт (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Создайте файл `.env` в корне (рядом с `manage.py`):
```env
DEBUG=True
SECRET_KEY=django-insecure-change-me
ALLOWED_HOSTS=*
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

Миграции и суперпользователь:
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Запуск сервера:
```powershell
python manage.py runserver 0.0.0.0:8000
```

Откройте:
- Главная: `http://localhost:8000/` — список товаров (пока пусто)
- Админка: `http://localhost:8000/admin/` — создайте `Item` и при желании `Order`

## Модели
- Item
  - `name: CharField`
  - `description: TextField`
  - `price: IntegerField` (в минорных единицах — центы/копейки)
  - `currency: CharField` (`usd|eur|rub`)
- Order (бонус)
  - `items: ManyToManyField(Item)`
  - `total_price: IntegerField` (кеш итоговой суммы)
  - `currency: CharField`
  - `discount_percent: PositiveIntegerField` (упрощённо)
  - `tax_percent: PositiveIntegerField` (демо; см. примечание ниже)

Примечание: `tax_percent` не применяется напрямую. Для реальных налогов используйте Stripe Automatic Tax или заранее созданные `TaxRate`.

## Эндпоинты
- GET `/` — список товаров
- GET `/item/{id}/` — HTML-страница товара с кнопкой Buy
  - JS: `fetch(/buy/{id}/)` → `stripe.redirectToCheckout({ sessionId })`
- GET `/buy/{id}/` — создаёт Stripe Checkout Session на 1 товар, возвращает `{ "id": "<session.id>" }`
- GET `/order/{id}/buy/` — оплачивает заказ из нескольких товаров; если задан `discount_percent`, создаётся одноразовый купон и применяется к сессии
- GET `/success` / `/cancel` — результат оплаты

## Stripe
- Используйте тестовые ключи из Dashboard: `pk_test_...` / `sk_test_...`
- В режиме разработки домен может быть `http://localhost:8000`
- При необходимости можно добавить `automatic_tax` в параметры сессии Stripe Checkout

## Переменные окружения
- `DEBUG` — по умолчанию True
- `SECRET_KEY` — задайте свой
- `ALLOWED_HOSTS` — например `*` или домен/хост развертывания
- `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY` — тестовые/боевые ключи

## Тесты
- Запуск всех тестов:
  ```powershell
  python manage.py test -v 2
  ```
- Юнит‑тесты: модели (`shop/tests/test_models.py`) и вьюхи с моками Stripe (`shop/tests/test_views.py`).
- Интеграционные тесты Stripe (`shop/tests/test_stripe_integration.py`):
  - Запускаются только если в окружении задан `STRIPE_SECRET_KEY` со значением, начинающимся на `sk_test_`. Иначе помечаются как skipped.
  - Пример запуска:
    ```powershell
    $env:STRIPE_SECRET_KEY="sk_test_..."
    $env:STRIPE_PUBLIC_KEY="pk_test_..."
    python manage.py test shop.tests.test_stripe_integration -v 2
    ```
  - Тесты создают настоящие Checkout Session в тестовом режиме и проверяют корректный `session.id`.

## Docker (опционально)
Опционально могут быть добавлены `Dockerfile` и `docker-compose.yml` с конфигурацией через переменные окружения.

## Деплой
- Подходит любой PaaS (Railway, Render, Fly.io, Dokku, Heroku-like) или VPS
- Потребуются переменные окружения из `.env`, миграции и статические файлы (WhiteNoise уже включён)

## Проверка
- После запуска сервер доступен на `http://0.0.0.0:8000/`
- Для оплаты создайте хотя бы один `Item` и используйте страницу `/item/{id}/`

## Лицензия
MIT