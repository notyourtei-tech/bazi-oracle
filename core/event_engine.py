# core/event_engine.py
# 流年 → 事件映射引擎（V1）

GAN_WUXING = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water"
}

# 十神关系（以日主为中心）
TEN_GOD = {
    "same": "比劫",
    "sheng_me": "印",
    "ke_me": "官杀",
    "me_ke": "财",
    "me_sheng": "食伤"
}

# 五行关系
SHENG = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood"
}

KE = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood"
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
    return "未知"


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
    if ten_god in ["官杀", "印"]:
        career = "事业压力增加，但有责任、考试、升迁机会"
    elif ten_god == "食伤":
        career = "表现欲增强，适合输出、创作、技术提升"
    elif ten_god == "比劫":
        career = "竞争加剧，易与同事产生摩擦"
    else:
        career = "事业变化不大，以积累为主"

    # === 财运 ===
    if ten_god == "财":
        wealth = "有赚钱机会，但伴随风险，需理性决策"
    elif ten_god == "比劫":
        wealth = "破财概率上升，注意借贷、人情支出"
    else:
        wealth = "财运平稳，重在规划"

    # === 感情 / 人际 ===
    if ten_god in ["比劫", "食伤"]:
        relationship = "情绪外放，易起争执，需注意沟通"
    elif ten_god in ["印", "官杀"]:
        relationship = "关系偏理性，可能因现实问题拉开距离"
    else:
        relationship = "感情状态稳定"

    # === 健康 ===
    if liu_wx not in yongshen:
        health = "五行失衡，注意对应脏腑与作息"
    else:
        health = "整体状态尚可，保持规律即可"

    return {
        "ten_god": ten_god,
        "career": career,
        "wealth": wealth,
        "relationship": relationship,
        "health": health
    }
