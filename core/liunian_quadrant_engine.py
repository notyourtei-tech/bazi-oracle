# core/liunian_quadrant_engine.py

GAN_WX = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water",
}

# 生克关系
SHENG = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood",
}
KE = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood",
}


def _level_from_relation(relation: str):
    """
    把关系映射成 UI 可用等级
    """
    if relation == "same":
        return "good"
    if relation == "sheng":
        return "good"
    if relation == "ke":
        return "attention"
    if relation == "be_ke":
        return "caution"
    return "normal"


def analyze_quadrants(
    *,
    rizhu_wx: str,
    year_gan: str,
    year_risk: str
):
    """
    核心四象限分析
    """
    year_wx = GAN_WX.get(year_gan, "earth")

    # 判断关系
    if year_wx == rizhu_wx:
        relation = "same"
    elif SHENG.get(rizhu_wx) == year_wx:
        relation = "sheng"
    elif KE.get(rizhu_wx) == year_wx:
        relation = "ke"
    elif KE.get(year_wx) == rizhu_wx:
        relation = "be_ke"
    else:
        relation = "other"

    level = _level_from_relation(relation)

    # 事业
    career = {
        "level": level,
        "text": (
            "事业层面有推动力，适合主动争取机会。"
            if level == "good"
            else "工作中需保持稳定，避免与权威产生冲突。"
            if level in ("attention", "caution")
            else "事业节奏相对平稳，重在执行。"
        )
    }

    # 财运
    wealth = {
        "level": "normal" if year_risk != "low" else "good",
        "text": (
            "财务上有改善空间，但不宜激进投资。"
            if year_risk == "low"
            else "财务波动较明显，建议以保守策略为主。"
        )
    }

    # 感情
    love = {
        "level": "caution" if relation in ("be_ke", "ke") else "normal",
        "text": (
            "感情中易出现立场分歧，沟通尤为重要。"
            if relation in ("be_ke", "ke")
            else "情感状态较为平稳，适合深化关系。"
        )
    }

    # 健康
    health = {
        "level": "attention" if year_risk == "high" else "normal",
        "text": (
            "需注意作息与压力管理，避免过度消耗。"
            if year_risk == "high"
            else "健康整体平稳，保持规律即可。"
        )
    }

    return {
        "career": career,
        "wealth": wealth,
        "love": love,
        "health": health
    }
