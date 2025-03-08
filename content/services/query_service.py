from content.models.article_query import ArticleDocument


class QueryService:
    @staticmethod
    def search_articles(query):
        return ArticleDocument.search().query("multi_match", query=query, fields=["title", "content"]).execute()
