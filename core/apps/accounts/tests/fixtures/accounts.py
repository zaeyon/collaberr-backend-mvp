import pytest
from model_bakery import baker
from rest_framework.test import APIClient

@pytest.fixture
def account(db):
    account = baker.make('Account', username='testuser', password='test', email='testuser@test.com', id='87b81f2974b4a444')
    print(account)
    return account
@pytest.fixture
def api_client():
    client = APIClient()
    return client

