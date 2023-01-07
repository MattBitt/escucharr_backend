import crud
import schemas
import models
from faker import Faker

from random import randrange
from db import SessionLocal


faker = Faker()


def load_random_record(repo, schema, num_to_load):
    rand = randrange(20) + 1
    object_data = repo.fetchById(rand)
    if object_data:
        return object_data
    return {"message": "Object not found"}


def fake_source():
    source = {}
    source["url"] = faker.image_url()
    source["video_title"] = faker.text(max_nb_chars=40).title()
    # source["upload_date"] = datetime.utcnow()
    return source


def fake_track():
    track = {}
    track["track_title"] = faker.text(max_nb_chars=40).title()
    track["start_time"] = faker.pyint(
        min_value=0, max_value=3600000
    )  # between 0 and 1 hours worth of milliseconds
    track["end_time"] = faker.pyint(
        min_value=track["start_time"] + 60000, max_value=track["start_time"] + 240000
    )  # between 1 minute and 4 minutes long
    return track


def fake_album_data():
    fake_path = "/albums/"
    album = {}

    album["album_name"] = faker.text(max_nb_chars=40).title()
    album["path"] = fake_path + album["album_name"]
    album["track_prefix"] = faker.text(max_nb_chars=5).upper()
    return album


def fake_word_data():
    word = {}
    word["word"] = faker.text(max_nb_chars=8).lower().replace(".", "")
    return word


def fake_producer_data():
    producer = {}
    producer["producer"] = faker.name()
    producer["youtube_url"] = faker.image_url()
    return producer


def fake_tag_data():
    tag = {}
    tag["tag"] = faker.text(max_nb_chars=8).lower().replace(".", "")
    return tag


def generate_data(num_to_generate, fake_object):
    if num_to_generate <= 0:
        return {}
    objects = []
    for i in range(num_to_generate):
        objects.append(fake_object())
    return objects


def add_to_db(data_to_add, model, repo, schema):
    objects_to_insert = []
    for obj in data_to_add:
        data = schema(**obj)
        data_model = model(**data.dict())
        objects_to_insert.append(data_model)
    session = SessionLocal()
    repo().bulk_create(session, objects_to_insert)
    session.close()

    return 201


def delete_data(repo):
    session = SessionLocal()
    repo().bulk_delete(session)
    session.close()


def data_exists(repo, num_records):
    session = SessionLocal()
    rows = repo().fetchAll(session)
    session.close()
    return len(rows) == num_records


def generate_fake_data():
    model_list = [
        {
            "repo": crud.SourceRepo,
            "model": models.Source,
            "schema": schemas.SourceBaseSchema,
            "num_to_create": 50,
            "fake_data_func": fake_source,
        },
        {
            "repo": crud.TrackRepo,
            "model": models.Track,
            "schema": schemas.TrackBaseSchema,
            "num_to_create": 100,
            "fake_data_func": fake_track,
        },
        {
            "repo": crud.AlbumRepo,
            "model": models.Album,
            "schema": schemas.AlbumBaseSchema,
            "num_to_create": 50,
            "fake_data_func": fake_album_data,
        },
        {
            "repo": crud.WordRepo,
            "model": models.Word,
            "schema": schemas.WordBaseSchema,
            "num_to_create": 100,
            "fake_data_func": fake_word_data,
        },
        {
            "repo": crud.ProducerRepo,
            "model": models.Producer,
            "schema": schemas.ProducerBaseSchema,
            "num_to_create": 50,
            "fake_data_func": fake_producer_data,
        },
        {
            "repo": crud.TagRepo,
            "model": models.Tag,
            "schema": schemas.TagBaseSchema,
            "num_to_create": 100,
            "fake_data_func": fake_tag_data,
        },
    ]
    for model in model_list:
        if not data_exists(model["repo"], model["num_to_create"]):
            delete_data(model["repo"])
            objects = generate_data(model["num_to_create"], model["fake_data_func"])
            add_to_db(objects, model["model"], model["repo"], model["schema"])

    # tracks = generate_data(100, fake_track)
    # for track in tracks:
    #     track_object = TrackSchema().load(track)
    #     source = load_random_record(SourceRepo(), SourceSchema(), 1)
    #     source.tracks.append(track_object)
    #     SourceRepo().update(source)

    # add_to_db(tracks, TrackRepo(), TrackSchema())

    # albums = generate_data(20, fake_album_data)
    # add_to_db(albums, AlbumRepo(), AlbumSchema())


if __name__ == "__main__":
    generate_fake_data()
