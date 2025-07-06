import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('user-register')
    data = {'username': 'newuser', 'password': 'newpass123'}
    response = api_client.post(url, data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_login(api_client, user):
    url = reverse('user-login')
    data = {'username': user.username, 'password': 'password'}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'token' in response.data

@pytest.mark.django_db
def test_user_logout(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user-logout')
    response = api_client.post(url)
    assert response.status_code == 204