import crud
import schemas
import models
from routers import get_or_create_album
from faker import Faker

from random import randrange
from db import Base, engine, db_session
from datetime import datetime
from main import logger

faker = Faker()


def load_random_record(repo):
    session = db_session()
    rand_record = randrange(repo().count_rows(session)) + 1
    session.close()
    return rand_record


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
    source_schema = schemas.SourceBaseSchema(**source)
    source["album_id"] = get_or_create_album(source_schema, db_session())
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
    track["source_id"] = load_random_record(crud.SourceRepo)
    session = db_session()
    track["album_id"] = (
        crud.SourceRepo().fetchById(track["source_id"], session).album_id
    )
    session.close()
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


def fake_beat_data():
    beat = {}
    beat["beat_name"] = faker.text(max_nb_chars=20).title()
    return beat


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


# def assign_albums_to_sources():

#     num_albums = 20  # how many albums to randomly select
#     albums = load_random_records(crud.AlbumRepo, schemas.AlbumSchema, num_albums)
#     session = db_session()
#     for source in crud.SourceRepo().fetchAll(session=session):

#         rand_record = randrange(num_albums) + 1
#         source.album_id = albums[rand_record - 1].id
#         session.add(source)
#         session.commit()
#     session.close()


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
            "num_to_create": 200,
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
        {
            "repo": crud.BeatRepo,
            "model": models.Beat,
            "schema": schemas.BeatBaseSchema,
            "num_to_create": 20,
            "fake_data_func": fake_beat_data,
        },
    ]
    # generates tables of data for the models above
    for model in model_list:
        logger.info("Generating fake data for {}".format(model["repo"]))
        if not data_exists(model["repo"], model["num_to_create"]):
            delete_data(model["repo"])
            objects = generate_data(model["num_to_create"], model["fake_data_func"])
            add_to_db(objects, model["model"], model["repo"], model["schema"])

    # now generate relationships (many to many)

    # track_words
    logger.info("Generating fake data for individual tracks")
    session = db_session()
    for track in crud.TrackRepo().fetchAll(session):
        logger.debug("Adding words to track")
        num_words = randrange(6) + 1  # choose up to 6 words per track
        for i in range(num_words):
            rand_word = load_random_record(crud.WordRepo)
            word = crud.WordRepo().fetchById(rand_word, session)
            if word not in track.words:
                track_word = models.TrackWord(
                    track_id=track.id, word_id=word.id, sequence_order=i + 1
                )
                session.add_all([track, track_word])
                session.commit()
        logger.debug("Adding tags to track")
        num_tags = randrange(4) + 1  # choose up to 4 tags per track
        for i in range(num_tags):
            rand_tag = load_random_record(crud.TagRepo)
            tag = crud.TagRepo().fetchById(rand_tag, session)
            if tag not in track.tags:
                track_tag = models.TrackTag(
                    track_id=track.id, tag_id=tag.id, sequence_order=i + 1
                )
                session.add_all([track, track_tag])
                session.commit()

        logger.debug("Adding producers to track")
        num_producers = randrange(3)  # choose up to 3 producers per track
        for i in range(num_producers):
            rand_producer = load_random_record(crud.ProducerRepo)
            producer = crud.ProducerRepo().fetchById(rand_producer, session)
            if producer not in track.producers:
                track_producer = models.TrackProducer(
                    track_id=track.id, producer_id=producer.id, sequence_order=i + 1
                )
                session.add_all([track, track_producer])
                session.commit()

        logger.debug("Adding beats to track")
        num_beats = randrange(2)  # choose up to 3 beats per track
        for i in range(num_beats):
            rand_beat = load_random_record(crud.BeatRepo)
            beat = crud.BeatRepo().fetchById(rand_beat, session)
            if beat not in track.beats:
                track_beat = models.TrackBeat(
                    track_id=track.id, beat_id=beat.id, sequence_order=i + 1
                )
                session.add_all([track, track_beat])
                session.commit()
    session.close()


if __name__ == "__main__":
    logger.info("Ready to generate fake data for the DB")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    generate_fake_data()
    logger.info("Data successfully generated")
    # session = db_session()
    # track = crud.TrackRepo().fetchById(12, session)
    # print(track)
    # session.close()
