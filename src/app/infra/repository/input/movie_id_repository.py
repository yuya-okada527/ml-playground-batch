from typing import List, Protocol

from domain.models.internal.movie_model import MovieId
from infra.repository.input.base_repository import ENGINE
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.result import RowProxy

# ---------------------------
# SQL
# ---------------------------
TRUNCATE_MOVIE_IDS_TABLE = """\
TRUNCATE TABLE movie_ids
-- DELETE FROM movie_ids
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
SELECT_ALL_MOVIE_ID_STATEMENT = """\
SELECT
    movie_id,
    tmdb_id,
    imdb_id
FROM
    movie_ids
"""
SELECT_MOVIE_ID_BY_TMDB_ID_STATEMENT = """\
SELECT
    movie_id,
    tmdb_id,
    imdb_id
FROM
    movie_ids
WHERE
    tmdb_id in (%(tmdb_ids)s)
"""


class AbstractMovieIdRepository(Protocol):

    def truncate_movie_ids_table(self) -> None:
        raise NotImplementedError()

    def save_movie_ids(self, movie_id_list: List[MovieId]) -> None:
        raise NotImplementedError()

    def fetch_all(self) -> List[MovieId]:
        raise NotImplementedError()

    def fetch_by_tmdb_ids(self, tmdb_ids: List[int]) -> List[MovieId]:
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

    def fetch_all(self) -> List[MovieId]:
        return [_map_to_movie_id(result) for result in self.engine.execute(SELECT_ALL_MOVIE_ID_STATEMENT)]

    def fetch_by_tmdb_ids(self, tmdb_ids: List[int]) -> List[MovieId]:
        results = self.engine.execute(SELECT_MOVIE_ID_BY_TMDB_ID_STATEMENT, {
            "tmdb_ids": ",".join([str(tmdb_id) for tmdb_id in tmdb_ids])
        })
        return [_map_to_movie_id(result) for result in results]


def _map_to_movie_id(result: RowProxy) -> MovieId:
    return MovieId(
        movie_id=result.movie_id,
        tmdb_id=result.tmdb_id,
        imdb_id=result.imdb_id
    )


def init_movie_id_repository():
    return MovieIdRepository()
