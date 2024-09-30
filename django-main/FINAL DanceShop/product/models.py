import datetime
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

class Product(models.Model): # модель для одного товара

    IdProduct = models.CharField(max_length=20, default='')
    State = models.CharField(max_length=20)
    AdType = models.CharField(max_length=20)
    Price = models.IntegerField()
    Style = models.CharField(max_length=15)
    Clothing = models.BooleanField(default=False)
    Shoes = models.BooleanField(default=False)
    Size = models.CharField(max_length=20)
    MaleFemale = models.CharField(max_length=20)
    Height = models.IntegerField()
    Color = models.CharField(max_length=100, default='')
    Location = models.CharField(max_length=100, default='')
    Photo_1 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_2 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_3 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_4 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_5 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_6 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_7 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_8 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_9 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_10 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_11 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_12 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_13 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_14 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_15 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_16 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_17 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_18 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_19 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_20 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_21 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_22 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_23 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_24 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_25 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_26 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_27 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_28 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_29 = models.ImageField(default=None, upload_to='apartaments_image/')
    Photo_30 = models.ImageField(default=None, upload_to='apartaments_image/')
    Video = models.CharField(default='', max_length=1000)
    Phone = models.IntegerField()
    Top = models.BooleanField(default=False)
    Highlight = models.BooleanField(default=False)
    Vip = models.BooleanField(default=False)

    def __str__(self):
        return self.IdProduct

# Create your models here.
class condition(models.Model):

    value = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.value

class Type4Heavy(models.Model):

    value = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.value

class price(models.Model):

    value = models.FloatField(default=0)
    def __str__(self):
        return self.value

class style(models.Model):

    value = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.value

class typeof(models.Model):

    value = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.value

class size(models.Model):

    value = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.value

class color(models.Model):

    value = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.value
