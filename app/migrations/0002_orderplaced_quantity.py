# Generated by Django 4.2.7 on 2023-12-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantity:'),
        ),
    ]
