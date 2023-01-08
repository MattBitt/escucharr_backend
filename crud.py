from typing import List

from sqlalchemy.orm import Session  # type: ignore

from models import Source, Track, Album, Word, Producer, Tag


class SourceRepo:
    def create(self, source: Source, session: Session):
        session.add(source)
        session.commit()
        return source

    def fetchById(self, id: int, session: Session) -> Source:
        return session.query(Source).filter_by(id=id).first()

    def fetchAll(self, session: Session) -> List[Source]:
        return session.query(Source).all()

    def delete(self, id: int, session: Session) -> None:
        source = session.query(Source).filter_by(id=id).first()
        session.delete(source)
        session.commit()

    def update(
        self,
        source_data: Source,
        session: Session,
    ):
        session.merge(source_data)
        session.commit()

    def bulk_create(self, session: Session, sources_list):
        session.bulk_save_objects(sources_list)
        session.commit()

    def bulk_delete(self, session: Session):
        session.query(Source).delete()
        session.commit()


class TrackRepo:
    def create(self, track: Track, session: Session):
        session.add(track)
        session.commit()
        return track

    def fetchById(self, id: int, session: Session) -> Track:
        return session.query(Track).filter_by(id=id).first()

    def fetchAll(self, session: Session) -> List[Track]:
        return session.query(Track).all()

    def delete(self, id: int, session: Session) -> None:
        track = session.query(Track).filter_by(id=id).first()
        session.delete(track)
        session.commit()

    def update(
        self,
        track_data: Track,
        session: Session,
    ):
        session.merge(track_data)
        session.commit()

    def bulk_create(self, session: Session, tracks_list):
        session.bulk_save_objects(tracks_list)
        session.commit()

    def bulk_delete(self, session: Session):
        session.query(Track).delete()
        session.commit()


class AlbumRepo:
    def create(self, album: Album, session: Session):
        session.add(album)
        session.commit()
        return album

    def fetchById(self, id: int, session: Session) -> Album:
        return session.query(Album).filter_by(id=id).first()

    def fetchByAlbumName(self, album_name: str, session: Session) -> Album:
        return session.query(Album).filter_by(album_name=album_name).first()

    def fetchAll(self, session: Session) -> List[Album]:
        return session.query(Album).all()

    def delete(self, id: int, session: Session) -> None:
        album = session.query(Album).filter_by(id=id).first()
        session.delete(album)
        session.commit()

    def update(
        self,
        album_data: Album,
        session: Session,
    ):
        session.merge(album_data)
        session.commit()

    def bulk_create(self, session: Session, albums_list):
        session.bulk_save_objects(albums_list)
        session.commit()

    def bulk_delete(self, session: Session):
        session.query(Album).delete()
        session.commit()


class WordRepo:
    def create(self, word: Word, session: Session):
        session.add(word)
        session.commit()
        return word

    def fetchById(self, id: int, session: Session) -> Word:
        return session.query(Word).filter_by(id=id).first()

    def fetchAll(self, session: Session) -> List[Word]:
        return session.query(Word).all()

    def delete(self, id: int, session: Session) -> None:
        word = session.query(Word).filter_by(id=id).first()
        session.delete(word)
        session.commit()

    def update(
        self,
        word_data: Word,
        session: Session,
    ):
        session.merge(word_data)
        session.commit()

    def bulk_create(self, session: Session, words_list):
        session.bulk_save_objects(words_list)
        session.commit()

    def bulk_delete(self, session: Session):
        session.query(Word).delete()
        session.commit()


class ProducerRepo:
    def create(self, producer: Producer, session: Session):
        session.add(producer)
        session.commit()
        return producer

    def fetchById(self, id: int, session: Session) -> Producer:
        return session.query(Producer).filter_by(id=id).first()

    def fetchAll(self, session: Session) -> List[Producer]:
        return session.query(Producer).all()

    def delete(self, id: int, session: Session) -> None:
        producer = session.query(Producer).filter_by(id=id).first()
        session.delete(producer)
        session.commit()

    def update(
        self,
        producer_data: Producer,
        session: Session,
    ):
        session.merge(producer_data)
        session.commit()

    def bulk_create(self, session: Session, producers_list):
        session.bulk_save_objects(producers_list)
        session.commit()

    def bulk_delete(self, session: Session):
        session.query(Producer).delete()
        session.commit()


class TagRepo:
    def create(self, tag: Tag, session: Session):
        session.add(tag)
        session.commit()
        return tag

    def fetchById(self, id: int, session: Session) -> Tag:
        return session.query(Tag).filter_by(id=id).first()

    def fetchAll(self, session: Session) -> List[Tag]:
        return session.query(Tag).all()

    def delete(self, id: int, session: Session) -> None:
        tag = session.query(Tag).filter_by(id=id).first()
        session.delete(tag)
        session.commit()

    def update(
        self,
        tag_data: Tag,
        session: Session,
    ):
        session.merge(tag_data)
        session.commit()

    def bulk_create(self, session: Session, tags_list):
        session.bulk_save_objects(tags_list)
        session.commit()

    def bulk_delete(self, session: Session):
        session.query(Tag).delete()
        session.commit()
