# Generated by Django 5.0.4 on 2024-07-06 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_image_options_post_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='inventory',
            field=models.PositiveIntegerField(default=0, verbose_name='موجودی'),
        ),
        migrations.AddField(
            model_name='post',
            name='off',
            field=models.PositiveIntegerField(default=0, verbose_name='تخفیف'),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
