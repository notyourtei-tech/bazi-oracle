# core/event_engine.py
# 流年 → 事件映射引擎（V1）
from core.constants import GAN_WUXING, SHENG, KE

# 十神关系（以日主为中心）
TEN_GOD = {
    "same": "比劫",
    "sheng_me": "印",
    "ke_me": "官杀",
    "me_ke": "财",
    "me_sheng": "食伤"
}


def _ten_god(day_wx: str, liunian_wx: str) -> str:
    if day_wx == liunian_wx:
        return TEN_GOD["same"]
    if SHENG[liunian_wx] == day_wx:
        return TEN_GOD["sheng_me"]
    if KE[liunian_wx] == day_wx:
        return TEN_GOD["ke_me"]
    if SHENG[day_wx] == liunian_wx:
        return TEN_GOD["me_sheng"]
    if KE[day_wx] == liunian_wx:
        return TEN_GOD["me_ke"]
    return "ten_god_unknown"


def map_liunian_event(
    bazi: dict,
    liunian: dict,
    strength_info: dict,
    yongshen_info: dict
) -> dict:
    """
    输入：
      - bazi: 八字
      - liunian: {"year": 2026, "gan": "丙", "zhi": "午"}（示例）
      - strength_info
      - yongshen_info

    输出：
      career / wealth / relationship / health
    """

    day_gan = bazi["day"][0]
    day_wx = GAN_WUXING.get(day_gan)

    liu_gan = liunian.get("gan")
    liu_wx = GAN_WUXING.get(liu_gan)
    if liu_wx is None:
        liu_wx = 'earth'

    ten_god = _ten_god(day_wx, liu_wx)
    strength = strength_info.get("strength")

    yongshen = yongshen_info.get("yongshen", [])

    # === 事业 ===
    career_risk = False
    if ten_god in ["官杀", "印"]:
        career = "event_career_guansha"
        career_risk = True
    elif ten_god == "食伤":
        career = "event_career_food"
    elif ten_god == "比劫":
        career = "event_career_bijian"
        career_risk = True
    else:
        career = "event_career_default"

    # === 财运 ===
    wealth_risk = False
    if ten_god == "财":
        wealth = "event_wealth_cai"
        wealth_risk = True
    elif ten_god == "比劫":
        wealth = "event_wealth_bijian"
        wealth_risk = True
    else:
        wealth = "event_wealth_default"

    # === 感情 / 人际 ===
    relationship_risk = False
    if ten_god in ["比劫", "食伤"]:
        relationship = "event_relationship_bijian"
        relationship_risk = True
    elif ten_god in ["印", "官杀"]:
        relationship = "event_relationship_guansha"
    else:
        relationship = "event_relationship_default"

    # === 健康 ===
    health_risk = False
    if yongshen and liu_wx not in yongshen:
        health = "event_health_imbalance"
        health_risk = True
    else:
        health = "event_health_default"

    risk_tags = {
        "career": career_risk,
        "wealth": wealth_risk,
        "relationship": relationship_risk,
        "health": health_risk,
        "yongshen": bool(yongshen) and not any(wx in yongshen for wx in ["water", "metal", "wood", "fire", "earth"])
    }

    return {
        "ten_god": ten_god,
        "career": career,
        "wealth": wealth,
        "relationship": relationship,
        "health": health,
        "risk_tags": risk_tags
    }
