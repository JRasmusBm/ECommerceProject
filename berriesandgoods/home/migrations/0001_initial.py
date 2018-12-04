# Generated by Django 2.1.3 on 2018-11-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orderitems',
            fields=[
                ('idorderitems', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('priceorderitems', models.IntegerField(db_column='priceOrderItems')),
            ],
            options={
                'db_table': 'orderitems',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('idorders', models.IntegerField(primary_key=True, serialize=False)),
                ('payment', models.BooleanField()),
                ('status', models.BooleanField()),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('idproduct', models.IntegerField(primary_key=True, serialize=False)),
                ('nameproduct', models.CharField(max_length=45)),
                ('priceproduct', models.IntegerField(blank=True, null=True)),
                ('img', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Producttype',
            fields=[
                ('nameproducttype', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('unit', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'producttype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('idusers', models.AutoField(primary_key=True, serialize=False, verbose_name='idusers')),
                ('admin', models.BooleanField(default=True, null=True)),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
