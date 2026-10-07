"""根据书籍分类与标签生成娱乐性质的 MBTI 推测。"""
import re
from collections import Counter
from functools import lru_cache


AXES = (
    {
        "left": "E",
        "right": "I",
        "left_name": "外向能量",
        "right_name": "内向能量",
        "left_terms": (
            "社交", "群像", "对话", "友情", "恋爱", "校园", "校园文学", "职场",
            "喜剧", "言情", "群体", "派对", "聚会", "幽默", "搞笑", "热闹",
            "综艺", "访谈", "演讲", "口才", "人际", "沟通", "社群", "团队",
            "合作", "青春", "都市", "情景喜剧", "social", "friendship",
            "dialogue", "comedy", "humor", "party", "interview", "speech",
            "communication", "teamwork", "community", "youth", "urban",
            "sitcom",
        ),
        "right_terms": (
            "独处", "内心", "心理", "心理学", "冥想", "哲学", "散文", "诗歌",
            "孤独", "自我", "意识", "意识流", "沉思", "个人成长", "隐居",
            "日记", "书信", "回忆录", "自省", "内省", "独白", "禅", "宗教",
            "神学", "存在主义", "隐士", "极简", "哲思", "随笔", "introspection",
            "philosophy", "poetry", "solitude", "psychology", "meditation",
            "diary", "memoir", "essay", "existentialism", "zen",
            "spirituality", "religion", "mindfulness",
        ),
    },
    {
        "left": "S",
        "right": "N",
        "left_name": "现实观察",
        "right_name": "想象雷达",
        "left_terms": (
            "历史", "传记", "纪实", "科普", "手册", "烹饪", "生活", "医学",
            "教育", "法律", "现实", "自然", "地理", "百科", "农业", "建筑",
            "体育", "健身", "健康", "养生", "园艺", "手工", "家居", "育儿",
            "汽车", "新闻", "报告文学", "工具书", "词典", "字典", "考古",
            "美食", "食谱", "biography", "history", "cooking", "cookbook",
            "nature", "geography", "encyclopedia", "reference", "health",
            "fitness", "gardening", "crafts", "parenting", "news",
            "documentary", "realism", "medicine", "education", "law",
        ),
        "right_terms": (
            "科幻", "奇幻", "魔法", "未来", "宇宙", "幻想", "神话", "超自然",
            "架空", "思想", "象征", "创意", "玄幻", "仙侠", "修仙", "穿越",
            "重生", "末世", "赛博朋克", "太空", "外星", "异世界", "寓言",
            "预言", "梦境", "隐喻", "超现实", "乌托邦", "灵异", "志怪",
            "science fiction", "fantasy", "magic", "mythology", "future",
            "imagination", "speculative", "cyberpunk", "dystopia", "utopia",
            "supernatural", "surreal", "legend", "folklore", "paranormal",
            "space", "alien",
        ),
    },
    {
        "left": "T",
        "right": "F",
        "left_name": "逻辑分析",
        "right_name": "情感共鸣",
        "left_terms": (
            "逻辑", "推理", "侦探", "科学", "数学", "编程", "技术", "经济",
            "管理", "战略", "军事", "犯罪", "悬疑", "谍战", "金融", "投资",
            "商业", "统计", "物理", "化学", "工程", "算法", "计算机",
            "人工智能", "法医", "刑侦", "兵法", "博弈", "论证", "辩论",
            "logic", "detective", "mystery", "mathematics", "programming",
            "business", "strategy", "science", "technology", "management",
            "finance", "investment", "statistics", "physics", "chemistry",
            "engineering", "algorithm", "computer", "thriller", "crime",
            "military",
        ),
        "right_terms": (
            "爱情", "情感", "亲情", "治愈", "温暖", "女性", "家庭", "童话",
            "心灵", "浪漫", "情绪", "成长小说", "暖心", "感动", "催泪", "虐心",
            "陪伴", "婚姻", "母爱", "共情", "公益", "人文", "关怀", "疗愈",
            "纯爱", "耽美", "百合", "日常", "love", "healing", "family",
            "romance", "fairy tale", "emotional", "heartwarming", "empathy",
            "marriage", "humanities",
        ),
    },
    {
        "left": "J",
        "right": "P",
        "left_name": "计划收纳",
        "right_name": "即兴探索",
        "left_terms": (
            "计划", "效率", "习惯", "方法", "教程", "指南", "整理", "目标",
            "工作", "学习", "规划", "时间管理", "项目管理", "清单", "自律",
            "职业规划", "考试", "备考", "教材", "教辅", "习题", "规范", "流程",
            "复盘", "收纳", "productivity", "organization", "planning",
            "how-to", "guide", "career", "textbook", "exam", "study",
            "checklist", "habit", "goal",
        ),
        "right_terms": (
            "冒险", "旅行", "短篇", "艺术", "漫画", "游戏", "实验", "即兴",
            "游记", "旅游", "流浪", "公路", "探险", "武侠", "轻小说", "绘本",
            "插画", "摄影", "音乐", "电影", "动漫", "同人", "脑洞", "设计",
            "涂鸦", "adventure", "travel", "comics", "games", "art",
            "creative", "improv", "anime", "manga", "music", "film",
            "design", "photography", "roadtrip",
        ),
    },
)

TIE_LETTER = "X"  # 该维度左右票数相同（含 0:0），无法判断
UNDECIDED_NAME = "迷雾中的藏书人"

TYPE_NAMES = {
    "ISTJ": "藏书楼总管",
    "ISFJ": "温柔守书人",
    "INFJ": "深夜预言家",
    "INTJ": "书单总策划",
    "ISTP": "拆书实验员",
    "ISFP": "美学收藏家",
    "INFP": "脑内造梦师",
    "INTP": "思想考古学家",
    "ESTP": "冒险开卷王",
    "ESFP": "氛围组主理人",
    "ENFP": "灵感烟花制造机",
    "ENTP": "观点辩论赛冠军",
    "ESTJ": "进度条管理员",
    "ESFJ": "书友会团宠",
    "ENFJ": "共读活动召集人",
    "ENTJ": "阅读项目总指挥",
}


def _values(value):
    if value is None:
        return []
    if isinstance(value, str):
        parts = value.replace("，", ",").split(",")
        return [part.strip() for part in parts if part.strip()]
    if isinstance(value, dict):
        return [str(item).strip() for item in value.values() if item]
    try:
        return [str(item).strip() for item in value if item]
    except TypeError:
        return [str(value).strip()]


def _term_pattern(term):
    """英文词按单词边界匹配，避免 art 命中 party、love 命中 glove；中文直接子串匹配。"""
    term = term.lower()
    if term.isascii():
        return re.compile(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])")
    return re.compile(re.escape(term))


_TERM_INDEX = tuple(
    (_term_pattern(term), term, index, side)
    for index, axis in enumerate(AXES)
    for side in ("left", "right")
    for term in axis[f"{side}_terms"]
)


@lru_cache(maxsize=None)  # 标签在书库中大量重复，缓存后每个不同线索只匹配一次
def _match_clue(clue):
    """返回单条线索命中的 (词, 维度序号, 侧)；被更长命中词包含的短词会被丢弃。"""
    hits = [
        (term, index, side)
        for pattern, term, index, side in _TERM_INDEX
        if pattern.search(clue)
    ]
    return tuple(
        hit for hit in hits
        if not any(hit[0] != other[0] and hit[0] in other[0] for other in hits)
    )


def _book_values(book, names):
    values = []
    for name in names:
        values.extend(_values(book.get(name)))
    return list(dict.fromkeys(value for value in values if value))


def analyze_books(books):
    """汇总分类和标签，按每本书每条维度最多一票推测四字母类型。"""
    category_counts = Counter()
    tag_counts = Counter()
    axis_counts = [{"left": 0, "right": 0} for _ in AXES]
    axis_evidence = [{"left": Counter(), "right": Counter()} for _ in AXES]
    books_with_clues = 0
    book_count = 0

    for book in books:
        book_count += 1
        categories = _book_values(book, ("categories", "category"))
        tags = _book_values(book, ("tags", "tag"))
        category_counts.update(categories)
        tag_counts.update(tags)
        clues = [value.lower() for value in categories + tags]
        if clues:
            books_with_clues += 1

        matches = [{"left": set(), "right": set()} for _ in AXES]
        for clue in clues:
            for term, index, side in _match_clue(clue):
                matches[index][side].add(term)

        for index in range(len(AXES)):
            left, right = matches[index]["left"], matches[index]["right"]
            if len(left) > len(right):
                winner = "left"
            elif len(right) > len(left):
                winner = "right"
            else:
                continue
            axis_counts[index][winner] += 1
            axis_evidence[index][winner].update(matches[index][winner])

    letters = []
    dimensions = []
    for index, axis in enumerate(AXES):
        counts = axis_counts[index]
        if counts["left"] == counts["right"]:
            letter = TIE_LETTER
        else:
            letter = axis["left"] if counts["left"] > counts["right"] else axis["right"]
        letters.append(letter)
        total = counts["left"] + counts["right"]
        dimensions.append(
            {
                "left": axis["left"],
                "right": axis["right"],
                "left_name": axis["left_name"],
                "right_name": axis["right_name"],
                "left_count": counts["left"],
                "right_count": counts["right"],
                "left_percent": (
                    round(counts["left"] * 100 / total) if total else 50
                ),
                "right_percent": (
                    round(counts["right"] * 100 / total) if total else 50
                ),
                "selected": letter,
                "tie": letter == TIE_LETTER,
                "evidence": {
                    side: [
                        {"name": name, "count": count}
                        for name, count in axis_evidence[index][side].most_common(4)
                    ]
                    for side in ("left", "right")
                },
            }
        )

    mbti = "".join(letters)
    eligible = sum(
        counts["left"] + counts["right"] for counts in axis_counts
    )
    confidence = (
        "书库证词很充分" if books_with_clues >= 40 and eligible >= 40
        else "线索不少，姑且当真" if books_with_clues >= 12 and eligible >= 12
        else "样本太少，纯属书库玄学"
    )

    return {
        "book_count": book_count,
        "books_with_clues": books_with_clues,
        "category_count": len(category_counts),
        "tag_count": len(tag_counts),
        "top_categories": [
            {"name": name, "count": count}
            for name, count in category_counts.most_common(6)
        ],
        "top_tags": [
            {"name": name, "count": count}
            for name, count in tag_counts.most_common(8)
        ],
        "type": mbti if book_count else None,
        "type_name": TYPE_NAMES.get(mbti, UNDECIDED_NAME) if book_count else None,
        "undecided": [d["left"] + d["right"] for d in dimensions if d["tie"]],
        "confidence": confidence,
        "dimensions": dimensions,
    }
