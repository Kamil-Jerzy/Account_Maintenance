from django.test import TestCase

import pytest
from django.urls import reverse
from django.test import Client
from django.http import HttpRequest
from .views import WelcomeView

import pytest


def test_example():
    assert 1 == 1



class TestWelcomeView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_method(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')



#
#
# @pytest.fixture
# def client():
#     return Client()
#
#
# def test_welcome_view_get(client):
#     url = reverse('welcome')
#     request = HttpRequest()
#     response = WelcomeView.as_view()(request)
#     assert response.status_code == 200
#
#
# def test_welcome_view_post(client):
#     url = reverse('welcome')
#     response = client.post(url, {'maintenance_type': 'A'})
#     assert response.status_code == 302
#     assert response.url == reverse('account_add')
#
#
