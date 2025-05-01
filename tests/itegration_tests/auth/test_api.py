


async def test_register_user(ac):
    resp = await ac.post("/auth/register", json={
                "email": "user3@example.com",
                "password": "string",
                "first_name": "string",
                "last_name": "string"
})

    assert resp.status_code == 200