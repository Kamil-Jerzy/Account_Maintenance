# Generated by Django 4.1.7 on 2023-04-08 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountMaintenance', '0012_delete_maintenance'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
