# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
#     modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field
# names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class Orderitems(models.Model):
    idorderitems = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    priceorderitems = models.IntegerField(
        db_column="priceorderitems"
    )  # Field name made lowercase.
    idorders = models.ForeignKey(
        "Orders", models.DO_NOTHING, db_column="idorders"
    )
    idproduct = models.ForeignKey(
        "Product", models.DO_NOTHING, db_column="idproduct"
    )

    class Meta:
        managed = False
        db_table = "orderitems"


class Orders(models.Model):
    idorders = models.IntegerField(primary_key=True)
    payment = models.BooleanField()
    status = models.BooleanField()
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
    nameproduct = models.CharField(max_length=45)
    priceproduct = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=200, blank=True)
    nameproducttype = models.ForeignKey(
        "Producttype",
        models.DO_NOTHING,
        db_column="nameproducttype",
        blank=True,
        null=True,
    )

    def __repr__(self):
        return f"Product {self.idproduct}: {self.nameproduct}"

    def __str__(self):
        return f"Product {self.idproduct}: {self.nameproduct}"

    class Meta:
        managed = False
        db_table = "product"


class Producttype(models.Model):
    nameproducttype = models.CharField(primary_key=True, max_length=45)
    unit = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = "producttype"


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, display_name=""):
        if not email:
            raise ValueError("Users must have an E-mail address")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, display_name=""):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Review(models.Model):
    idusers = models.ForeignKey(
        "Users", models.DO_NOTHING, db_column="idusers", primary_key=True
    )
    idproduct = models.ForeignKey(
        Product, models.DO_NOTHING, db_column="idproduct"
    )
    comment = models.CharField(max_length=8000, blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        managed = False
        db_table = "review"
        unique_together = (("idusers", "idproduct"),)


class Users(AbstractBaseUser):
    idusers = models.AutoField("idusers", primary_key=True)
    admin = models.BooleanField(default=False, null=True)
    display_name = models.CharField(
        max_length=255, default="", unique=True, null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True
    )

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.admin

    class Meta:
        db_table = "users"
