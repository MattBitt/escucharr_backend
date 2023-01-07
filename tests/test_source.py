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


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# these tests should test the round trip from a request coming in from the
# frontend to the response back to the front end


def test_get_sources():
    response = client.get("/sources")
    assert response.status_code == 200
    results = list(response.json())
    assert len(results) > 0
    assert results[0]["url"] != ""
    assert results[0]["video_title"] != ""


def test_create_source():
    request = {
        "url": "https://www.youtube.com/watch?v=AXFLcqQ0wGY",
        "video_title": "NEVER SEEN HARRY LIKE THIS?!!",
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


def test_update_source():
    response = client.get("/sources")
    result = list(response.json())[0]
    old_title = result["video_title"]
    old_url = result["url"]
    request = {
        "url": "https://www.youtube.com/watch?v=AXFLcqQ0wGY",
        "video_title": "NEVER SEEN HARRY LIKE THIS?!!",
        "ignore": False,
        "plex_id": "",
        "id": result["id"],
    }
    assert old_title != request["video_title"]
    assert old_url != request["url"]
    response = client.put("/sources/" + str(result["id"]), json=request)
    assert response.status_code == 200
    check_response = client.get("/sources/" + str(result["id"]))
    result = check_response.json()
    assert result["url"] == request["url"]
    assert result["video_title"] == request["video_title"]


def test_delete_source():
    response = client.get("/sources")
    assert response.status_code == 200
    result = list(response.json())[0]
    response = client.delete("/sources/" + str(result["id"]))
    assert response.status_code == 200
    response = client.get("/sources/" + str(result["id"]))
    assert response.status_code == 404
