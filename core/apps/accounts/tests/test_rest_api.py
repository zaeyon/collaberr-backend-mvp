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


# def test_login(api_client, account):
#     response = api_client.post(
#             '/api/login/',
#             {'email': 'testuserbaker@test.com', 'password': 'test'},
#             format='json')

#     assert response.status_code == 200


# def test_edit_profile(api_client, account):
#     api_client.post('/api/login/', {
#         'email': 'testuser@test.com',
#         'password': 'test'
#         })

#     logged_in_user = get_user(api_client)
#     logged_in_user_id = logged_in_user.id
#     print(logged_in_user_id)
#     response = api_client.patch(f'/api/accounts/{logged_in_user_id}/',
#                                 {'username': 'new_username'})
#     assert response.status_code == 200
#     assert response.json() == {
#         'username': 'new_username',
#         'email': 'testuser@test.com',
#         'first_name': '',
#         'last_name': ''
#         }
