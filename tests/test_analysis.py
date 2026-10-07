import unittest

from backend.analysis import AXES, analyze_books


class AnalyzeBooksTests(unittest.TestCase):
    def test_category_and_tag_keywords_vote_once_per_book(self):
        result = analyze_books([
            {
                "categories": ["科幻", "科幻"],
                "tags": ["科幻", "未来", "计划", "效率"],
            },
            {"category": "历史", "tag": ["历史", "传记"]},
            {"tags": ["爱情", "治愈", "家庭"]},
            {"tags": ["推理", "侦探"]},
        ])

        self.assertEqual(result["book_count"], 4)
        self.assertEqual(result["books_with_clues"], 4)
        self.assertEqual(result["type"], "XXXJ")
        self.assertEqual(result["category_count"], 2)
        self.assertEqual(result["tag_count"], 11)
        self.assertEqual(result["dimensions"][1]["right_count"], 1)
        self.assertEqual(result["dimensions"][1]["left_count"], 1)
        self.assertEqual(result["dimensions"][1]["selected"], "X")
        self.assertEqual(result["dimensions"][3]["left_count"], 1)
        self.assertEqual(result["dimensions"][3]["right_count"], 0)

    def test_no_books_has_no_personality_result(self):
        result = analyze_books([])

        self.assertEqual(result["book_count"], 0)
        self.assertIsNone(result["type"])
        self.assertIsNone(result["type_name"])

    def test_unrecognized_tags_are_reported_as_low_confidence(self):
        result = analyze_books([{"categories": ["其他"], "tags": ["暂未归类"]}])

        self.assertEqual(result["books_with_clues"], 1)
        self.assertEqual(result["type"], "XXXX")
        self.assertEqual(result["type_name"], "迷雾中的藏书人")
        self.assertEqual(result["undecided"], ["EI", "SN", "TF", "JP"])
        self.assertTrue(all(item["tie"] for item in result["dimensions"]))
        self.assertEqual(result["confidence"], "样本太少，纯属书库玄学")
        self.assertEqual(result["dimensions"][0]["left_percent"], 50)
        self.assertEqual(result["dimensions"][0]["right_percent"], 50)

    def test_string_values_and_english_terms_are_supported(self):
        result = analyze_books([
            {"categories": "fantasy, adventure", "tags": "travel, fiction"},
        ])

        self.assertEqual(result["type"], "XNXP")
        self.assertEqual(result["top_categories"][0]["name"], "fantasy")
        self.assertEqual(result["top_tags"][0]["name"], "travel")

    def test_tied_axis_is_undecided_instead_of_defaulting_right(self):
        result = analyze_books([{"tags": ["科幻"]}])

        self.assertEqual(result["dimensions"][1]["tie"], False)
        self.assertEqual(result["dimensions"][0]["selected"], "X")
        self.assertEqual(result["dimensions"][0]["tie"], True)
        self.assertTrue(result["type"].startswith("X"))

    def test_terms_are_unique_across_all_axes(self):
        terms = [
            term.lower()
            for axis in AXES
            for side in ("left_terms", "right_terms")
            for term in axis[side]
        ]
        duplicated = {term for term in terms if terms.count(term) > 1}

        self.assertEqual(duplicated, set())

    def test_english_terms_match_whole_words_only(self):
        result = analyze_books([{"tags": ["party planning", "glove", "martial arts"]}])

        evidence = {
            item["name"]
            for dimension in result["dimensions"]
            for side in dimension["evidence"].values()
            for item in side
        }
        self.assertIn("party", evidence)
        self.assertNotIn("love", evidence)
        self.assertNotIn("art", evidence)

    def test_longer_term_swallows_contained_shorter_terms(self):
        result = analyze_books([{"tags": ["Science Fiction"]}])

        self.assertEqual(result["dimensions"][1]["right_count"], 1)
        self.assertEqual(result["dimensions"][2]["left_count"], 0)
        self.assertEqual(result["dimensions"][3]["right_count"], 0)


if __name__ == "__main__":
    unittest.main()
