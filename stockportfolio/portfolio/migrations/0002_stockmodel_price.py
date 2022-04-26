# Generated by Django 2.2 on 2022-04-24 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmodel',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50),
        ),
    ]
