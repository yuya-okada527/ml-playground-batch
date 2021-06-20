from time import time_ns
from typing import List

from domain.models.elastic.elastic_movie_model import ElasticMovieModel
from domain.models.internal.movie_model import Movie
from prefect import Flow, task
from prefect.utilities.tasks import unmapped


@task
def create_exec_time() -> int:
    return time_ns()


@task
def extract_all_movies() -> List[Movie]:
    print("extract_all_movies")
    return []


@task
def transform_movie(movie: Movie, exec_time: int) -> ElasticMovieModel:
    print("transform_movie")
    return None


@task
def load_movies(movies: List[ElasticMovieModel]) -> None:
    print("load_movies")


@task
def delete_old(exec_time: int) -> None:
    print("delete_old")


with Flow("Feed Movies Task") as flow:

    exec_time = create_exec_time()
    movies = extract_all_movies()
    elastic_movies = transform_movie.map(movie=movies, exec_time=unmapped(exec_time))
    load_movies_task = load_movies(movies=elastic_movies)
    delete_old_task = delete_old(exec_time=exec_time)
    delete_old_task.set_upstream(load_movies_task)
