from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from products.views import product_detail
from mixer.backend.django import mixer
from django.test import TestCase
import pytest

@pytest.fixture(scope='module')
def factory():
    return RequestFactory()

@pytest.fixture
def product(db):
    return mixer.blend('products.Product')

def test_product_detail_authenticated(factory, product):
    path = reverse('detail', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = mixer.blend(User)

    response = product_detail(request, pk=1)
    assert response.status_code == 200

def test_product_detail_unauthenticated(factory, product):
    path = reverse('detail', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = product_detail(request, pk=1)
    assert 'accounts/login' in response.url
