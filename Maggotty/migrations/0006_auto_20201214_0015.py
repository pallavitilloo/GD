# Generated by Django 3.1.3 on 2020-12-14 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maggotty', '0005_order_eventname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='eventName',
            field=models.CharField(max_length=255),
        ),
    ]
