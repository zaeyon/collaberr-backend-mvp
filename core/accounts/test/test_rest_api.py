import pytest
from rest_framework.test import APIClient
from model_bakery import baker

@pytest.mark.django_db
class TestAccountAPI:

    def test_login(self, client, account):
        response = client.post('/api/login/', {'email': account.email, 'password': 'password123'})
        assert response.status_code == 200

    def test_edit_profile(self, client, account):
        # Test profile editing
        client.force_authenticate(user=account)
        response = client.patch(f'/api/accounts/{account.id}/', {'email': 'new_email'})
        assert response.status_code == 200
        assert response.data['email'] == 'new_email'

    def test_create_campaign(self, client, account):
        # Test campaign creation
        client.force_authenticate(user=account)
        response = client.post('/api/campaigns/', {'title': 'Test Campaign', 'description': 'Test Description'})
        assert response.status_code == 201
        assert response.data['title'] == 'Test Campaign'
        assert response.data['description'] == 'Test Description'

    def test_edit_campaign(self, client, account):
        # Test campaign editing
        client.force_authenticate(user=account)
        response = client.patch(f'/api/campaigns/{account.id}/', {'title': 'Updated Campaign'})
        assert response.status_code == 200
        assert response.data['title'] == 'Updated Campaign'


