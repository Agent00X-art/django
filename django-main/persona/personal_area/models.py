import datetime
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class PersonalData(AbstractBaseUser, PermissionsMixin): # модель для персональных данных

    Surname = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    Phone = models.CharField(max_length=15)
    PhoneValidate = models.BooleanField(default=False)
    EmailValidate = models.BooleanField(default=False)
    PhoneCode = models.CharField(default='', max_length=4)
    EmailCode = models.CharField(default='', max_length=4)
    email = models.EmailField(_('email address'), unique=True, default='')
    password = models.CharField(max_length=100, default='')
    Avatar = models.ImageField(default=None, upload_to='accounts/')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.Phone

class Message(models.Model):
    IdChat = models.CharField(max_length=40, default='')
    FirstPhone = models.CharField(max_length=20)
    SecondPhone = models.CharField(max_length=20)
    Chat = models.CharField(max_length=700000, default='')
    def __str__(self):
        return self.IdChat

class CreateLoyaltyCard(models.Model):

    IdCard = models.CharField(default='0000000000000001', max_length=16)
    Phone = models.CharField(max_length=15)
    PIN = models.CharField(max_length=4)

    def __str__(self):
        return self.IdCard

class CreateGiftCard(models.Model):

    IdCard = models.CharField(default='0000000000000001', max_length=16)
    Phone = models.CharField(max_length=15)
    PIN = models.CharField(max_length=4)
    email = models.EmailField(default='', max_length=150)

    def __str__(self):
        return self.IdCard