import pytest
from catalog.models import Product

BASE = "/api"

@pytest.mark.django_db
def test_add_set_remove_cart(auth_client, product):
    # add
    resp = auth_client.post(f"{BASE}/orders/me/cart/add-item", {"product_id": product.id, "quantity": 2}, format="json")
    assert resp.status_code == 200
    assert len(resp.data["items"]) == 1
    assert resp.data["items"][0]["quantity"] == 2

    # set
    resp = auth_client.post(f"{BASE}/orders/me/cart/set-item", {"product_id": product.id, "quantity": 5}, format="json")
    assert resp.status_code == 200
    assert resp.data["items"][0]["quantity"] == 5

    # remove
    resp = auth_client.post(f"{BASE}/orders/me/cart/remove-item", {"product_id": product.id}, format="json")
    assert resp.status_code == 200
    assert len(resp.data["cart"]["items"]) == 0

@pytest.mark.django_db
def test_checkout_happy_path(auth_client, product):
    auth_client.post(f"{BASE}/orders/me/cart/add-item", {"product_id": product.id, "quantity": 2}, format="json")
    resp = auth_client.post(f"{BASE}/orders/me/cart/checkout", {"shipping_address": "Rua X, 123"}, format="json")
    assert resp.status_code == 200
    assert resp.data["status"] == "PENDING"

    product.refresh_from_db()
    assert product.stock == 8  # 10 - 2

@pytest.mark.django_db
def test_checkout_insufficient_stock(auth_client, product):
    product.stock = 1
    product.save(update_fields=["stock"])
    auth_client.post(f"{BASE}/orders/me/cart/add-item", {"product_id": product.id, "quantity": 2}, format="json")
    resp = auth_client.post(f"{BASE}/orders/me/cart/checkout", {"shipping_address": "Rua X, 123"}, format="json")
    assert resp.status_code == 400
    assert "Estoque insuficiente" in resp.data["detail"]
