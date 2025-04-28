

async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    print(f"{response.json()=}")

    assert response.status_code == 200
