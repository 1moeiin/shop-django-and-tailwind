# Generated by Django 5.0.6 on 2024-07-19 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_productfeature_remove_post_weight_alter_post_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='feature',
        ),
        migrations.DeleteModel(
            name='ProductFeature',
        ),
    ]
