

async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    print(f"{response.json()=}")

    assert response.status_code == 200


async def test_post_facilities(ac):
    facility_data = "Массаж"
    response = await ac.post("/facilities", json={"title": facility_data})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_data
    assert "data" in res
