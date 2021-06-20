import pytest
from app.domain.models.elastic.elastic_movie_model import (ElasticMovieModel,
                                                           init,
                                                           trigram_analyzer)


@pytest.mark.skip
def test_save_and_get_same_movie():

    init()

    # テストデータ
    test_id = 1
    movie = ElasticMovieModel(meta={"id": test_id}, **{
        "movie_id": "test"
    })
    movie.save()

    assert movie.to_dict() == ElasticMovieModel.get(id=test_id).to_dict()


@pytest.mark.skip
def test_trigram_analyser_properly_tokenize():

    response = trigram_analyzer.simulate("Hello")

    actual = [t.token for t in response.tokens]
    expected = ["he", "el", "ll", "lo", "hel", "ell", "llo"]

    assert sorted(actual) == sorted(expected)
