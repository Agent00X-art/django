import datetime
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()
    Photo = models.ImageField(default=None, upload_to='categories_image/')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title

class Product(models.Model):

    Article = models.CharField(max_length=200, default='')
    Brand = models.CharField(max_length=200, default='')
    Color = models.CharField(max_length=50, default='')
    Compound = models.CharField(max_length=1000, default='')
    Country = models.CharField(max_length=100, default='')
    Tags = models.CharField(max_length=1000)
    HeaderAd = models.CharField(max_length=150)
    Description = models.CharField(max_length=9000)
    Information = models.CharField(max_length=9000)
    Return = models.CharField(max_length=9000)
    Delivery = models.CharField(max_length=9000)
    Price = models.IntegerField(default=None)
    New_Price = models.IntegerField(default=None)
    Sizes = models.CharField(max_length=10)
    Top = models.BooleanField(default=False)
    Photo_1 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_2 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_3 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_4 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_5 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_6 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_7 = models.ImageField(default=None, upload_to='Product_images/')
    Photo_8 = models.ImageField(default=None, upload_to='Product_images/')
    logocompany = models.ImageField(default=None, upload_to='Product_images/')

    def __str__(self):
        return self.Article
