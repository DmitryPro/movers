# Generated by Django 5.2.1 on 2025-05-28 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_offer_status2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='status2',
        ),
    ]
