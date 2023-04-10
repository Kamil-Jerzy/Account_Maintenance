from django.test import Client, TestCase
from .forms import ChangeAccountForm
from .models import AccountChart, Currency
from django.urls import reverse


class TestWelcomeView(TestCase):
    """
    This unit test class TestWelcomeView tests the GET method of the home view,
    ensuring it returns a 200 status code and uses the home.html template.
    """

    def setUp(self):
        self.client = Client()

    # Check GET method when rendering home.html
    def test_get_method(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class TestAddAccountView(TestCase):
    """
    Unit tests for the AddAccountView class, including GET and POST requests and account creation with validations.
    """
    def setUp(self):
        self.client = Client()
        self.add_account_url = reverse('account_add')
        self.currency = Currency.objects.create(currency_name='Euro', currency='EUR')
        self.form_data = {
            'country_code': 'IE',
            'account_number': '123',
            'account_name': 'Test Account',
            'currency': self.currency.pk,
            'keep_subsidiary': True,
            'requestor': 'Test',
            'approver': 'Test',
            'additional_info': 'Test',
            'created_by': 'Admin'
        }

    def test_get(self):
        response = self.client.get(self.add_account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_add.html')

    def test_post_valid(self):
        # create a new account
        response = self.client.post(self.add_account_url, self.form_data)
        self.assertEqual(response.status_code, 200)

        # # check if the account exists in the AccountChart model
        # account = AccountChart.objects.filter(account_number=self.form_data['account_number']).first()
        # self.assertIsNotNone(account)

    def test_post_account_exists(self):
        # create an account
        account = AccountChart(
            country_code='IE',
            account_number='123',
            account_name='Test Account',
            currency=self.currency,
            keep_subsidiary=True
        )
        account.save()

    def test_post_invalid(self):
        # submit an empty form
        form_data = {}
        response = self.client.post(self.add_account_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'End at CreateAccountView')


class ChangeAccountViewTest(TestCase):
    """
    Class ChangeAccountViewTest contains two methods for testing GET and POST requests on the account_change.html template.
    It also checks if account name has been changed.
    """
    def setUp(self):
        self.currency = Currency.objects.create(currency_name='Euro',
                                                currency='EUR')
        self.account = AccountChart.objects.create(
            country_code='IE',
            account_number='999',
            account_name='Test Account',
            currency=self.currency)
        self.url = reverse('account_change')

    # Check GET method when rendering account_change.html
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_change.html')
        self.assertIsInstance(response.context['change_form'], ChangeAccountForm)

    def test_post_valid_form(self):
        data = {
            'country_code': 'IE',
            'account_number': '999',
            'account_name': 'New Test Account',
            'requestor': 'John Doe',
            'approver': 'Jane Smith',
            'additional_info': 'Test additional info',
            'created_by': 'Admin'
        }
        # Create a currency object that matches the code in the form data
        currency = Currency.objects.create(currency_name='Test Currency', currency='FAKE CURRENCY')
        data['currency'] = currency
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        # Check that the account name has been updated
        updated_account = AccountChart.objects.get(id=self.account.id)
        self.assertEqual(updated_account.account_name, 'New Test Account')


class DeleteAccountViewTestCase(TestCase):
    """
    This class tests the functionality of deleting an account and keeping or deleting its subsidiary accounts using a client POST request,
    and asserts that the response status code is 200 and the account (or its subsidiary accounts) is either deleted or
    not based on the "keep_subsidiary" field value.
    """
    def setUp(self):
        self.client = Client()
        self.currency = Currency.objects.create(currency_name='Euro',
                                                currency='EUR')
        self.url = reverse('account_delete')
        self.account = AccountChart.objects.create(
            country_code='US',
            account_number=int(1234),
            account_name='Test Account',
            currency=self.currency,
            keep_subsidiary='N',
        )

    def test_delete_account(self):
        response = self.client.post(self.url, {
            'country_code': 'US',
            'account_number': int(1234),
            'account_name': 'Test Account',
            'requestor': 'Test User',
            'approver': 'Test User',
            'additional_info': 'Test Info',
            'created_by': 'Test User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AccountChart.objects.filter(country_code='US', account_number=int(1234)).exists())

    def test_keep_subsidiary(self):
        self.account.keep_subsidiary = 'Y'
        self.account.save()
        response = self.client.post(self.url, {
            'country_code': 'US',
            'account_number': '1234',
            'account_name': 'Test Account',
            'requestor': 'Test User',
            'approver': 'Test User',
            'additional_info': 'Test Info',
            'created_by': 'Test User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AccountChart.objects.filter(country_code='US', account_number='1234').exists())
