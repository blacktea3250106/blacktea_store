# Generated by Django 4.2.4 on 2023-08-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_cart_formatted_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]