# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Berry(models.Model):
    idberry = models.IntegerField(primary_key=True)
    nameberry = models.CharField(max_length=45, blank=True, null=True)
    idberrytype = models.ForeignKey(
        "Berrytype",
        models.DO_NOTHING,
        db_column="idberrytype",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "berry"


class Berrytype(models.Model):
    idberrytype = models.IntegerField(primary_key=True)
    nameberrytype = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "berrytype"


class Goods(models.Model):
    idgoods = models.IntegerField(primary_key=True)
    namegoods = models.CharField(max_length=45, blank=True, null=True)
    idgoodstype = models.ForeignKey(
        "Goodstype",
        models.DO_NOTHING,
        db_column="idgoodstype",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "goods"


class Goodstype(models.Model):
    idgoodstype = models.IntegerField(primary_key=True)
    namegoodstype = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "goodstype"


class Orders(models.Model):
    idorders = models.IntegerField(primary_key=True)
    payment = models.BooleanField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    idusers = models.ForeignKey(
        "Users",
        models.DO_NOTHING,
        db_column="idusers",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "orders"


class Product(models.Model):
    idproduct = models.IntegerField(primary_key=True)
    amount = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    idorders = models.ForeignKey(
        Orders,
        models.DO_NOTHING,
        db_column="idorders",
        blank=True,
        null=True,
    )
    idproducttype = models.ForeignKey(
        "Producttype",
        models.DO_NOTHING,
        db_column="idproducttype",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "product"


class Producttype(models.Model):
    idproducttype = models.IntegerField(primary_key=True)
    idberry = models.ForeignKey(
        Berry, models.DO_NOTHING, db_column="idberry", blank=True, null=True
    )
    idgoods = models.ForeignKey(
        Goods, models.DO_NOTHING, db_column="idgoods", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "producttype"


class Users(models.Model):
    idusers = models.IntegerField(primary_key=True)
    admin = models.BooleanField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"
