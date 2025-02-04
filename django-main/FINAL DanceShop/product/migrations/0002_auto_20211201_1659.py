# Generated by Django 3.2.9 on 2021-12-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Highlight',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='Top',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='Video',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='Vip',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='Height',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='MaleFemale',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.IntegerField(),
        ),
    ]
