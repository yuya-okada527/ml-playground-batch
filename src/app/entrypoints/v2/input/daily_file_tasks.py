from datetime import date
from typing import Tuple

from prefect import Flow, task
from prefect.core.task import Parameter


@task
def fetch_daily_file(target_date: date) -> Tuple[str, str]:
    target_date = target_date or date.today()
    print(f"fetch_daily_file: {target_date}")
    return "", ""

@task
def truncate_movie_ids() -> None:
    print("truncate_movie_ids")


with Flow("Daily File") as flow:
    target_date = Parameter("target_date", default=None)
    bucket, object_key = fetch_daily_file(target_date=target_date)
    truncate_movie_ids()
