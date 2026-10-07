import unittest

from backend.analysis import analyze_books


class AnalyzeBooksTests(unittest.TestCase):
    def test_scores_tags_and_categories_into_a_type(self):
        result = analyze_books([
            {"title": "星际漫游", "categories": ["科幻"], "tags": ["宇宙", "幻想"]},
            {"title": "逻辑之美", "categories": ["数学"], "tags": ["编程"]},
        ])

        self.assertEqual(result["type"], "INTP")
        self.assertEqual(result["book_count"], 2)
        self.assertTrue(result["evidence"])

    def test_empty_library_returns_neutral_percentages_and_valid_type(self):
        result = analyze_books([])

        self.assertEqual(result["type"], "INFP")
        self.assertEqual([axis["left_percent"] for axis in result["axes"]], [50, 50, 50, 50])
        self.assertEqual(result["signal_count"], 0)

    def test_string_categories_and_tags_are_supported(self):
        result = analyze_books([{"categories": "历史,纪实", "tags": "旅行"}])

        self.assertEqual(result["book_count"], 1)
        self.assertEqual(result["label_count"], 3)


if __name__ == "__main__":
    unittest.main()