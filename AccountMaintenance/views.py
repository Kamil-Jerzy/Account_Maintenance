from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
import openpyxl
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from datetime import datetime

from .forms import WelcomeForm, AddAccountForm, ChangeAccountForm, DeleteAccountForm
from .models import Account, ExcelFile, Log

class WelcomeView(View):
    def get(self, request):
        maintenance_type = WelcomeForm()
        context = {'maintenance_type': maintenance_type}
        print(context)
        return render(request, 'home.html', context)
    def post(self, request):
        form = WelcomeForm(request.POST)
        if form.is_valid():
            maintenance_type = form.cleaned_data['maintenance_type']
            if maintenance_type == 'A':
                return redirect('account_add')
            elif maintenance_type == 'C':
                return redirect('account_change')
            elif maintenance_type == 'D':
                return redirect('account_delete')
        return HttpResponse("Error")


class AddAccountView(View):
    def get(self, request):
        add_form = AddAccountForm()
        context = {'add_form': add_form, }
        return render(request, 'account_add.html', context)

    def post(self, request):
        add_form = AddAccountForm(request.POST)
        if add_form.is_valid():
            maintenance_type = 'A'
            country_code = add_form.cleaned_data['country_code']
            account_number = add_form.cleaned_data['account_number']
            account_name = add_form.cleaned_data['account_name']
            currency = add_form.cleaned_data['currency']

            account = Account(
                country_code=country_code,
                account_number=account_number,
                account_name=account_name,
                currency=currency
            )
            account.save()

            context = {
                'maintenance_type': maintenance_type,
                'country_code': country_code,
                'account_number': account_number,
                'account_name': account_name,
                'currency': currency
            }

            # return render(request, 'account_add.html', context)
            return HttpResponse(f'Account {country_code}: {account_number} / {account_name} has been created')
        return HttpResponse("End at CreateAccountView")


class ChangeAccountView(View):
    def get(self, request):
        change_form = ChangeAccountForm()
        context = {'change_form': change_form}
        return render(request, 'account_change.html', context)

    def post(self, request):
        change_form = ChangeAccountForm(request.POST)
        if change_form.is_valid():
            maintenance_type = 'C'
            country_code = change_form.cleaned_data['country_code']
            account_number = change_form.cleaned_data['account_number']
            new_account_name = change_form.cleaned_data['account_name']

            try:
                account = Account.objects.get(country_code=country_code, account_number=account_number)
            except Account.DoesNotExist:
                return HttpResponse('Account does not exist')

            account.account_name = new_account_name
            account.save()

            context = {
                'maintenance_type': 'C',
                'account_number': account_number,
                'account_name': new_account_name
            }
            # return render(request, 'account_change.html', context)
            return HttpResponse(f'Name of account# {account_number} has been changed to {new_account_name}')
        return HttpResponse('Returning ChangeView')


class DeleteAccountView(View):
    def get(self, request):
        delete_form = DeleteAccountForm()
        context = {'delete_form': delete_form}
        return render(request, 'account_delete.html', context)

    def post(self, request):
        delete_form = ChangeAccountForm(request.POST)
        if delete_form.is_valid():
            maintenance_type = 'D'
            country_code = delete_form.cleaned_data['country_code']
            account_number = delete_form.cleaned_data['account_number']
            account_name = delete_form.cleaned_data['account_name']

            try:
                account = Account.objects.get(country_code=country_code, account_number=account_number)
            except Account.DoesNotExist:
                return HttpResponse('Account does not exist')

            account.delete()

            context = {
                'maintenance_type': 'D',
                'account_number': account_number,
                'account_name': account_name
            }
            # return render(request, 'account_change.html', context)
            return HttpResponse(f'The account# {account_number} has been deleted')
        return HttpResponse('Returning DeleteView')


def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        # Reading file content
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb['Sheet1']
        maintenance_type = worksheet['B1'].value
        country_code = worksheet['B2'].value
        account_number = worksheet['B3'].value
        account_name = worksheet['B4'].value
        currency = worksheet['B5'].value

        # # Save uploaded file to ExcelFile model
        # excel_file_model = ExcelFile(file=excel_file)
        # excel_file_model.save()

        context = {
            'maintenance_type': maintenance_type,
            'country_code': country_code,
            'account_number': account_number,
            'account_name': account_name,
            'currency': currency,
        }
        # Redirect to relevant stream depending on Maintenance Type
        if maintenance_type == 'A':
            return render(request, 'account_add_upload.html', context=context)
        elif maintenance_type == 'C':
            return render(request, 'account_change_upload.html', context=context)
        elif maintenance_type == 'D':
            return render(request, 'account_delete_upload.html', context=context)
        return render(request, 'account_change.html', context=context)
    return render(request, 'upload_excel.html')


def account_add_upload(request):
    if request.method == 'POST':
        # Get details from account_add_upload.html
        maintenance_type = request.POST['maintenance_type']
        country_code = request.POST['country_code']
        account_number = request.POST['account_number']
        account_name = request.POST['account_name']
        currency = request.POST['currency']
        keep_subsidiary = request.POST['keep_subsidiary']
        requestor = request.POST['requestor']
        approver = request.POST['approver']
        additional_info = request.POST['additional_info']
        created_by = request.POST['created_by']

        # Get current date
        current_date = datetime.now().date()

        # Save details to Account model
        account = Account(
            country_code=country_code,
            account_number=account_number,
            account_name=account_name,
            currency=currency,
            keep_subsidiary=keep_subsidiary
        )
        account.save()

        # Save details to Log model
        log = Log(
            maintenance_date=current_date,
            country_code=country_code,
            account_number=account_number,
            account_name=account_name,
            currency=currency,
            maintenance_type=maintenance_type,
            requestor=requestor,
            approver=approver,
            additional_info=additional_info,
            created_by=created_by
        )
        log.save()

        # Get the last uploaded Excel file
        last_file = ExcelFile.objects.last()
        if last_file:
            # Rename the file with the account number and country code
            filename = f'{country_code}_{account_number}.xlsx'
            # Save the renamed file to a drive (assuming default storage is a local filesystem)
            path = default_storage.save(os.path.join('excel_files', filename), ContentFile(last_file.file.read()))
            # Delete the original file from the database and disk
            last_file.delete()

        return HttpResponse(f'Account {country_code}: {account_number} / {account_name} has been created')
    else:
        return render(request, 'account_add_upload.html')


def account_change_upload(request):
    if request.method == 'POST':
        # Get details from account_change_upload.html
        maintenance_type = request.POST['maintenance_type']
        country_code = request.POST['country_code']
        account_number = request.POST['account_number']
        new_account_name = request.POST['account_name']
        currency = request.POST['currency']
        requestor = request.POST['requestor']
        approver = request.POST['approver']
        additional_info = request.POST['additional_info']
        created_by = request.POST['created_by']

        # Get current date
        current_date = datetime.now().date()

        # Checking if account is set up in Account model
        try:
            account = Account.objects.get(country_code=country_code, account_number=account_number)
        except Account.DoesNotExist:
            return HttpResponse('Account does not exist')

        # If account is set up change Account name and save
        account.account_name = new_account_name
        account.save()

        # Save details to Log model
        log = Log(
            maintenance_date=current_date,
            country_code=country_code,
            account_number=account_number,
            account_name=new_account_name,
            currency=currency,
            maintenance_type=maintenance_type,
            requestor=requestor,
            approver=approver,
            additional_info=additional_info,
            created_by=created_by
        )
        log.save()

        # Get the last uploaded Excel file
        last_file = ExcelFile.objects.last()
        if last_file:
            # Rename the file with the account number and country code
            filename = f'{country_code}_{account_number}.xlsx'
            # Save the renamed file to a drive (assuming default storage is a local filesystem)
            path = default_storage.save(os.path.join('excel_files', filename), ContentFile(last_file.file.read()))
            # Delete the original file from the database and disk
            last_file.delete()

        # account = Account(
        #     country_code=country_code,
        #     account_number=account_number,
        #     account_name=account_name,
        #     currency=currency
        # )
        # account.save()
        # return redirect('account_detail', pk=account.pk)
        return HttpResponse(f'Account {country_code}: {account_number} name has been changed to {new_account_name}')
    else:
        return render(request, 'account_change_upload.html')


def account_delete_upload(request):
    if request.method == 'POST':
        # Get details from account_add_upload.html
        maintenance_type = request.POST['maintenance_type']
        country_code = request.POST['country_code']
        account_number = request.POST['account_number']
        account_name = request.POST['account_name']
        currency = request.POST['currency']
        requestor = request.POST['requestor']
        approver = request.POST['approver']
        additional_info = request.POST['additional_info']
        created_by = request.POST['created_by']

        # Checking if account is set up in Account model
        try:
            account = Account.objects.get(country_code=country_code, account_number=account_number)
            keep_subsidiary = account.keep_subsidiary
            # Checking Keep Subsidiary value
            if keep_subsidiary == 'Y':
                return HttpResponse('Account has Keep Subsidiary set to Y, do the following: <p>' 
                                    '1) check account balances on subsidiary level <p>'
                                    '2) with 0.00 balances, change Keep Subsidiary parameter to N <p>'
                                    '3) resubmit request')
        except Account.DoesNotExist:
            return HttpResponse('Account does not exist')
        account.delete()

        # Get current date
        current_date = datetime.now().date()

        # Save details to Log model
        log = Log(
            maintenance_date=current_date,
            country_code=country_code,
            account_number=account_number,
            account_name=account_name,
            currency=currency,
            maintenance_type=maintenance_type,
            requestor=requestor,
            approver=approver,
            additional_info=additional_info,
            created_by=created_by
        )
        log.save()

        # Get the last uploaded Excel file
        last_file = ExcelFile.objects.last()
        if last_file:
            # Rename the file with the account number and country code
            filename = f'{country_code}_{account_number}.xlsx'
            # Save the renamed file to a drive (assuming default storage is a local filesystem)
            path = default_storage.save(os.path.join('excel_files', filename), ContentFile(last_file.file.read()))
            # Delete the original file from the database and disk
            last_file.delete()

        return HttpResponse(f'Account {country_code}: {account_number} / {account_name} has been deleted')
    else:
        return render(request, 'account_delete_upload.html')
