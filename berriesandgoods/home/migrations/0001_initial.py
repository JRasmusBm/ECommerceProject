# Generated by Django 2.1.3 on 2018-12-07 13:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Orderitems",
            fields=[
                (
                    "idorderitems",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("amount", models.IntegerField()),
                (
                    "priceorderitems",
                    models.IntegerField(db_column="priceorderitems"),
                ),
            ],
            options={"db_table": "orderitems", "managed": False},
        ),
        migrations.CreateModel(
            name="Orders",
            fields=[
                (
                    "idorders",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("payment", models.BooleanField()),
                ("status", models.BooleanField()),
                ("price", models.IntegerField(blank=True, null=True)),
            ],
            options={"db_table": "orders", "managed": False},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "idproduct",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("nameproduct", models.CharField(max_length=45)),
                (
                    "priceproduct",
                    models.IntegerField(blank=True, null=True),
                ),
                ("availability", models.IntegerField()),
                ("img", models.CharField(blank=True, max_length=200)),
            ],
            options={"db_table": "product", "managed": False},
        ),
        migrations.CreateModel(
            name="Producttype",
            fields=[
                (
                    "nameproducttype",
                    models.CharField(
                        max_length=45, primary_key=True, serialize=False
                    ),
                ),
                ("unit", models.CharField(max_length=45)),
            ],
            options={"db_table": "producttype", "managed": False},
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "password",
                    models.CharField(
                        max_length=128, verbose_name="password"
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "idusers",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="idusers",
                    ),
                ),
                ("admin", models.BooleanField(default=False, null=True)),
                (
                    "display_name",
                    models.CharField(
                        default="", max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
            ],
            options={"db_table": "users"},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "idusers",
                    models.ForeignKey(
                        db_column="idusers",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True, max_length=8000, null=True
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
            ],
            options={"db_table": "review", "managed": False},
        ),
    ]
