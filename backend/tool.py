"""从藏书看MBTI：只读书库分类与标签的 MyBooks 外置工具。"""
from webserver.handlers.base import BaseHandler, auth, js
from webserver.services import AsyncService
from webserver.toolbox.base_tool import BaseTool

from .analysis import analyze_books


class MBTITester(BaseTool):
    service_item_name = "从藏书看MBTI"

    @staticmethod
    def info():
        return {
            "tool_id": "mbti_tester",
            "name": "从藏书看MBTI",
            "description": "统计书库中的分类与标签，趣味推测你的 MBTI 类型；虽属娱乐，严肃认真，一本正经；",
            "revision": "0.2.0",
            "author": "Arthas来也",
            "publish_date": "2026-10-07",
            "repo_url": "https://github.com/ArthasC/mybooks-mbti-tester",
        }

    @AsyncService.register_function
    def analyze(self):
        book_ids = list(self.api.calibre.all_book_ids())
        return analyze_books(self._read_books(book_ids))

    def _read_books(self, book_ids):
        calibre = self.api.calibre
        if hasattr(calibre, "get_field_map"):
            return self._read_books_batch(calibre, book_ids)
        return self._read_books_legacy(calibre, book_ids)

    @staticmethod
    def _read_books_batch(calibre, book_ids):
        # 新版 mybooks：按字段批量读取，不构造完整元数据
        tags = calibre.get_field_map("tags", book_ids)
        categories = calibre.get_field_map("#category", book_ids)
        for book_id in book_ids:
            yield {"tags": tags.get(book_id), "category": categories.get(book_id)}

    @staticmethod
    def _read_books_legacy(calibre, book_ids):
        # 旧版 mybooks 没有 get_field_map，只能逐本读取
        for book_id in book_ids:
            mi = calibre.get_metadata(book_id)
            yield {
                "tags": list(mi.tags or []),
                # category 是自定义列(#category)，须用 get_custom 读取，label 不带 # 前缀
                "category": calibre.get_custom(book_id, "category"),
            }


class AnalyzeHandler(BaseHandler):
    @js
    @auth
    def get(self):
        return {"err": "ok", "data": MBTITester().analyze()}
