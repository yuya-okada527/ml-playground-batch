from typing import Protocol

from infra.repository.input.base_repository import ENGINE
from sqlalchemy.engine.base import Engine

# ---------------------------
# SQL
# ---------------------------
TRUNCATE_MOVIE_IDS_TABLE = """\
-- TRUNCATE TABLE movie_ids
DELETE FROM movie_ids
"""


class AbstractMovieIdRepository(Protocol):

    def truncate_movie_ids_table(self) -> None:
        raise NotImplementedError()



class MovieIdRepository:

    def __init__(self, engine: Engine = ENGINE) -> None:
        self.engine: Engine = engine

    def truncate_movie_ids_table(self) -> None:

        self.engine.execute(TRUNCATE_MOVIE_IDS_TABLE)



def init_movie_id_repository():
    return MovieIdRepository()
