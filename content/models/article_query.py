from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from content.models.article import Article

article_index = Index("articles")
article_index.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@article_index.doc_type
class ArticleDocument(Document):
    """
    Elasticsearch query model for Articles.
    """

    title = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )
    content = fields.TextField(analyzer=html_strip)
    published_date = fields.DateField()
    updated_date = fields.DateField()
    review_count = fields.IntegerField()
    avg_rating = fields.FloatField()

    class Django:
        model = Article  # Connect to Django's SQL model
