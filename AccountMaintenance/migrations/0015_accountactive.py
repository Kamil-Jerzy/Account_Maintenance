# Generated by Django 4.1.7 on 2023-04-08 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccountMaintenance', '0014_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountActive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.IntegerField()),
                ('account_name', models.CharField(max_length=32)),
                ('keep_subsidiary', models.CharField(default='N', max_length=1)),
                ('country_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AccountMaintenance.country')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AccountMaintenance.currency')),
            ],
        ),
    ]
