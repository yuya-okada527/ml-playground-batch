from typing import List

from infra.client.tmdb.tmdb_api import init_tmdb_client
from infra.repository.input.genre_repository import init_genre_repository
from prefect import Flow, Parameter, task
from service.input_service import exec_update_genre_master


@task
def update_genre_master(force_update: bool) -> None:
    print("update_genre_master")
    # リポジトリの初期化
    genre_repository = init_genre_repository()
    tmdb_client = init_tmdb_client()

    # サービスの実行
    exec_update_genre_master(
        force_update=force_update,
        genre_repository=genre_repository,
        tmdb_client=tmdb_client
    )


def update_genre_flow():
    with Flow("Update Genre Master") as flow:
        force_update = Parameter("force_update", default=True)
        update_genre_master(force_update)

    flow.run()
