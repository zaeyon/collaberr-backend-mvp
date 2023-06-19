import pytest
from rest_framework.test import APIClient
from ..models import Accounts


@pytest.mark.django_db
def test_client(api_client):
    response = api_client.get('/api/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(api_client):
    # Prepare the request data (e.g., username and password)
    account = Accounts.objects.create_user(
            username='testuserbaker',
            password='test',
            email='baker@test.com',
            )
    data = {
        'email': 'baker@test.com',
        'password': 'test'
    }

    # Send the POST request to the login endpoint
    response = api_client.post('/api/login/', data=data, format='json')

    # Assert the response status code
    assert response.status_code == 200

    # Verify the response data
    response_data = response.json()
    assert 'access' in response_data
    assert 'refresh' in response_data
