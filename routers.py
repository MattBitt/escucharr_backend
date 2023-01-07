from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
from db import SessionLocal, engine
from schemas import (
    ItemBaseSchema,
    ItemSchema,
    SourceSchema,
    SourceBaseSchema,
    TrackSchema,
    TrackBaseSchema,
    AlbumSchema,
    AlbumBaseSchema,
    WordSchema,
    WordBaseSchema,
    ProducerSchema,
    ProducerBaseSchema,
    TagSchema,
    TagBaseSchema,
)

models.Base.metadata.create_all(bind=engine)
itemrouter = APIRouter(prefix="/items", tags=["items"])
source_router = APIRouter(prefix="/sources", tags=["Sources"])
track_router = APIRouter(prefix="/tracks", tags=["Tracks"])
album_router = APIRouter(prefix="/albums", tags=["Albums"])
word_router = APIRouter(prefix="/words", tags=["Words"])
producer_router = APIRouter(prefix="/producers", tags=["Producers"])
tag_router = APIRouter(prefix="/tags", tags=["Tags"])


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@itemrouter.get("/", response_model=List[ItemSchema])
def read_items(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    items = crud.get_items(session=session, skip=skip, limit=limit)
    return items


@itemrouter.get("/{id}", response_model=ItemSchema)
def read_item(id: int, session: Session = Depends(get_session)):
    item = crud.get_item_by_name(session=session, id=id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@itemrouter.post("/")
def create_item(item: ItemBaseSchema, session: Session = Depends(get_session)):
    item = crud.add_item(item=item, session=session)
    return item


# ******************************** SOURCE ROUTER *************************
# These functions are called from the front end
# either nothing or an id is sent by the front end
# this data is sent (along with db session) to the db functions
@source_router.get("/", response_model=List[SourceSchema])
def read_sources(session: Session = Depends(get_session)):
    sources = crud.SourceRepo().fetchAll(session=session)
    return sources


@source_router.get("/{id}", response_model=SourceSchema)
def read_source(id: int, session: Session = Depends(get_session)):
    source = crud.SourceRepo().fetchById(session=session, id=id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@source_router.post("/", response_model=SourceSchema)
def create_source(source: SourceBaseSchema, session: Session = Depends(get_session)):
    source_model = models.Source(**source.dict())
    source = crud.SourceRepo().create(session=session, source=source_model)
    return source


@source_router.put("/{id}", response_model=SourceSchema)
def update_source(source: SourceSchema, session: Session = Depends(get_session)):
    updated_source = crud.SourceRepo().fetchById(id=source.id, session=session)
    if updated_source:
        updated_source.video_title = source.video_title
        updated_source.url = source.url
        # TODO update all fields
        source = crud.SourceRepo().update(source_data=updated_source, session=session)
        source = crud.SourceRepo().fetchById(id=updated_source.id, session=session)
        return source
    return {"message": "source not found"}, 404


@source_router.delete("/{id}")
def delete_source(id: int, session: Session = Depends(get_session)):
    source_data = crud.SourceRepo().fetchById(id=id, session=session)
    if source_data:
        crud.SourceRepo().delete(id=id, session=session)
        return {"message": "source deleted successfully"}, 200
    return {"message": "source not found"}, 404

    # ******************************** SOURCE ROUTER *************************


# ******************************** TRACK ROUTER *************************
# These functions are called from the front end
# either nothing or an id is sent by the front end
# this data is sent (along with db session) to the db functions
@track_router.get("/", response_model=List[TrackSchema])
def read_tracks(session: Session = Depends(get_session)):
    tracks = crud.TrackRepo().fetchAll(session=session)
    return tracks


@track_router.get("/{id}", response_model=TrackSchema)
def read_track(id: int, session: Session = Depends(get_session)):
    track = crud.TrackRepo().fetchById(session=session, id=id)
    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@track_router.post("/", response_model=TrackSchema)
def create_track(track: TrackBaseSchema, session: Session = Depends(get_session)):
    track_model = models.Track(**track.dict())
    track = crud.TrackRepo().create(session=session, track=track_model)
    return track


@track_router.put("/{id}", response_model=TrackSchema)
def update_track(track: TrackSchema, session: Session = Depends(get_session)):
    updated_track = crud.TrackRepo().fetchById(id=track.id, session=session)
    if updated_track:
        updated_track.track_title = track.track_title
        updated_track.start_time = track.start_time
        updated_track.end_time = track.end_time
        updated_track.plex_id = track.plex_id
        track = crud.TrackRepo().update(track_data=updated_track, session=session)
        track = crud.TrackRepo().fetchById(id=updated_track.id, session=session)
        return track
    return {"message": "track not found"}, 404


@track_router.delete("/{id}")
def delete_track(id: int, session: Session = Depends(get_session)):
    track_data = crud.TrackRepo().fetchById(id=id, session=session)
    if track_data:
        crud.TrackRepo().delete(id=id, session=session)
        return {"message": "track deleted successfully"}, 200
    return {"message": "track not found"}, 404

    # ******************************** TRACK ROUTER *************************


# ******************************** ALBUM ROUTER *************************
# These functions are called from the front end
# either nothing or an id is sent by the front end
# this data is sent (along with db session) to the db functions
@album_router.get("/", response_model=List[AlbumSchema])
def read_albums(session: Session = Depends(get_session)):
    albums = crud.AlbumRepo().fetchAll(session=session)
    return albums


@album_router.get("/{id}", response_model=AlbumSchema)
def read_album(id: int, session: Session = Depends(get_session)):
    album = crud.AlbumRepo().fetchById(session=session, id=id)
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@album_router.post("/", response_model=AlbumSchema)
def create_album(album: AlbumBaseSchema, session: Session = Depends(get_session)):
    album_model = models.Album(**album.dict())
    album = crud.AlbumRepo().create(session=session, album=album_model)
    return album


@album_router.put("/{id}", response_model=AlbumSchema)
def update_album(album: AlbumSchema, session: Session = Depends(get_session)):
    updated_album = crud.AlbumRepo().fetchById(id=album.id, session=session)
    if updated_album:
        updated_album.album_name = album.album_name
        updated_album.path = album.path
        updated_album.track_prefix = album.track_prefix
        album = crud.AlbumRepo().update(album_data=updated_album, session=session)
        album = crud.AlbumRepo().fetchById(id=updated_album.id, session=session)
        return album
    return {"message": "album not found"}, 404


@album_router.delete("/{id}")
def delete_album(id: int, session: Session = Depends(get_session)):
    album_data = crud.AlbumRepo().fetchById(id=id, session=session)
    if album_data:
        crud.AlbumRepo().delete(id=id, session=session)
        return {"message": "album deleted successfully"}, 200
    return {"message": "album not found"}, 404


# ******************************** ALBUM ROUTER *************************


# ******************************** WORD ROUTER *************************
# These functions are called from the front end
# either nothing or an id is sent by the front end
# this data is sent (along with db session) to the db functions
@word_router.get("/", response_model=List[WordSchema])
def read_words(session: Session = Depends(get_session)):
    words = crud.WordRepo().fetchAll(session=session)
    return words


@word_router.get("/{id}", response_model=WordSchema)
def read_word(id: int, session: Session = Depends(get_session)):
    word = crud.WordRepo().fetchById(session=session, id=id)
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@word_router.post("/", response_model=WordSchema)
def create_word(word: WordBaseSchema, session: Session = Depends(get_session)):
    word_model = models.Word(**word.dict())
    word = crud.WordRepo().create(session=session, word=word_model)
    return word


@word_router.put("/{id}", response_model=WordSchema)
def update_word(word: WordSchema, session: Session = Depends(get_session)):
    updated_word = crud.WordRepo().fetchById(id=word.id, session=session)
    if updated_word:
        updated_word.word = word.word
        word = crud.WordRepo().update(word_data=updated_word, session=session)
        word = crud.WordRepo().fetchById(id=updated_word.id, session=session)
        return word
    return {"message": "word not found"}, 404


@word_router.delete("/{id}")
def delete_word(id: int, session: Session = Depends(get_session)):
    word_data = crud.WordRepo().fetchById(id=id, session=session)
    if word_data:
        crud.WordRepo().delete(id=id, session=session)
        return {"message": "word deleted successfully"}, 200
    return {"message": "word not found"}, 404


# ******************************** WORD ROUTER *************************


# ******************************** PRODUCER ROUTER *************************
# These functions are called from the front end
# either nothing or an id is sent by the front end
# this data is sent (along with db session) to the db functions
@producer_router.get("/", response_model=List[ProducerSchema])
def read_producers(session: Session = Depends(get_session)):
    producers = crud.ProducerRepo().fetchAll(session=session)
    return producers


@producer_router.get("/{id}", response_model=ProducerSchema)
def read_producer(id: int, session: Session = Depends(get_session)):
    producer = crud.ProducerRepo().fetchById(session=session, id=id)
    if producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer


@producer_router.post("/", response_model=ProducerSchema)
def create_producer(
    producer: ProducerBaseSchema, session: Session = Depends(get_session)
):
    producer_model = models.Producer(**producer.dict())
    producer = crud.ProducerRepo().create(session=session, producer=producer_model)
    return producer


@producer_router.put("/{id}", response_model=ProducerSchema)
def update_producer(producer: ProducerSchema, session: Session = Depends(get_session)):
    updated_producer = crud.ProducerRepo().fetchById(id=producer.id, session=session)
    if updated_producer:
        updated_producer.producer = producer.producer
        producer = crud.ProducerRepo().update(
            producer_data=updated_producer, session=session
        )
        producer = crud.ProducerRepo().fetchById(
            id=updated_producer.id, session=session
        )
        return producer
    return {"message": "producer not found"}, 404


@producer_router.delete("/{id}")
def delete_producer(id: int, session: Session = Depends(get_session)):
    producer_data = crud.ProducerRepo().fetchById(id=id, session=session)
    if producer_data:
        crud.ProducerRepo().delete(id=id, session=session)
        return {"message": "producer deleted successfully"}, 200
    return {"message": "producer not found"}, 404


# ******************************** PRODUCER ROUTER *************************


# ******************************** TAG ROUTER *************************
# These functions are called from the front end
# either nothing or an id is sent by the front end
# this data is sent (along with db session) to the db functions
@tag_router.get("/", response_model=List[TagSchema])
def read_tags(session: Session = Depends(get_session)):
    tags = crud.TagRepo().fetchAll(session=session)
    return tags


@tag_router.get("/{id}", response_model=TagSchema)
def read_tag(id: int, session: Session = Depends(get_session)):
    tag = crud.TagRepo().fetchById(session=session, id=id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@tag_router.post("/", response_model=TagSchema)
def create_tag(tag: TagBaseSchema, session: Session = Depends(get_session)):
    tag_model = models.Tag(**tag.dict())
    tag = crud.TagRepo().create(session=session, tag=tag_model)
    return tag


@tag_router.put("/{id}", response_model=TagSchema)
def update_tag(tag: TagSchema, session: Session = Depends(get_session)):
    updated_tag = crud.TagRepo().fetchById(id=tag.id, session=session)
    if updated_tag:
        updated_tag.tag = tag.tag
        tag = crud.TagRepo().update(tag_data=updated_tag, session=session)
        tag = crud.TagRepo().fetchById(id=updated_tag.id, session=session)
        return tag
    return {"message": "tag not found"}, 404


@tag_router.delete("/{id}")
def delete_tag(id: int, session: Session = Depends(get_session)):
    tag_data = crud.TagRepo().fetchById(id=id, session=session)
    if tag_data:
        crud.TagRepo().delete(id=id, session=session)
        return {"message": "tag deleted successfully"}, 200
    return {"message": "tag not found"}, 404


# ******************************** TAG ROUTER *************************
