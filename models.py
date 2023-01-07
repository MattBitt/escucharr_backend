from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

# from sqlalchemy.orm import relationship

from db import Base


class Item(Base):
    """
    Defines the items model
    """

    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    def __repr__(self) -> str:
        return f"<Item {self.name}>"


class CommonModel(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def created(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def modified(cls):
        return Column(DateTime(timezone=True), onupdate=func.now())


class Source(Base, CommonModel):  # type: ignore
    __tablename__ = "sources"
    # Required
    url = Column(String(80), nullable=False)
    video_title = Column(String(80), nullable=False)
    # upload_date = db.Column(db.Date, nullable=False)

    # Not used on init
    ignore = Column(Boolean, nullable=False, default=False)
    plex_id = Column(String(40), default="")

    # Relationships
    # One to Many
    # files = db.relationship("File", back_populates="source")
    # tracks = relationship("Track", back_populates="source")

    # Many to One
    # album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    # album = db.relationship("Album", back_populates="album")

    def __repr__(self):
        return "SourceModel(id=%d,video_title=%s, url=%s,)" % (
            self.id,
            self.video_title,
            self.url,
        )


class Track(Base, CommonModel):  # type: ignore
    __tablename__ = "tracks"
    # Required
    track_title = Column(String(200), nullable=False)

    # Not needed on init?
    start_time = Column(Integer, nullable=False, default=0)  # in ms
    end_time = Column(Integer, nullable=False, default=0)

    # Not used on init
    # not sure where this is in the plexapi.
    # there should be a way to do it without matching files...
    plex_id = Column(String(40), default="")

    # Relationships
    # Track -> File (One to Many)
    # files = db.relationship("File", back_populates="track")

    # (Many to One)
    # album_id = column(db.Integer, db.ForeignKey("album.id"))
    # album = db.relationship("Album", back_populates="tracks")
    # source_id = Column(Integer, ForeignKey("sources.id"))
    # source = relationship("Source", back_populates="tracks")

    # (Many to Many)
    # artists = db.relationship("Artist", back_populates="track")
    # producers = db.relationship("Producer", back_populates="track")
    # beats = db.relationship("Beat", back_populates="track")
    # words = db.relationship("Word", back_populates="track")
    # tags = db.relationship("Tag", back_populates="track")

    def __repr__(self):
        return "TrackModel(id=%d,track_title=%s)" % (self.id, self.track_title)


class Album(Base, CommonModel):  # type: ignore
    __tablename__ = "albums"
    # Init
    album_name = Column(String(200), nullable=False)
    path = Column(String(200), nullable=False)
    track_prefix = Column(String(200), default="")

    #     # Relationships
    #     # (One to Many)
    #     sources = db.relationship("Source", back_populates="album")
    #     files = db.relationship("File", back_populates="album") # should have an image file
    #     tracks = db.relationship("Track", back_populates="album")

    def __repr__(self):
        return "Album(id=%d,album_name=%s)" % (self.id, self.album_name)


class Word(Base, CommonModel):  # type: ignore
    __tablename__ = "words"

    # Required
    word = Column(String(200))
    # need to add sequence order to word_track table

    def __repr__(self):
        return "Word(id=%d,word=%s)" % (self.id, self.word)


class Producer(Base, CommonModel):  # type: ignore
    __tablename__ = "producers"
    # Required
    producer = Column(String(200), nullable=False)
    youtube_url = Column(String(200))

    def __repr__(self):
        return "Producer(id=%d,producer=%s)" % (self.id, self.producer)


class Tag(Base, CommonModel):  # type: ignore
    __tablename__ = "tags"
    # Required
    # need to add sequence order
    tag = Column(String(200))

    def __repr__(self):
        return "Tag(id=%d,tag=%s)" % (self.id, self.tag)
