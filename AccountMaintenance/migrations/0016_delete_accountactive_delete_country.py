# Generated by Django 4.1.7 on 2023-04-08 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountMaintenance', '0015_accountactive'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AccountActive',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
