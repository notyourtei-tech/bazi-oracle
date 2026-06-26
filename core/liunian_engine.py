# core/dayun_liunian_engine.py
from __future__ import annotations
from core.constants import GAN_WUXING, ZHI_WUXING, SHENG as GENERATES, KE as CONTROLS


def analyze_liunian(year: int, gz: str, day_master_wx: str, yongshen: str | None = None):
    """
    返回【流年四象限】分析结果
    - year: 年份
    - gz: 流年干支（如 乙巳）
    - day_master_wx: 日主五行（wood/fire/earth/metal/water）
    - yongshen: 用神五行（可选）
    """

    gan = gz[0]
    zhi = gz[1]

    gan_wx = GAN_WUXING.get(gan)
    zhi_wx = ZHI_WUXING.get(zhi)

    # ===== 事业 =====
    if gan_wx == day_master_wx:
        career = "liunian_career_same"
    elif GENERATES.get(day_master_wx) == gan_wx:
        career = "liunian_career_sheng"
    elif CONTROLS.get(gan_wx) == day_master_wx:
        career = "liunian_career_ke"
    else:
        career = "liunian_career_other"

    # ===== 财运 =====
    if gan_wx == CONTROLS.get(day_master_wx):
        wealth = "liunian_wealth_be_ke"
    elif gan_wx == GENERATES.get(day_master_wx):
        wealth = "liunian_wealth_sheng"
    else:
        wealth = "liunian_wealth_other"

    # ===== 感情 =====
    if zhi_wx == day_master_wx:
        relationship = "liunian_relationship_same"
    elif GENERATES.get(zhi_wx) == day_master_wx:
        relationship = "liunian_relationship_sheng"
    else:
        relationship = "liunian_relationship_other"

    # ===== 健康 =====
    if CONTROLS.get(zhi_wx) == day_master_wx:
        health = "liunian_health_ke"
    elif zhi_wx == day_master_wx:
        health = "liunian_health_same"
    else:
        health = "liunian_health_other"

    return {
        "year": year,
        "gz": gz,
        "career": career,
        "wealth": wealth,
        "relationship": relationship,
        "health": health
    }
