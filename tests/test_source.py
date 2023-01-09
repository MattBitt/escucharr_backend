def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_sources(client):
    response = client.get("/sources")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["url"] != ""
    assert results[0]["video_title"] != ""


def test_create_source(client):
    request = {
        "url": "https://www.youtube.com/watch?v=AXFLcqQ0wGY",
        "video_title": "NEVER SEEN HARRY LIKE THIS?!!",
        "video_type": "Omegle Bars",
        "episode_number": "080",
        "upload_date": "01-07-2023",
        "separate_album_per_video": "True",
    }
    response = client.post("/sources/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/sources/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["url"] == request["url"]
    assert r_json["video_title"] == request["video_title"]
    assert r_json["ignore"] is False
    assert r_json["plex_id"] == ""


def test_update_source(client):
    response = client.get("/sources")
    result = list(response.json())[0]
    old_title = result["video_title"]
    old_url = result["url"]
    request = {
        "url": "https://www.youtube.com/watch?v=AXFLcqQ0wGY",
        "video_title": "NEVER SEEN HARRY LIKE THIS?!!",
        "video_type": "Omegle Bars",
        "episode_number": "080",
        "ignore": False,
        "plex_id": "",
        "id": result["id"],
        "upload_date": "01-07-2023",
        "separate_album_per_video": "True",
    }
    assert old_title != request["video_title"]
    assert old_url != request["url"]
    response = client.put("/sources/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/sources/" + str(result["id"]))
    result = check_response.json()
    assert result["url"] == request["url"]
    assert result["video_title"] == request["video_title"]


def test_delete_source(client):
    response = client.get("/sources")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/sources/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/sources/" + str(result["id"]))
    assert response.status_code == 404


def test_source_tracks(client):
    response = client.get("/sources")
    assert response.status_code == 200
    result = list(response.json())[0]
    assert len(result["tracks"]) > 0
