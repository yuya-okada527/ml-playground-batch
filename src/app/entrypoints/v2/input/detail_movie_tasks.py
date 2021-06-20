from typing import List

from domain.enums.movie_enums import MovieLanguage
from domain.enums.similarity_enums import SimilarityModelType
from domain.models.internal.movie_model import (Movie, MovieId, Review,
                                                SimilarMovie)
from infra.client.tmdb.tmdb_api import init_tmdb_client
from infra.repository.input.movie_id_repository import init_movie_id_repository
from infra.repository.input.movie_repository import init_movie_repository
from infra.repository.input.review_repository import init_review_repository
from prefect import Flow, task
# from prefect.utilities.tasks import unmapped
from service.logic.input_logic import fetch_similar_movies, map_review_model


@task
def truncate_movie_details() -> None:
    movie_repository = init_movie_repository()
    movie_repository.truncate_movies()


@task
def truncate_movie_reviews() -> None:
    review_repository = init_review_repository()
    review_repository.truncate_reviews()


@task
def truncate_similar_movies() -> None:
    movie_repository = init_movie_repository()
    movie_repository.truncate_similar_movies()

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
def extract_similar_movie(movie_id: MovieId, registered_movie_ids: List[MovieId]) -> List[SimilarMovie]:
    tmdb_client = init_tmdb_client()
    movie_id_repository = init_movie_id_repository()
    similar_movie_tmdb_ids = fetch_similar_movies(
        movie_id=movie_id.tmdb_id,
        registered_movies_id_set={movie_id.tmdb_id for movie_id in registered_movie_ids},
        tmdb_client=tmdb_client
    )
    similar_movie_ids = movie_id_repository.fetch_by_tmdb_ids(similar_movie_tmdb_ids[:5])
    return [
        SimilarMovie(
            movie_id=movie_id,
            model_type=SimilarityModelType.TMDB_SIM,
            similar_movie_id=similar_movie_id
        )
        for similar_movie_id in similar_movie_ids
    ]


@task
def extract_movie_review(movie_id: MovieId) -> List[Review]:
    tmdb_client = init_tmdb_client()
    movie_review_response = tmdb_client.fetch_movie_reviews(movie_id=movie_id.tmdb_id)
    return [
        map_review_model(review, movie_id)
        for review in movie_review_response.results
    ]


@task
def load_movie_details(movies: List[Movie]) -> None:
    movie_repository = init_movie_repository()
    movie_repository.save_movie_list(movies)


@task
def load_movie_reviews(review_list: List[Review]) -> None:
    review_repository = init_review_repository()
    review_repository.save_review_list(review_list=review_list)


@task
def load_similar_movies(similar_movies: List[SimilarMovie]) -> None:
    movie_repository = init_movie_repository()
    movie_repository.save_similar_movie_list(similar_movies)


with Flow("Detail Movie Tasks") as flow:
    # データを削除
    truncate_movies_task = truncate_movie_details()
    truncate_reviews_task = truncate_movie_reviews()
    # truncate_similar_movies_task = truncate_similar_movies()

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

    # 類似映画を取得
    # TODO 類似映画が全然マッチしない問題。。。。
    # TODO とりあえず、ここら辺はコメントアウト
    # similar_movies = extract_similar_movie.map(movie_id=movie_ids, registered_movie_ids=unmapped(movie_ids))
    # load_similar_movies_task = load_similar_movies.map(similar_movies=similar_movies)
    # load_similar_movies_task.set_upstream(truncate_similar_movies_task)
