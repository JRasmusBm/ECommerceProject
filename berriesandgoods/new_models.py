# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Orderitems(models.Model):
    idorderitems = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    priceorderitems = models.IntegerField(db_column='priceOrderItems')  # Field name made lowercase.
    idorders = models.ForeignKey('Orders', models.DO_NOTHING, db_column='idorders')
    idproduct = models.ForeignKey('Product', models.DO_NOTHING, db_column='idproduct')

    class Meta:
        managed = False
        db_table = 'orderitems'


class Orders(models.Model):
    idorders = models.IntegerField(primary_key=True)
    payment = models.BooleanField()
    status = models.BooleanField()
    price = models.IntegerField(blank=True, null=True)
    idusers = models.ForeignKey('Users', models.DO_NOTHING, db_column='idusers', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Product(models.Model):
    idproduct = models.IntegerField(primary_key=True)
    nameproduct = models.CharField(max_length=45)
    priceproduct = models.FloatField()
    img = models.CharField(max_length=200, blank=True, null=True)
    nameproducttype = models.ForeignKey('Producttype', models.DO_NOTHING, db_column='nameproducttype', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Producttype(models.Model):
    nameproducttype = models.CharField(primary_key=True, max_length=45)
    unit = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'producttype'


class Users(models.Model):
    idusers = models.IntegerField(primary_key=True)
    admin = models.BooleanField()
    email = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
