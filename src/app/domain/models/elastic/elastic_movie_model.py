from elasticsearch_dsl import Document, Text, analyzer, connections, tokenizer
from elasticsearch_dsl.field import Double, Integer, Keyword, Long

trigram_analyzer = analyzer(
    "trigram_analyzer",
    type="custom",
    tokenizer=tokenizer(
        "trigram",
        "nGram",
        min_gram=2,
        max_gram=3
    ),
    filter=[
        "lowercase"
    ]
)


class ElasticMovieModel(Document):
    movie_id = Keyword(required=True)
    free_word = Text(analyzer=trigram_analyzer)
    original_title = Keyword()
    japanese_title = Keyword()
    overview = Keyword()
    tagline = Keyword()
    poster_path = Keyword()
    backdrop_path = Keyword()
    popularity = Double()
    release_date = Keyword()
    release_year = Integer()
    genres = Integer(multi=True)
    genre_labels = Keyword(multi=True)
    keywords = Integer(multi=True)
    keyword_labels = Keyword(multi=True)
    index_time = Long()

    class Index:
        name = "movie"


# TODO メソッド名変える
def init():
    # ホストを環境変数に
    connections.create_connection(hosts=["localhost"])
    if not connections.get_connection().indices.exists(index="movie"):
        ElasticMovieModel.init()


def refresh_index():
    connections.create_connection(hosts=["localhost"])
    connections.get_connection().indices.refresh()
