# ABOUT

Подробное описание реализованного сервиса Django + Stripe Checkout.

## Общее
- Назначение: демонстрационный магазин с оплатой через Stripe Checkout.
- Компоненты: Django-приложение `shop`, Stripe SDK, минимальные HTML-шаблоны, админка.
- Хранилище: SQLite (по умолчанию).

## Структура проекта
```
manage.py
requirements.txt
README.md
ABOUT.md
config/
  __init__.py
  settings.py
  urls.py
  wsgi.py
  asgi.py
shop/
  __init__.py
  apps.py
  admin.py
  models.py
  urls.py
  views.py
  views_index.py
  tests/
    __init__.py
    test_models.py
    test_views.py
    test_stripe_integration.py
templates/
  shop/
    index.html
    item_detail.html
    success.html
    cancel.html
static/
  .gitkeep
```

## Данные (модели/таблицы)
- Item
  - `id: BigAutoField` (PK)
  - `name: CharField`
  - `description: TextField`
  - `price: IntegerField` — цена в минорных единицах (центах/копейках)
  - `currency: CharField` — одно из: `usd|eur|rub`
  - Свойство `price_major` — строка с ценой в основных единицах, формат `X.XX`
- Order (бонус)
  - `id: BigAutoField` (PK)
  - `items: ManyToManyField(Item)`
  - `total_price: IntegerField` — итог в минорных единицах (кеш)
  - `currency: CharField` — `usd|eur|rub`
  - `discount_percent: PositiveIntegerField` — упрощённая скидка, %
  - `tax_percent: PositiveIntegerField` — демо-поле; не применяется напрямую при создании сессии (см. Stripe Automatic Tax)
  - Метод `calculate_totals()` — перерасчёт суммы с учётом скидки и налога

Миграции: `shop/migrations/0001_initial.py` (генерируются автоматически при `makemigrations`).

## Роуты (URLs)
- Пользовательские страницы:
  - `GET /` — индекс, список товаров
  - `GET /item/<id>/` — страница товара с кнопкой “Buy” (Stripe Checkout через JS)
  - `GET /success` — страница успешной оплаты
  - `GET /cancel` — страница отмены оплаты
- API/действия оплаты:
  - `GET /buy/<id>/` — создаёт Stripe Checkout Session для одного товара, ответ: `{ "id": "<session.id>" }`
  - `GET /order/<id>/buy/` — создаёт Stripe Checkout Session для заказа из нескольких товаров; при наличии `discount_percent` создаётся одноразовый купон и применяется к сессии
- Админка:
  - `GET /admin/` — CRUD для `Item` и `Order`

Примечания по Stripe:
- В `buy_item` и `buy_order` используется Stripe Checkout (Session API) в режиме `payment`.
- Для Order с `discount_percent > 0` создаётся купон `stripe.Coupon.create(percent_off=..., duration='once')` и передаётся в `discounts` при создании сессии.
- Поле `tax_percent` как демо не передаётся напрямую. Для реального применения налогов используйте Stripe Automatic Tax (включается в Dashboard) или `TaxRate`.

## CRUD
- Через Django Admin (`/admin/`):
  - `Item`: создать/просмотреть/изменить/удалить, поиск по `name`.
  - `Order`: создать/просмотреть/изменить/удалить, выбор товаров через M2M.
- Прямых REST-эндпоинтов CRUD не реализовано. При необходимости легко добавить DRF или классические Django CBV для JSON API.

## Шаблоны (UI)
- `templates/shop/index.html` — простой список товаров с ссылками на карточки
- `templates/shop/item_detail.html` — карточка товара с кнопкой “Buy” и подключением Stripe.js
- `templates/shop/success.html`, `templates/shop/cancel.html` — страницы результата

## Настройки/конфигурация
- Переменные окружения (через `django-environ`, читаются из `.env`):
  - `DEBUG` (bool), по умолчанию True
  - `SECRET_KEY`
  - `ALLOWED_HOSTS` (список)
  - `STRIPE_PUBLIC_KEY` (pk_test_...)
  - `STRIPE_SECRET_KEY` (sk_test_...)
- Статика:
  - `STATIC_URL = 'static/'`
  - `STATIC_ROOT = <project>/staticfiles` (для деплоя; WhiteNoise подключён)
  - Локально используется папка `static/` (создана), чтобы избежать предупреждений

## Тесты
- Запуск всех тестов: `python manage.py test -v 2`
- Файлы:
  - `shop/tests/test_models.py` — модельные тесты `Item.price_major`, `Order.calculate_totals()`
  - `shop/tests/test_views.py` — тесты вьюх: рендер карточки, создание Session для товара/заказа (Stripe вызовы замоканы)
  - `shop/tests/test_stripe_integration.py` — интеграционные тесты Stripe, создают настоящие Checkout Session в тестовом режиме
    - Запускаются только если `STRIPE_SECRET_KEY` из окружения начинается с `sk_test_` (иначе `skip`)
    - Пример запуска в PowerShell:
      ```powershell
      $env:STRIPE_SECRET_KEY="sk_test_..."
      $env:STRIPE_PUBLIC_KEY="pk_test_..."
      python manage.py test shop.tests.test_stripe_integration -v 2
      ```

## Как запустить локально (кратко)
1) Виртуальное окружение и зависимости:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```
2) `.env`:
```env
DEBUG=True
SECRET_KEY=django-insecure-change-me
ALLOWED_HOSTS=*
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```
3) БД и суперпользователь:
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
4) Сервер:
```powershell
python manage.py runserver 0.0.0.0:8000
```

## Деплой
- Подходит любой PaaS/VPS. Требуется выставить переменные окружения из `.env`.
- `STATIC_ROOT` и WhiteNoise позволяют обслуживать статику без внешнего CDN на небольших проектах.
- Для продакшна используйте `DEBUG=False`, задайте надёжный `SECRET_KEY`, настройте `ALLOWED_HOSTS`.

## Ограничения и дальнейшие улучшения
- Налоги упрощены. Для реального сценария — Stripe Automatic Tax или `TaxRate`.
- Нет REST CRUD API — можно добавить DRF для публичных JSON-эндпоинтов.
- Нет Docker/compose — можно добавить по запросу.
- Валидация валюты/цен/ограничений — базовая; при необходимости расширить.
