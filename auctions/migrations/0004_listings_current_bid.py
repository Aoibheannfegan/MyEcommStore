# Generated by Django 4.2.3 on 2023-07-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listings_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='current_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]