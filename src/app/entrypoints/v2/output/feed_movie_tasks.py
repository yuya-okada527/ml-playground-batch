from time import time_ns
from typing import List

from domain.models.elastic.elastic_movie_model import (ElasticMovieModel, init,
                                                       refresh_index)
from domain.models.internal.movie_model import Movie
from infra.repository.input.movie_repository import init_movie_repository
from prefect import Flow, task
from prefect.utilities.edges import unmapped
from service.logic.output_logic import map_to_elastic_model


@task
def create_exec_time() -> int:
    return time_ns()


@task
def extract_all_movies() -> List[Movie]:
    movie_repository = init_movie_repository()
    result = movie_repository.fetch_all()
    return result


@task
def transform_movie(movie: Movie, exec_time: int) -> ElasticMovieModel:
    return map_to_elastic_model(movie, exec_time)


@task
def load_movies(movies: List[ElasticMovieModel]) -> None:
    init()
    for movie in movies:
        movie.save()


@task
def delete_old(exec_time: int) -> None:
    print("delete_old")


@task
def refresh() -> None:
    refresh_index()


with Flow("Feed Movies Task") as flow:

    exec_time = create_exec_time()
    movies = extract_all_movies()
    elastic_movies = transform_movie.map(movie=movies, exec_time=unmapped(exec_time))
    load_movies_task = load_movies(movies=elastic_movies)
    delete_old_task = delete_old(exec_time=exec_time)
    delete_old_task.set_upstream(load_movies_task)
    refresh_task = refresh()
    refresh.set_upstream(delete_old_task)
