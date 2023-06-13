import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth import get_user

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.mark.django_db
class TestAccountAPI:

    def test_login(self, client, account):
        response = client.post('/login/', {'email': "testuser@test.com", 'password': 'test'})
        assert response.status_code == 200

    def test_edit_profile(self, api_client, account):
        api_client.post('/login/', {'email': "testuser@test.com", 'password': 'test'})

        logged_in_user = get_user(api_client)
        logged_in_user_id = logged_in_user.id
        print(logged_in_user_id)
        response = api_client.patch(f'/api/accounts/{logged_in_user_id}/', {'username': 'new_username'})
        assert response.status_code == 200
        assert response.data['username'] == 'new_username'

    # def test_create_campaign(self, client, account):
    #     client.force_authenticate(user=account)
    #     response = client.post('/api/campaigns/', {'title': 'Test Campaign', 'description': 'Test Description'})
    #     assert response.status_code == 201
    #     assert response.data['title'] == 'Test Campaign'
    #     assert response.data['description'] == 'Test Description'

    # def test_edit_campaign(self, client, account):
    #     client.force_authenticate(user=account)
    #     response = client.patch(f'/api/campaigns/{account.id}/', {'title': 'Updated Campaign'})
    #     assert response.status_code == 200
    #     assert response.data['title'] == 'Updated Campaign'


