import os
import csv

from configs import cnf
from my_logging import logger
from utils import convert_hms_to_ms
import crud
import models
import schemas
from db import db_session, Base, engine
from getkey import getkey, keys


def import_tracks_from_csv():
    csv_name = cnf.APP_CONFIG.csv_to_import
    if not os.path.exists(csv_name):
        raise FileNotFoundError(f"File {csv_name} not found")

    with open(csv_name, "r") as f:
        csv_reader = csv.DictReader(f)
        track_info = list(csv_reader)
    return track_info


def show_word_options():
    print("Renaming Options:")
    print("Keep as is (Enter)")
    print("Change to Title Case (t)")
    print("Enter custom replacement (c)")
    print("There is an ERROR with the word (e)")
    print("This is not a word (n)")


def get_input_about_word(word):
    print(f"The word is:  '{word}'")
    key = getkey()
    if key == keys.ENTER:
        # keep it as lower case
        return word
    if key == "t":
        return word.title()
    if key == "c":
        pass
    if key == "e":
        pass
    if key == "n":
        pass
    else:
        pass


def add_to_db(data_to_add, model, repo, schema):
    data = schema(**data_to_add)
    data_model = model(**data.dict())
    session = db_session()
    db_object = repo.create(data_model, session)
    session.close()
    return db_object


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    tracks = import_tracks_from_csv()

    for track_row in tracks:
        session = db_session()
        track_title = track_row["title"]
        track = crud.TrackRepo.fetchByTrackTitle(track_title, session)

        sequence_number = 0

        words = track_title.split(",")
        for word_str in words:
            if track is not None:
                sequence_number = (
                    crud.TrackWordRepo().fetchLastWordSequence(track, session) + 1
                )
            word_to_add = word_str.lower().strip()
            word_dict = {"word": word_to_add}
            word = crud.WordRepo.fetchByWord(word_to_add, session)
            if word is None:
                data = schemas.WordBaseSchema(**word_dict)
                data_model = models.Word(**data.dict())
                word = crud.WordRepo.create(data_model, session)
                # word = add_to_db(
                #     word_dict, models.Word, crud.WordRepo, schemas.WordBaseSchema
                # )
            if word not in track.words:
                track_word = models.TrackWord(
                    track_id=track.id,
                    word_id=word.id,
                    sequence_order=sequence_number,
                )
            session.add_all([track, track_word])
            session.commit()
        session.close()

    # for each word in track title
    #   find the word in the db
    # if it doesn't exist, then create it
    # add the track and word to the TrackWord table increment sequence
