def test_get_tags(client):
    response = client.get("/tags")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["tag"] != ""


def test_create_tag(client):
    request = {
        "tag": "live",
    }
    response = client.post("/tags/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/tags/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["tag"] == request["tag"]


def test_update_tag(client):
    response = client.get("/tags")
    result = list(response.json())[0]
    old_name = result["tag"]

    request = {
        "tag": "string",
        "id": result["id"],
    }
    assert old_name != request["tag"]
    response = client.put("/tags/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/tags/" + str(result["id"]))
    result = check_response.json()
    assert result["tag"] == request["tag"]


def test_delete_tag(client):
    response = client.get("/tags")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/tags/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/tags/" + str(result["id"]))
    assert response.status_code == 404
