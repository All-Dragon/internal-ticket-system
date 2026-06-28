import logging


async def test_admin_login(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.auth")

    response = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert any(record.name == "app.services.auth" for record in caplog.records)


async def test_admin_login_negative_invalid_credentials(client, caplog):
    caplog.set_level(logging.WARNING, logger="app.services.auth")

    response = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrong"},
    )

    assert response.status_code == 401
    assert any(record.levelno == logging.WARNING for record in caplog.records)


async def test_admin_login_negative_invalid_payload(client):
    response = await client.post(
        "/auth/login",
        json={"username": "admin"},
    )

    assert response.status_code == 422
