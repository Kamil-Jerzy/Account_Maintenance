# Generated by Django 4.1.7 on 2023-04-02 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountMaintenance', '0004_excelfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_date', models.DateField()),
                ('country_code', models.CharField(max_length=2)),
                ('account_number', models.IntegerField()),
                ('account_name', models.CharField(max_length=32)),
                ('currency', models.CharField(max_length=3)),
                ('maintenance_type', models.CharField(max_length=1)),
                ('requestor', models.CharField(max_length=64)),
                ('approver', models.CharField(max_length=64)),
                ('additional_info', models.CharField(max_length=64)),
                ('created_by', models.CharField(max_length=64)),
            ],
        ),
    ]
