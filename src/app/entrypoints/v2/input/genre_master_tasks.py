from typing import List

from infra.client.tmdb.tmdb_api import init_tmdb_client
from infra.repository.input.genre_repository import init_genre_repository
from prefect import Flow, task


@task
def update_genre_master():
    print("update_genre_master")
    genre_repository = init_genre_repository()
    tmdb_client = init_tmdb_client()
