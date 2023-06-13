import pytest
from model_bakery import baker
from rest_framework.test import APIClient

@pytest.fixture
def account(db):
    account = baker.make('Account', username='testuser', password='test', email='testuser@test.com')
    print(account)
    return account
@pytest.fixture
def api_client():
    client = APIClient()
    return client

