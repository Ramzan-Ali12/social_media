from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Post, Like

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='user1', password='pass')

@pytest.fixture
def user2(db):
    return User.objects.create_user(username='user2', password='pass')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def post(user):
    return Post.objects.create(author=user, content='Test post')

@pytest.mark.django_db
def test_post_creation(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('post-list')
    data = {'content': 'Created post'}
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['content'] == 'Created post'

@pytest.mark.django_db
def test_post_update_owner(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse('post-detail', args=[post.id])
    response = api_client.patch(url, {'content': 'Updated'})
    assert response.status_code == 200
    assert response.data['content'] == 'Updated'

@pytest.mark.django_db
def test_post_update_not_owner(api_client, user2, post):
    api_client.force_authenticate(user=user2)
    url = reverse('post-detail', args=[post.id])
    response = api_client.patch(url, {'content': 'Hacked'})
    assert response.status_code == 403

@pytest.mark.django_db
def test_post_delete_owner(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse('post-detail', args=[post.id])
    response = api_client.delete(url)
    assert response.status_code == 204

@pytest.mark.django_db
def test_post_delete_not_owner(api_client, user2, post):
    api_client.force_authenticate(user=user2)
    url = reverse('post-detail', args=[post.id])
    response = api_client.delete(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_post_list_view(api_client, post):
    url = reverse('post-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list) or isinstance(response.data, dict)  # DRF pagination

@pytest.mark.django_db
def test_post_detail_view(api_client, post):
    url = reverse('post-detail', args=[post.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == post.id

@pytest.mark.django_db
def test_like_post(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse('post-toggle-like', args=[post.id])
    response = api_client.post(url)
    assert response.status_code == 201
    assert Like.objects.filter(author=user, post=post).exists()

@pytest.mark.django_db
def test_unlike_post(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse('post-toggle-like', args=[post.id])
    api_client.post(url)  # Like
    response = api_client.post(url)  # Unlike
    assert response.status_code == 204
    assert not Like.objects.filter(author=user, post=post).exists()

@pytest.mark.django_db
def test_anonymous_post_list(api_client, post):
    url = reverse('post-list')
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_anonymous_post_detail(api_client, post):
    url = reverse('post-detail', args=[post.id])
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_anonymous_cannot_create(api_client):
    url = reverse('post-list')
    response = api_client.post(url, {'content': 'anon'})
    assert response.status_code == 401

@pytest.mark.django_db
def test_anonymous_cannot_like(api_client, post):
    url = reverse('post-toggle-like', args=[post.id])
    response = api_client.post(url)
    assert response.status_code == 401
