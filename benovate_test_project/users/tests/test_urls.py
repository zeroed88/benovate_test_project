import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_root():
    assert reverse("users:api-root") == '/api/'

def test_api_loans():
    assert reverse('users:Loans-list') == '/api/loans/'
    assert reverse('users:Loans-detail', kwargs={'pk': 1}) == '/api/loans/1/'

def test_api_users():
    assert reverse('users:Users-list') == '/api/users/'
    assert reverse('users:Users-detail', kwargs={'pk': 1}) == '/api/users/1/'
