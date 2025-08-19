## Django + Stripe Checkout (Shop)

Небольшой сервер на Django с оплатой через Stripe Checkout. Включает админку, страницу товара с кнопкой Buy и оплату заказа из нескольких товаров.

### Основные возможности
- Модель товара `Item` (name, description, price в минорных единицах, currency)
- Страницы: список товаров, карточка товара, success/cancel
- Оплата одного товара: создание Stripe Checkout Session и редирект через Stripe.js
- Оплата заказа из нескольких товаров (Order) с применением скидки через купон
- Админка Django для управления моделями

### Требования
- Python >= 3.10
- Django 4.2
- Тестовые ключи Stripe (pk_test_... / sk_test_...)

## Установка и запуск (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Создать файл `.env` рядом с `manage.py`:
```env
DEBUG=True
SECRET_KEY=django-insecure-change-me
ALLOWED_HOSTS=*
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

Инициализация базы данных и суперпользователь:
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Запуск сервера разработки:
```powershell
python manage.py runserver 0.0.0.0:8000
```

Доступ:
- Главная: `http://localhost:8000/`
- Админка: `http://localhost:8000/admin/`

## Запуск через Docker
```bash
docker compose up --build
```
- Откроется `http://localhost:8000`
- Переменные окружения берутся из `.env`

## Эндпоинты
- `GET /` — список товаров
- `GET /item/{id}/` — страница товара с кнопкой Buy
  - JS: запрос на `/buy/{id}/`, далее `stripe.redirectToCheckout({ sessionId })`
- `GET /buy/{id}/` — создание Stripe Checkout Session для одного товара, ответ: `{ "id": "<session.id>" }`
- `GET /order/{id}/buy/` — создание Checkout Session для заказа из нескольких товаров; при наличии `discount_percent` создаётся одноразовый купон и применяется к сессии
- `GET /success` / `GET /cancel` — результат оплаты

## Модели
- `Item`
  - `name: CharField`
  - `description: TextField`
  - `price: IntegerField` (минорные единицы — центы/копейки)
  - `currency: CharField` (`usd|eur|rub`)
- `Order`
  - `items: ManyToManyField(Item)`
  - `total_price: IntegerField` (кеш итоговой суммы в минорных единицах)
  - `currency: CharField`
  - `discount_percent: PositiveIntegerField`
  - `tax_percent: PositiveIntegerField` (демо‑поле)

Примечание: налоги через `tax_percent` напрямую не применяются при создании сессии. Для реальных налогов рекомендуется использовать Stripe Automatic Tax или `TaxRate`.

## Тесты
Запуск всех тестов:
```powershell
python manage.py test -v 2
```
- Юнит‑тесты: модели и вьюхи с моками Stripe — `shop/tests/test_models.py`, `shop/tests/test_views.py`
- Интеграционные тесты Stripe — `shop/tests/test_stripe_integration.py`
  - Запускаются только при наличии `STRIPE_SECRET_KEY` с префиксом `sk_test_`
  - Пример запуска:
    ```powershell
    $env:STRIPE_SECRET_KEY="sk_test_..."
    $env:STRIPE_PUBLIC_KEY="pk_test_..."
    python manage.py test shop.tests.test_stripe_integration -v 2
    ```

## Конфигурация
- `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY` читаются из `.env`
- Статические файлы: `STATIC_URL='static/'`, `STATIC_ROOT=staticfiles/` (WhiteNoise подключён)

## Деплой
- Требуется задать переменные окружения из `.env`
- Выполнить миграции и сбор статических файлов (`collectstatic`)
- Пример продакшн‑команды см. в `Dockerfile`/`docker-compose.yml` (gunicorn)