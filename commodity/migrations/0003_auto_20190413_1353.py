# Generated by Django 2.1.4 on 2019-04-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0002_commodity_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]