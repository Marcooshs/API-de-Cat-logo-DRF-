from django.test import Client

def test_healthz_ok():
    c = Client()
    resp = c.get("/healthz/")
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"
