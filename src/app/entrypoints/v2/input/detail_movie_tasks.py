from typing import List

from domain.models.internal.movie_model import MovieId
from prefect import Flow, task


@task
def truncate_movie_details() -> None:
    print("truncate_movie_details")

@task
def fetch_movie_ids() -> List[MovieId]:
    print("fetch_movie_ids")
    return []


with Flow("Detail Movie Tasks") as flow:
    truncate_movie_details()
    fetch_movie_ids()
