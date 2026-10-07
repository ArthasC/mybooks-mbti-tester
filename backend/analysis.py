from collections import Counter


TRAITS = (
    ("E", "I", "外向", "内向"),
    ("S", "N", "实感", "直觉"),
    ("T", "F", "思考", "情感"),
    ("J", "P", "判断", "感知"),
)

KEYWORDS = {
    "E": ("社交", "沟通", "演讲", "团队", "旅行", "冒险", "派对", "职场", "营销", "领导"),
    "I": ("心理", "哲学", "冥想", "独处", "日记", "内心", "思考", "文学", "诗歌", "自我"),
    "S": ("历史", "传记", "科普", "科学", "医学", "教程", "烹饪", "摄影", "自然", "纪实"),
    "N": ("科幻", "奇幻", "幻想", "悬疑", "推理", "未来", "宇宙", "魔法", "创意", "神话"),
    "T": ("逻辑", "编程", "数学", "商业", "经济", "战略", "管理", "技术", "数据", "法律"),
    "F": ("爱情", "情感", "家庭", "治愈", "成长", "友情", "心理", "小说", "人际", "温暖"),
    "J": ("计划", "效率", "方法", "管理", "清单", "目标", "习惯", "教程", "整理", "时间"),
    "P": ("旅行", "冒险", "随笔", "创意", "艺术", "即兴", "幻想", "小说", "探索", "漫画"),
}

TRAIT_COPY = {
    "E": "社交电量看起来相当充足，连书架都像在邀请人来串门。",
    "I": "你的书架像一间安静的秘密基地，独处不是退场，是主场。",
    "S": "你偏爱摸得着的细节与可靠的知识，现实世界被你读得明明白白。",
    "N": "想象力已经从书页出逃，下一站大概是平行宇宙。",
    "T": "逻辑先别急着下班，你连选书都像在做一场漂亮的论证。",
    "F": "共情雷达常开，书里角色的心事可能都被你认真接住了。",
    "J": "你的阅读宇宙隐约有张路线图，连灵感都排好了队。",
    "P": "书单像一扇扇没关上的门，今天想去哪一页就去哪一页。",
}


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]
    try:
        return [str(part).strip() for part in value if str(part).strip()]
    except TypeError:
        return [str(value).strip()]


def analyze_books(books):
    scores = Counter()
    evidence = Counter()
    analyzed_books = []
    total_labels = 0

    for book in books:
        labels = list(dict.fromkeys(_as_list(book.get("categories")) + _as_list(book.get("tags"))))
        total_labels += len(labels)
        book_traits = set()
        for label in labels:
            lowered = label.lower()
            for trait, keywords in KEYWORDS.items():
                if any(keyword in lowered for keyword in keywords):
                    scores[trait] += 1
                    evidence[label] += 1
                    book_traits.add(trait)
        if book_traits:
            analyzed_books.append({"title": book.get("title") or "无题之书", "traits": sorted(book_traits)})

    axes = []
    letters = []
    for positive, negative, positive_name, negative_name in TRAITS:
        positive_score = scores[positive]
        negative_score = scores[negative]
        total = positive_score + negative_score
        positive_percent = round(positive_score * 100 / total) if total else 50
        dominant = positive if positive_score > negative_score else negative
        letters.append(dominant)
        axes.append({
            "left": positive_name,
            "right": negative_name,
            "left_percent": positive_percent,
            "right_percent": 100 - positive_percent,
            "leaning": positive_name if dominant == positive else negative_name,
        })

    code = "".join(letters)
    archetypes = {
        "INTJ": "藏书总编", "INTP": "脑洞研究员", "ENTJ": "知识策展人", "ENTP": "灵感辩手",
        "INFJ": "故事解码师", "INFP": "浪漫收藏家", "ENFJ": "共鸣放映机", "ENFP": "奇想漫游者",
        "ISTJ": "书单工程师", "ISFJ": "温柔守卷人", "ESTJ": "效率馆长", "ESFJ": "人间推荐官",
        "ISTP": "冷静拆书匠", "ISFP": "感官漫游者", "ESTP": "行动派读者", "ESFP": "快乐翻页机",
    }
    return {
        "type": code,
        "archetype": archetypes[code],
        "traits": [TRAIT_COPY[letter] for letter in code],
        "axes": axes,
        "book_count": len(books),
        "signal_count": sum(scores.values()),
        "label_count": total_labels,
        "evidence": [{"label": label, "count": count} for label, count in evidence.most_common(8)],
        "books": analyzed_books[:6],
    }