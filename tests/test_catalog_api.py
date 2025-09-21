import pytest
from catalog.models import Product

BASE = "/api"

@pytest.mark.django_db
def test_public_can_list_only_active_products(api_client, category):
    Product.objects.create(sku="A1", name="Ativo", price="10.00", stock=5, is_active=True, category=category)
    Product.objects.create(sku="B2", name="Inativo", price="10.00", stock=5, is_active=False, category=category)

    resp = api_client.get(f"{BASE}/catalog/products/")
    assert resp.status_code == 200
    assert resp.data["count"] == 1
    assert resp.data["results"][0]["name"] == "Ativo"

@pytest.mark.django_db
def test_non_admin_cannot_create_product(auth_client, category):
    payload = {"sku":"C3","name":"Proibido","price":"9.99","stock":3,"category":category.id,"is_active":True}
    resp = auth_client.post(f"{BASE}/catalog/products/", payload, format="json")
    assert resp.status_code in (401, 403)

@pytest.mark.django_db
def test_admin_can_create_product(admin_client, category):
    payload = {"sku":"D4","name":"Permitido","price":"12.50","stock":8,"category":category.id,"is_active":True}
    resp = admin_client.post(f"{BASE}/catalog/products/", payload, format="json")
    assert resp.status_code == 201
    assert resp.data["name"] == "Permitido"
