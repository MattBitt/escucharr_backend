def test_get_words(client):
    response = client.get("/words")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["word"] != ""


def test_create_word(client):
    request = {
        "word": "antidisistablishmentarianism",
    }
    response = client.post("/words/", json=request)
    assert response.status_code == 200
    new_id = response.json()["id"]
    response = client.get("/words/" + str(new_id))
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["id"] == new_id
    assert r_json["word"] == request["word"]


def test_update_word(client):
    response = client.get("/words")
    result = list(response.json())[0]
    old_name = result["word"]

    request = {
        "word": "string",
        "path": "string",
        "track_prefix": "",
        "id": result["id"],
    }
    assert old_name != request["word"]
    response = client.put("/words/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/words/" + str(result["id"]))
    result = check_response.json()
    assert result["word"] == request["word"]


def test_delete_word(client):
    response = client.get("/words")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/words/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/words/" + str(result["id"]))
    assert response.status_code == 404
