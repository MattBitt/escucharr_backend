def test_get_artists(client):
    response = client.get("/artists")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["artist"] != ""


def test_create_artist(client):
    request = {
        "artist": "live",
    }
    response = client.post("/artists/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/artists/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["artist"] == request["artist"]


def test_update_artist(client):
    response = client.get("/artists")
    result = list(response.json())[0]
    old_name = result["artist"]

    request = {
        "artist": "string",
        "id": result["id"],
    }
    assert old_name != request["artist"]
    response = client.put("/artists/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/artists/" + str(result["id"]))
    result = check_response.json()
    assert result["artist"] == request["artist"]


def test_delete_artist(client):
    response = client.get("/artists")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/artists/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/artists/" + str(result["id"]))
    assert response.status_code == 404
