from typing import List

from domain.enums.movie_enums import MovieLanguage
from domain.models.internal.movie_model import Movie, MovieId, Review
from infra.client.tmdb.tmdb_api import init_tmdb_client
from infra.repository.input.movie_id_repository import init_movie_id_repository
from infra.repository.input.movie_repository import init_movie_repository
from infra.repository.input.review_repository import init_review_repository
from prefect import Flow, task
from service.logic.input_logic import map_review_model


@task
def truncate_movie_details() -> None:
    movie_repository = init_movie_repository()
    movie_repository.truncate_movies()


@task
def truncate_movie_reviews() -> None:
    review_repository = init_review_repository()
    review_repository.truncate_reviews()


@task
def extract_movie_ids() -> List[MovieId]:
    movie_id_repository = init_movie_id_repository()
    return movie_id_repository.fetch_all()


@task
def extract_movie_detail(movie_id: MovieId) -> Movie:
    tmdb_client = init_tmdb_client()
    return tmdb_client.fetch_movie_detail(
        movie_id=movie_id.tmdb_id,
        language=MovieLanguage.JP
    ).to_internal_movie(movie_id.movie_id)


@task
def load_movie_details(movies: List[Movie]) -> None:
    movie_repository = init_movie_repository()
    movie_repository.save_movie_list(movies)


@task
def extract_movie_review(movie_id: MovieId) -> List[Review]:
    tmdb_client = init_tmdb_client()
    movie_review_response = tmdb_client.fetch_movie_reviews(movie_id=movie_id.tmdb_id)
    return [
        map_review_model(review, movie_id)
        for review in movie_review_response.results
    ]


@task
def load_movie_reviews(review_list: List[Review]) -> None:
    review_repository = init_review_repository()
    review_repository.save_review_list(review_list=review_list)


with Flow("Detail Movie Tasks") as flow:
    # データを削除
    truncate_movies_task = truncate_movie_details()
    truncate_reviews_task = truncate_movie_reviews()

    # 映画IDを取得
    movie_ids = extract_movie_ids()

    # 映画詳細を取得
    movies = extract_movie_detail.map(movie_id=movie_ids)
    load_movies_task = load_movie_details(movies)
    load_movies_task.set_upstream(truncate_movies_task)

    # 映画レビューを取得
    movie_reviews = extract_movie_review.map(movie_id=movie_ids)
    load_reviews_task = load_movie_reviews.map(review_list=movie_reviews)
    load_reviews_task.set_upstream(truncate_reviews_task)
