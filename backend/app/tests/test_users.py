
import pytest

@pytest.mark.asyncio
async def test_get_current_user(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "TestPassword123",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "me@example.com",
            "password": "TestPassword123",
        },
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "me@example.com"

    @pytest.mark.asyncio
    async def test_users_me_invalid_token(client):
        response = await client.get(
            "/api/v1/users/me",
            headers={
                "Authorization": "Bearer invalid-token"
            },
        )

        assert response.status_code == 401