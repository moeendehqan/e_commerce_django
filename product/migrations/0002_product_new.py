# Generated by Django 5.1.6 on 2025-03-05 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='new',
            field=models.BooleanField(default=True, verbose_name='جدید'),
        ),
    ]
