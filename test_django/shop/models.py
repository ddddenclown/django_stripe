from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('rub', 'RUB'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField(help_text='Price in minor units (cents/kopeks)')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self) -> str:
        return self.name

    @property
    def price_major(self) -> str:
        return f"{self.price / 100:.2f}"


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders', blank=True)
    total_price = models.IntegerField(default=0, help_text='Total in minor units')
    currency = models.CharField(max_length=3, choices=Item.CURRENCY_CHOICES, default='usd')

    # Optional simple discount/tax fields for demo
    discount_percent = models.PositiveIntegerField(default=0)
    tax_percent = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Order #{self.pk}"

    def calculate_totals(self) -> int:
        subtotal = sum(item.price for item in self.items.all())
        if self.discount_percent:
            subtotal = subtotal - (subtotal * self.discount_percent // 100)
        if self.tax_percent:
            subtotal = subtotal + (subtotal * self.tax_percent // 100)
        self.total_price = subtotal
        return subtotal
