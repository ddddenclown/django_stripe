from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "price",
                    models.IntegerField(
                        help_text="Price in minor units (cents/kopeks)"
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[("usd", "USD"), ("eur", "EUR"), ("rub", "RUB")],
                        default="usd",
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_price",
                    models.IntegerField(default=0, help_text="Total in minor units"),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[("usd", "USD"), ("eur", "EUR"), ("rub", "RUB")],
                        default="usd",
                        max_length=3,
                    ),
                ),
                ("discount_percent", models.PositiveIntegerField(default=0)),
                ("tax_percent", models.PositiveIntegerField(default=0)),
                (
                    "items",
                    models.ManyToManyField(
                        blank=True, related_name="orders", to="shop.item"
                    ),
                ),
            ],
        ),
    ]
