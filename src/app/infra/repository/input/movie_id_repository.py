from typing import List, Protocol

from domain.models.internal.movie_model import MovieId
from infra.repository.input.base_repository import ENGINE
from sqlalchemy.engine.base import Engine

# ---------------------------
# SQL
# ---------------------------
TRUNCATE_MOVIE_IDS_TABLE = """\
-- TRUNCATE TABLE movie_ids
DELETE FROM movie_ids
"""
INSERT_MOVIE_ID = """\
INSERT INTO
    movie_ids
VALUES
    (
        %(movie_id)s,
        %(tmdb_id)s,
        %(imdb_id)s
    )
"""


class AbstractMovieIdRepository(Protocol):

    def truncate_movie_ids_table(self) -> None:
        raise NotImplementedError()


    def save_movie_ids(self, movie_id_list: List[MovieId]) -> None:
        raise NotImplementedError()


class MovieIdRepository:

    def __init__(self, engine: Engine = ENGINE) -> None:
        self.engine: Engine = engine

    def truncate_movie_ids_table(self) -> None:

        self.engine.execute(TRUNCATE_MOVIE_IDS_TABLE)

    def save_movie_ids(self, movie_id_list: List[MovieId]) -> None:
        for movie_id in movie_id_list:
            self.engine.execute(INSERT_MOVIE_ID, {
                "movie_id": movie_id.movie_id,
                "tmdb_id": movie_id.tmdb_id,
                "imdb_id": movie_id.imdb_id
            })


def init_movie_id_repository():
    return MovieIdRepository()
