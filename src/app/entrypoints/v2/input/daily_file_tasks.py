from datetime import date
from typing import List

from domain.models.internal.movie_model import MovieId
from infra.repository.object_storage.object_model import ObjectKey
from prefect import Flow, task
from prefect.core.task import Parameter


@task
def extract_daily_file(target_date: date) -> ObjectKey:
    target_date = target_date or date.today()
    print(f"extract_daily_file: {target_date}")
    return ObjectKey("", "")


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
def chunck_movie_id_list(movie_id_list: List[MovieId], chunk_size: int) -> List[List[MovieId]]:
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
    movie_id_list = make_movie_ids(daily_file_key, max_id_size)

    # 映画IDをチャンク化
    chunk_size = Parameter("chunk_size", default=100)
    chunked_movie_id_list = chunck_movie_id_list(movie_id_list, chunk_size)
    chunked_movie_id_list.set_upstream(truncate_result)

    # 映画IDをDBに保存
    chunked_movie_id_list.map(load_movie_id_list)
