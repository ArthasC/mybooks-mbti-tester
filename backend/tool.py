from webserver.handlers.base import BaseHandler, auth, js
from webserver.services import AsyncService
from webserver.toolbox.base_tool import BaseTool

from .analysis import analyze_books


class BooksMBTI(BaseTool):
    @staticmethod
    def info():
        return {
            "tool_id": "books_mbti",
            "name": "从藏书看MBTI",
            "description": "根据书库中的分类与标签生成一份娱乐向的MBTI藏书画像",
            "revision": "0.1.0",
            "author": "Arthas来了",
            "publish_date": "2026-10-07",
            "repo_url": "https://github.com/ArthasC/mybooks-mbti-tester",
        }

    @AsyncService.register_function
    def analyze(self):
        books = []
        for book_id in self.api.calibre.all_book_ids():
            metadata = self.api.calibre.get_metadata(book_id)
            categories = metadata.get("#category", [])
            if not categories:
                categories = metadata.get("#categories", metadata.get("category", []))
            books.append({
                "title": metadata.title,
                "categories": categories,
                "tags": metadata.tags or [],
            })
        return analyze_books(books)


class AnalysisHandler(BaseHandler):
    @js
    @auth
    def get(self):
        return {"err": "ok", "data": BooksMBTI().analyze()}