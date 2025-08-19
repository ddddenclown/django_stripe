from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Discount",
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
                ("percent", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Tax",
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
                ("percent", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="discounts",
            field=models.ManyToManyField(
                blank=True, related_name="orders", to="shop.discount"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="taxes",
            field=models.ManyToManyField(
                blank=True, related_name="orders", to="shop.tax"
            ),
        ),
    ]
