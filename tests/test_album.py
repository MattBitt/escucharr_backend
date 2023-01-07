from fastapi.testclient import TestClient

from main import app
from data_generator import generate_fake_data
import models
from db import engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

generate_fake_data()


# these tests should test the round trip from a request coming in from the
# frontend to the response back to the front end


def test_get_albums():
    response = client.get("/albums")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["album_name"] != ""


def test_create_album():
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


def test_update_album():
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


def test_delete_album():
    response = client.get("/albums")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/albums/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/albums/" + str(result["id"]))
    assert response.status_code == 404
