from typing import List

from domain.enums.movie_enums import MovieLanguage
from domain.models.rest.tmdb_model import TmdbMovieGenre
from prefect import Flow, task


@task
def fetch_genre_master(language: MovieLanguage) -> List[TmdbMovieGenre]:
    print("fetch_genre_master")
    return []


@task
def truncate_genre_master() -> None:
    print("truncate_genre_master")


@task()
def update_genre_master(
    japanese_genres: List[TmdbMovieGenre],
    english_genres: List[TmdbMovieGenre]
) -> None:
    print("update_genre_master")


with Flow("Update Genre Master") as flow:
    japanese_genres = fetch_genre_master(MovieLanguage.JP)
    english_genres = fetch_genre_master(MovieLanguage.EN)
    truncate_genre_master()
    result = update_genre_master(japanese_genres, english_genres)
    result.set_upstream(truncate_genre_master)
