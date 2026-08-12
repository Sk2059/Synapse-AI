import pytest 

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "sksingh@example.com",
            "username": "sksingh",
            "password": "password123"
        },
    )
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "sksingh@example.com"
    assert data["username"] == "sksingh"
    assert "hashed_password" not in data
    
@pytest.mark.asyncio
async def test_duplicate_email(client):
    payload = {
        "email": "sksingh@example.com",
        "username": "sksingh",
        "password": "password123"
    }
    first_response = await client.post(
        "/api/v1/auth/register",
        json=payload
    )
    assert first_response.status_code == 200

    second_response = await client.post(
        "/api/v1/auth/register",
        json={

            **payload,
            "username": "sksingh2"
        }
    )
    assert second_response.status_code == 400

@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "sksingh@example.com",
            "username": "sksingh",
            "password": "password123"
        }
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "sksingh@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(client):
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "wrong@example.com",
                "username": "wronguser",
                "password": "TestPassword123",
            },
        )

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "wrong@example.com",
                "password": "WrongPassword123",
            },
        )

        assert response.status_code == 401
