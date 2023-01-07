from fastapi.testclient import TestClient

from main import app
import models
from db import engine
from data_generator import generate_fake_data

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


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# these tests should test the round trip from a request coming in from the
# frontend to the response back to the front end


def test_get_tracks():
    response = client.get("/tracks")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["track_title"] != ""


def test_create_track():
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


def test_update_track():
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


def test_delete_track():
    response = client.get("/tracks")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/tracks/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/tracks/" + str(result["id"]))
    assert response.status_code == 404
