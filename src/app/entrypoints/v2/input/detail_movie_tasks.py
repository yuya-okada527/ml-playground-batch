from typing import List

from domain.models.internal.movie_model import Movie, MovieId
from infra.repository.input.movie_repository import init_movie_repository
from prefect import Flow, task


@task
def truncate_movie_details() -> None:
    movie_repository = init_movie_repository()
    movie_repository.truncate_movies()

@task
def extract_movie_ids() -> List[MovieId]:
    print("fetch_movie_ids")
    return []

@task
def extract_movie_detail(movie_id: MovieId) -> Movie:
    print("fetch_movie_detail")
    return None

@task
def load_movie_details(movies: List[Movie]) -> None:
    print("load_movie_details")


with Flow("Detail Movie Tasks") as flow:
    truncate_task = truncate_movie_details()
    movie_ids = extract_movie_ids()
    movies = extract_movie_detail.map(movie_id=movie_ids)
    load_task = load_movie_details(movies)
    load_task.set_upstream(truncate_task)
