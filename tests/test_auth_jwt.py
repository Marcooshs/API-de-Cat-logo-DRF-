import pytest


@pytest.mark.django_db
def test_obtain_and_refresh_token(api_client, user):
    response = api_client.post(
        "/api/auth/login/",
        {"username": "user", "password": "pass123"},
        format="json",
    )
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data

    refresh_response = api_client.post(
        "/api/auth/refresh/",
        {"refresh": data["refresh"]},
        format="json",
    )
    assert refresh_response.status_code == 200
    refreshed_data = refresh_response.json()
    assert "access" in refreshed_data
