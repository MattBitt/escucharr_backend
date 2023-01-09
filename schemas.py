from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date, datetime


class SourceBaseSchema(BaseModel):
    url: str
    video_title: str
    video_type: str
    episode_number: Optional[str] = ""
    ignore: Optional[bool] = False
    plex_id: Optional[str] = ""
    upload_date: date
    separate_album_per_video: bool

    # when a source is created, it shouldn't have an album reference yet
    # after establishing the source, the album name/details should be created
    album_id: Optional[int]

    class Config:
        orm_mode = True

    @validator("upload_date", pre=True)
    def date_validate(cls, v):
        if type(v) == str:
            return datetime.strptime(v, "%m-%d-%Y")
        else:
            return v

    # this is how I did the relationship with Marshmallow
    # tracks = List(fields.Nested(TrackSchema(exclude=("id", "source"))))


class SourceSchema(SourceBaseSchema):
    id: int

    class Config:
        orm_mode = True


class TrackBaseSchema(BaseModel):
    track_title: str
    source_id: int
    start_time: Optional[int] = 0
    end_time: Optional[int] = 0
    plex_id: Optional[str] = ""
    source_id: int
    album_id: int

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


class BeatBaseSchema(BaseModel):
    beat_name: str

    class Config:
        orm_mode = True


class BeatSchema(BeatBaseSchema):
    id: int

    class Config:
        orm_mode = True


class SourceWithRelationships(SourceSchema):
    album: AlbumSchema
    tracks: List[TrackSchema]


class AlbumWithRelationships(AlbumSchema):
    sources: List[SourceSchema]


class TrackWithRelationships(TrackSchema):
    source: SourceSchema
    album: AlbumSchema
    words: List[WordSchema]
    tags: List[TagSchema]
    producers: List[ProducerSchema]
    beats: List[BeatSchema]


class WordWithRelationships(WordSchema):
    tracks: List[TrackSchema]


class TagWithRelationships(TagSchema):
    tracks: List[TrackSchema]


class ProducerWithRelationships(TagSchema):
    tracks: List[TrackSchema]


class BeatWithRelationships(TagSchema):
    tracks: List[TrackSchema]
