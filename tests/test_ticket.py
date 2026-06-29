import logging


async def create_ticket(
    client,
    title: str = "Printer is broken",
    description: str | None = "The office printer does not print.",
    priority: str = "normal",
):
    return await client.post(
        "/tickets",
        json={
            "title": title,
            "description": description,
            "priority": priority,
        },
    )


async def login_admin(client):
    response = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_get_tickets(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.ticket")
    await create_ticket(
        client,
        title="VPN access",
        description="Need VPN access for a new laptop.",
        priority="high",
    )
    await create_ticket(
        client,
        title="Keyboard replacement",
        description="Keyboard has broken keys.",
        priority="low",
    )

    response = await client.get(
        "/tickets",
        params={
            "search": "vpn",
            "priority": "high",
            "sort_by": "created_at",
            "sort_order": "desc",
            "page": 1,
            "page_size": 10,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["pages"] == 1
    assert data["items"][0]["title"] == "VPN access"
    assert any(record.name == "app.services.ticket" for record in caplog.records)


async def test_get_tickets_negative_invalid_page_size(client):
    response = await client.get("/tickets", params={"page_size": 101})

    assert response.status_code == 422


async def test_get_tickets_search_is_case_insensitive_for_cyrillic(client):
    await create_ticket(
        client,
        title="Заявка на принтер",
        description="Проверить картридж.",
        priority="normal",
    )

    lower_response = await client.get("/tickets", params={"search": "заявка"})
    upper_response = await client.get("/tickets", params={"search": "ЗАЯВКА"})

    assert lower_response.status_code == 200
    assert upper_response.status_code == 200

    lower_data = lower_response.json()
    upper_data = upper_response.json()

    assert lower_data["total"] == 1
    assert lower_data["items"][0]["title"] == "Заявка на принтер"
    assert upper_data["total"] == 1
    assert upper_data["items"][0]["title"] == "Заявка на принтер"


async def test_get_ticket_by_id(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.ticket")
    create_response = await create_ticket(client, title="Monitor issue", priority="normal")
    ticket_id = create_response.json()["id"]

    response = await client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == "Monitor issue"
    assert data["status"] == "new"
    assert any(record.name == "app.services.ticket" for record in caplog.records)


async def test_get_ticket_by_id_negative_not_found(client, caplog):
    caplog.set_level(logging.WARNING, logger="app.services.ticket")

    response = await client.get("/tickets/999")

    assert response.status_code == 404
    assert any(record.levelno == logging.WARNING for record in caplog.records)


async def test_create_ticket(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.ticket")

    response = await create_ticket(
        client,
        title="install IDE",
        description="install IDE on a developer workstation.",
        priority="high",
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Install IDE"
    assert data["description"] == "Install IDE on a developer workstation."
    assert data["priority"] == "high"
    assert data["status"] == "new"
    assert data["created_at"]
    assert data["updated_at"]
    assert any(record.name == "app.services.ticket" for record in caplog.records)


async def test_create_ticket_negative_invalid_title(client):
    response = await client.post(
        "/tickets",
        json={
            "title": "No",
            "description": "Too short title.",
            "priority": "normal",
        },
    )

    assert response.status_code == 422


async def test_update_ticket_status(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.ticket")
    create_response = await create_ticket(client, title="Network issue", priority="high")
    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["status"] == "in_progress"
    assert any(record.name == "app.services.ticket" for record in caplog.records)


async def test_update_ticket_status_negative_done_ticket(client, caplog):
    caplog.set_level(logging.WARNING, logger="app.services.ticket")
    create_response = await create_ticket(client, title="Closed request", priority="normal")
    ticket_id = create_response.json()["id"]
    done_response = await client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "done"},
    )
    assert done_response.status_code == 200

    response = await client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "new"},
    )

    assert response.status_code == 409
    assert any(record.levelno == logging.WARNING for record in caplog.records)


async def test_update_ticket(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.ticket")
    create_response = await create_ticket(client, title="Old title", priority="low")
    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title": "updated title",
            "description": "updated description.",
            "priority": "high",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description."
    assert data["priority"] == "high"
    assert data["status"] == "new"
    assert any(record.name == "app.services.ticket" for record in caplog.records)


async def test_update_ticket_negative_done_ticket(client, caplog):
    caplog.set_level(logging.WARNING, logger="app.services.ticket")
    create_response = await create_ticket(client, title="Readonly request", priority="normal")
    ticket_id = create_response.json()["id"]
    done_response = await client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "done"},
    )
    assert done_response.status_code == 200

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title": "Should not update",
            "description": "Ticket is done.",
            "priority": "high",
        },
    )

    assert response.status_code == 409
    assert any(record.levelno == logging.WARNING for record in caplog.records)


async def test_update_ticket_negative_blank_title(client):
    create_response = await create_ticket(client, title="Whitespace title", priority="normal")
    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title": "   ",
            "description": "Title has only spaces.",
            "priority": "normal",
        },
    )

    assert response.status_code == 422


async def test_delete_ticket(client, caplog):
    caplog.set_level(logging.INFO, logger="app.services.ticket")
    admin_headers = await login_admin(client)
    create_response = await create_ticket(client, title="Temporary access", priority="low")
    ticket_id = create_response.json()["id"]

    response = await client.delete(f"/tickets/{ticket_id}", headers=admin_headers)

    assert response.status_code == 204

    get_response = await client.get(f"/tickets/{ticket_id}")
    assert get_response.status_code == 404
    assert any(record.name == "app.services.ticket" for record in caplog.records)


async def test_delete_ticket_negative_done_ticket(client, caplog):
    caplog.set_level(logging.WARNING, logger="app.services.ticket")
    admin_headers = await login_admin(client)
    create_response = await create_ticket(client, title="Do not delete", priority="normal")
    ticket_id = create_response.json()["id"]
    done_response = await client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "done"},
    )
    assert done_response.status_code == 200

    response = await client.delete(f"/tickets/{ticket_id}", headers=admin_headers)

    assert response.status_code == 409
    assert any(record.levelno == logging.WARNING for record in caplog.records)


async def test_delete_ticket_negative_without_admin_token(client):
    create_response = await create_ticket(client, title="No token delete", priority="normal")
    ticket_id = create_response.json()["id"]

    response = await client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 401
