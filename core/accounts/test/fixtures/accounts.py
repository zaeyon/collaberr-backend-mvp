import pytest
from model_bakery import baker
from rest_framework.test import APIClient

@pytest.fixture
def account():
    return baker.make('Account', username='testuser', password='password123', email='testuser@test.com')

@pytest.fixture
def api_client():
    client = APIClient()
    return client

