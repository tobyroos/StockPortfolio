# Generated by Django 2.2 on 2022-04-25 01:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_buymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmodel',
            name='date_bought_field',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
