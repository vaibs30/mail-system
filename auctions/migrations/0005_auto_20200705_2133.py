# Generated by Django 3.0.8 on 2020-07-05 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200705_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watchlist_items',
        ),
        migrations.CreateModel(
            name='watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='auctions.listing')),
            ],
        ),
    ]