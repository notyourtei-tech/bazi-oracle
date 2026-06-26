# core/liunian_quadrant_engine.py
from core.constants import GAN_WX, SHENG, KE


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
            "liunian_quad_career_good"
            if level == "good"
            else "liunian_quad_career_attention"
            if level in ("attention", "caution")
            else "liunian_quad_career_normal"
        )
    }

    # 财运
    wealth = {
        "level": "normal" if year_risk != "low" else "good",
        "text": (
            "liunian_quad_wealth_low"
            if year_risk == "low"
            else "liunian_quad_wealth_other"
        )
    }

    # 感情
    love = {
        "level": "caution" if relation in ("be_ke", "ke") else "normal",
        "text": (
            "liunian_quad_love_ke"
            if relation in ("be_ke", "ke")
            else "liunian_quad_love_normal"
        )
    }

    # 健康
    health = {
        "level": "attention" if year_risk == "high" else "normal",
        "text": (
            "liunian_quad_health_high"
            if year_risk == "high"
            else "liunian_quad_health_normal"
        )
    }

    return {
        "career": career,
        "wealth": wealth,
        "love": love,
        "health": health
    }
