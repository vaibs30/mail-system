# Generated by Django 3.0.8 on 2020-07-06 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20200706_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='cprice',
            field=models.IntegerField(null=True),
        ),
    ]
