from django import forms
from django.core.exceptions import ValidationError
from .models import Currency

COUNTRY = (
    ('IE', 'Ireland'),
    ('LU', 'Luxembourg'),

)

MAINT_TYPE = (
    ('A', 'Add'),
    ('C', 'Change'),
    ('D', 'Delete'),
)

class WelcomeForm(forms.Form):
    maintenance_type = forms.ChoiceField(label='Maintenance Type',
                                         choices=MAINT_TYPE,
                                         widget=forms.RadioSelect)

def account_no_validator(value):
    if not (90000 <= value <= 94999):  # Sprawdzamy czy podana wartość nie mieści się w podanym pprzedziale
        # Jeśli dane nie są poprawne funkcja walidująca zawsze powinna podnieść wyjątek ValidationError
        raise ValidationError(f'Wartość {value} nie mieści się w przedziale od 90000 do 94999')


class AddAccountForm(forms.Form):
    country_code = forms.ChoiceField(choices=COUNTRY, widget=forms.RadioSelect)
    # maintenance_type = forms.ChoiceField(label='Maintenance Type',
    #                                      choices=MAINT_TYPE,
    #                                      widget=forms.RadioSelect)
    account_number = forms.IntegerField(label='Account Number')
    # account_number = forms.IntegerField(label='Account Number',
    #                                     validators=[account_no_validator])
    account_name = forms.CharField(label="Account Name", max_length=32)
    #currency = forms.CharField(label="Currency", max_length=3)
    currency = forms.ModelChoiceField(label="Currency", queryset=Currency.objects.all())

    # account_branch = forms.IntegerField(label='Account Branch')
    # account_serial = forms.IntegerField(label='Account Serial')
    # account_suffix = forms.IntegerField(label='Account Suffix')

class ChangeAccountForm(forms.Form):
    country_code = forms.ChoiceField(choices=COUNTRY, widget=forms.RadioSelect)
    account_number = forms.IntegerField(label='Account Number')
    account_name = forms.CharField(label="Account Name", max_length=32)

class DeleteAccountForm(forms.Form):
    country_code = forms.ChoiceField(choices=COUNTRY, widget=forms.RadioSelect)
    account_number = forms.IntegerField(label='Account Number')
    account_name = forms.CharField(label="Account Name", max_length=32)