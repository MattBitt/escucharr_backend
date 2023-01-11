def test_get_beats(client):
    response = client.get("/beats")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["beat_name"] != ""


def test_create_beat(client):
    request = {
        "beat_name": "live",
    }
    response = client.post("/beats/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/beats/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["beat_name"] == request["beat_name"]


def test_update_beat(client):
    response = client.get("/beats")
    result = list(response.json())[0]
    old_name = result["beat_name"]

    request = {
        "beat_name": "string",
        "id": result["id"],
    }
    assert old_name != request["beat_name"]
    response = client.put("/beats/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/beats/" + str(result["id"]))
    result = check_response.json()
    assert result["beat_name"] == request["beat_name"]


def test_delete_beat(client):
    response = client.get("/beats")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/beats/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/beats/" + str(result["id"]))
    assert response.status_code == 404
