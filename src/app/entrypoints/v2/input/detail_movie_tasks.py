from typing import List

from domain.enums.movie_enums import MovieLanguage
from domain.models.internal.movie_model import Movie, MovieId
from infra.client.tmdb.tmdb_api import init_tmdb_client
from infra.repository.input.movie_id_repository import init_movie_id_repository
from infra.repository.input.movie_repository import init_movie_repository
from prefect import Flow, task


@task
def truncate_movie_details() -> None:
    movie_repository = init_movie_repository()
    movie_repository.truncate_movies()


@task
def extract_movie_ids() -> List[MovieId]:
    movie_id_repository = init_movie_id_repository()
    return movie_id_repository.fetch_all()


@task
def extract_movie_detail(movie_id: MovieId) -> Movie:
    tmdb_client = init_tmdb_client()
    return tmdb_client.fetch_movie_detail(
        movie_id=movie_id.tmdb_id,
        language=MovieLanguage.JP
    ).to_internal_movie(movie_id.movie_id)


@task
def load_movie_details(movies: List[Movie]) -> None:
    movie_repository = init_movie_repository()
    movie_repository.save_movie_list(movies)


with Flow("Detail Movie Tasks") as flow:
    truncate_task = truncate_movie_details()
    movie_ids = extract_movie_ids()
    movies = extract_movie_detail.map(movie_id=movie_ids)
    load_task = load_movie_details(movies)
    load_task.set_upstream(truncate_task)
