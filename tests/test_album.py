def test_get_albums(client):
    response = client.get("/albums")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["album_name"] != ""


def test_create_album(client):
    request = {
        "album_name": "NEVER SEEN HARRY LIKE THIS?!!",
        "path": "/albums/some fake path i made up",
    }
    response = client.post("/albums/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/albums/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["path"] == request["path"]
    assert r_json["album_name"] == request["album_name"]


def test_update_album(client):
    response = client.get("/albums")
    result = list(response.json())[0]
    old_name = result["album_name"]

    request = {
        "album_name": "string",
        "path": "string",
        "track_prefix": "",
        "id": result["id"],
    }
    assert old_name != request["album_name"]
    response = client.put("/albums/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/albums/" + str(result["id"]))
    result = check_response.json()
    assert result["album_name"] == request["album_name"]


def test_delete_album(client):
    response = client.get("/albums")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/albums/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/albums/" + str(result["id"]))
    assert response.status_code == 404
