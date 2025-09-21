import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from catalog.models import Category, Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="user", password="pass123")

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="admin", password="adminpass")

@pytest.fixture
def auth_client(user):
    client = APIClient()
    access = str(RefreshToken.for_user(user).access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client

@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    access = str(RefreshToken.for_user(admin_user).access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client

@pytest.fixture
def category(db):
    return Category.objects.create(name="Eletrônicos")

@pytest.fixture
def product(category, db):
    return Product.objects.create(
        sku="SKU-1",
        name="Headset",
        description="...",
        price="199.90",
        stock=10,
        is_active=True,
        category=category,
    )
