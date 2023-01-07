from pydantic import BaseModel
from typing import Optional


class ItemBaseSchema(BaseModel):
    name: str
    price: int

    class Config:
        orm_mode = True


class ItemSchema(ItemBaseSchema):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True


class SourceBaseSchema(BaseModel):
    url: str
    video_title: str
    ignore: Optional[bool] = False
    plex_id: Optional[str] = ""

    class Config:
        orm_mode = True

    # this is how I did the relationship with Marshmallow
    # tracks = List(fields.Nested(TrackSchema(exclude=("id", "source"))))


class SourceSchema(SourceBaseSchema):
    id: int

    class Config:
        orm_mode = True


class TrackBaseSchema(BaseModel):
    track_title: str
    start_time: Optional[int] = 0
    end_time: Optional[int] = 0
    plex_id: Optional[str] = ""

    class Config:
        orm_mode = True

    # this is how I did the relationship with Marshmallow
    # source = fields.Nested(lambda: SourceSchema(only=("id", "video_title")))


class TrackSchema(TrackBaseSchema):
    id: int

    class Config:
        orm_mode = True


class AlbumBaseSchema(BaseModel):
    album_name: str
    path: str
    track_prefix: Optional[str] = ""

    class Config:
        orm_mode = True

    # this is how I did the relationship with Marshmallow
    # source = fields.Nested(lambda: SourceSchema(only=("id", "video_title")))


class AlbumSchema(AlbumBaseSchema):
    id: int

    class Config:
        orm_mode = True


class WordBaseSchema(BaseModel):
    word: str

    class Config:
        orm_mode = True


class WordSchema(WordBaseSchema):
    id: int

    class Config:
        orm_mode = True


class ProducerBaseSchema(BaseModel):
    producer: str
    youtube_url: Optional[str]

    class Config:
        orm_mode = True


class ProducerSchema(ProducerBaseSchema):
    id: int

    class Config:
        orm_mode = True


class TagBaseSchema(BaseModel):
    tag: str

    class Config:
        orm_mode = True


class TagSchema(TagBaseSchema):
    id: int

    class Config:
        orm_mode = True
