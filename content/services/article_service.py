from content.models.article import Article
from content.tasks.sync_to_elasticsearch import sync_article_to_elasticsearch


class ArticleService:
    @staticmethod
    def create_article(title, content):
        article = Article.objects.create(title=title, content=content)
        sync_article_to_elasticsearch(article.id)  # Sync to Elasticsearch
        return article

    @staticmethod
    def update_article(article_id, title=None, content=None):
        article = Article.objects.get(id=article_id)
        if title:
            article.title = title
        if content:
            article.content = content
        article.save()
        sync_article_to_elasticsearch(article.id)  # Sync to Elasticsearch
        return article
