from datetime import date
from typing import List

from core.config import TmdbSettings
from domain.models.internal.movie_model import MovieId
from infra.repository.object_storage.object_model import ObjectKey
from infra.repository.object_storage.object_storage_repository import \
    init_object_storage_repository
from prefect import Flow, Parameter, task
from util.http_util import call_get_api


@task
def extract_daily_file(target_date: date) -> ObjectKey:

    # パラメータを取得
    target_date = target_date or date.today()

    # オブジェクトのキー名を作成
    object_key = ObjectKey(
        bucket_name="ml-playground-movie-data",
        object_key=f"tmdb/movies/{target_date.year}/{target_date.month}/{target_date.day}.json.gz"
    )

    # 取得済みの場合、処理しない
    object_storage_repository = init_object_storage_repository()
    if object_storage_repository.exists(object_key):
        return object_key

    # TMDBから日時ファイルを取得
    tmdb_settings = TmdbSettings()
    daily_file_url = tmdb_settings.tmdb_file_url + f"movie_ids_{target_date.month:02}_{target_date.day}_{target_date.year}.json.gz"
    file_response = call_get_api(url=daily_file_url)

    # ファイルを保存
    object_storage_repository.save(file_response.content, object_key)

    return object_key


@task
def truncate_movie_ids() -> None:
    print("truncate_movie_ids")


@task
def make_movie_ids(daily_file_key: ObjectKey, max_id_size: int) -> List[MovieId]:
    """映画IDを発番します.

    Args:
        daily_file_key: 日時ファイル識別子
        max_id_size: 発番する映画IDの最大数

    Returns:
        List[MovieId]: 映画IDリスト
    """
    print("make_movie_ids")
    return []


@task
def chunck_movie_id_list(movie_id_list: List[MovieId]) -> List[List[MovieId]]:
    print("chunck_movie_id_list")
    return []


@task
def load_movie_id_list(movie_id_list: List[MovieId]):
    print("load_movie_id_list")
    pass


with Flow("Daily File") as flow:

    # 日時ファイルを取得
    target_date = Parameter("target_date", default=None)
    daily_file_key = extract_daily_file(target_date=target_date)

    # 映画IDを全て削除
    truncate_result = truncate_movie_ids()

    # 映画IDを発番
    max_id_size = Parameter("max_id_size", default=300)
    movie_id_list = make_movie_ids(daily_file_key=daily_file_key, max_id_size=max_id_size)

    # 映画IDをチャンク化
    # chunk_size = Parameter("chunk_size", default=100)
    chunked_movie_id_list = chunck_movie_id_list(movie_id_list=movie_id_list)
    chunked_movie_id_list.set_upstream(truncate_result)

    # 映画IDをDBに保存
    load_movie_id_list.map(chunked_movie_id_list)
