from django.db import models


class Currency(models.Model):
    currency = models.CharField(max_length=3, unique=True)
    currency_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.currency}'


class AccountChart(models.Model):
    country_code = models.CharField(max_length=2)
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=32)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    # currency = models.CharField(max_length=3)
    keep_subsidiary = models.CharField(max_length=1, default='N')


class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files')


class Log(models.Model):
    maintenance_date = models.DateField()
    country_code = models.CharField(max_length=2)
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=32)
    currency = models.CharField(max_length=3)
    maintenance_type = models.CharField(max_length=1)
    # --------------
    requestor = models.CharField(max_length=64)
    approver = models.CharField(max_length=64)
    additional_info = models.CharField(max_length=64)
    created_by = models.CharField(max_length=64)


class AccountOptions(models.Model):
    account_serial = models.IntegerField()
    account_type = models.CharField(max_length=3)
    balance_option = models.IntegerField()
    mapping_asset = models.IntegerField(null=True, blank=True)
    mapping_liab = models.IntegerField(null=True, blank=True)

