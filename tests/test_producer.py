def test_get_producers(client):
    response = client.get("/producers")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["producer"] != ""


def test_create_producer(client):
    request = {
        "producer": "anabolic beats",
    }
    response = client.post("/producers/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/producers/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["producer"] == request["producer"]


def test_update_producer(client):
    response = client.get("/producers")
    result = list(response.json())[0]
    old_name = result["producer"]

    request = {
        "producer": "string",
        "id": result["id"],
    }
    assert old_name != request["producer"]
    response = client.put("/producers/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/producers/" + str(result["id"]))
    result = check_response.json()
    assert result["producer"] == request["producer"]


def test_delete_producer(client):
    response = client.get("/producers")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/producers/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/producers/" + str(result["id"]))
    assert response.status_code == 404
