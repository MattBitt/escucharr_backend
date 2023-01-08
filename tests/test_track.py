def test_get_tracks(client):
    response = client.get("/tracks")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["track_title"] != ""


def test_create_track(client):
    request = {
        "track_title": "test track",
        "start_time": 105525,
        "end_time": 108356,
    }
    response = client.post("/tracks/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/tracks/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["track_title"] == request["track_title"]
    assert r_json["start_time"] == request["start_time"]
    assert r_json["end_time"] == request["end_time"]
    assert r_json["plex_id"] == ""


def test_update_track(client):
    response = client.get("/tracks")
    result = list(response.json())[0]
    old_title = result["track_title"]
    request = {
        "track_title": "This is a brand new track!",
        "start_time": 205525,
        "end_time": 208925,
        "plex_id": "",
        "id": result["id"],
    }
    assert old_title != request["track_title"]
    response = client.put("/tracks/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/tracks/" + str(result["id"]))
    result = check_response.json()
    assert result["track_title"] == request["track_title"]


def test_delete_track(client):
    response = client.get("/tracks")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/tracks/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/tracks/" + str(result["id"]))
    assert response.status_code == 404
