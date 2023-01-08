import crud
import schemas
import models
from routers import create_album_from_source
from faker import Faker
from itertools import repeat

from random import randrange
from db import db_session
from datetime import datetime


faker = Faker()


def load_random_records(repo, schema, num_to_load):
    object_list = []
    session = db_session()
    for i in repeat(None, num_to_load):
        rand_record = randrange(num_to_load) + 1
        object_data = repo().fetchById(rand_record, session=session)
        if object_data:
            object_list.append(object_data)
        else:
            return {"message": "Object not found"}
    session.close()
    return object_list


def fake_source():
    source = {}
    source["url"] = faker.image_url()
    source["video_title"] = faker.text(max_nb_chars=40).title()
    source["video_type"] = "Omegle Bars"
    source["episode_number"] = str(faker.pyint(min_value=0, max_value=100)).zfill(3)
    source["upload_date"] = faker.date_between(
        start_date=datetime(2017, 1, 1)
    ).strftime("%m-%d-%Y")
    source["separate_album_per_video"] = faker.pybool()
    if not source["separate_album_per_video"]:
        source["episode_number"] = ""
    source["album_id"] = create_album_from_source(source, db_session())
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
    session = db_session()
    repo().bulk_create(session, objects_to_insert)
    session.close()

    return 201


def delete_data(repo):
    session = db_session()
    repo().bulk_delete(session)
    session.close()


def data_exists(repo, num_records):
    session = db_session()
    rows = repo().fetchAll(session)
    session.close()
    return len(rows) == num_records


def assign_albums_to_sources():

    num_albums = 20  # how many albums to randomly select
    albums = load_random_records(crud.AlbumRepo, schemas.AlbumSchema, num_albums)
    session = db_session()
    for source in crud.SourceRepo().fetchAll(session=session):

        rand_record = randrange(num_albums) + 1
        source.album_id = albums[rand_record - 1].id
        session.add(source)
        session.commit()
    session.close()


def generate_fake_data():
    model_list = [
        {
            "repo": crud.SourceRepo,
            "model": models.Source,
            "schema": schemas.SourceBaseSchema,
            "num_to_create": 30,
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
            "repo": crud.WordRepo,
            "model": models.Word,
            "schema": schemas.WordBaseSchema,
            "num_to_create": 1000,
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
    # assign_albums_to_sources()
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
