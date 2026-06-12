# core/dayun_liunian_engine.py

# 五行映射（简化专业版）
GAN_WUXING = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water"
}

ZHI_WUXING = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water"
}

# 简化的五行生克关系
GENERATES = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood"
}

CONTROLS = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood"
}


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
        career = "事业压力较为集中，容易承担更多责任，宜稳扎稳打，避免频繁变动。"
    elif GENERATES.get(day_master_wx) == gan_wx:
        career = "事业上有发挥空间，适合主动争取机会，利于展示能力。"
    elif CONTROLS.get(gan_wx) == day_master_wx:
        career = "事业中可能遇到外部约束或挑战，需注意人际与规则问题。"
    else:
        career = "事业运势较为平稳，适合积累经验，不宜激进决策。"

    # ===== 财运 =====
    if gan_wx == CONTROLS.get(day_master_wx):
        wealth = "财运波动较大，容易有支出增加的情况，应注意风险控制。"
    elif gan_wx == GENERATES.get(day_master_wx):
        wealth = "财运有增长机会，适合正财积累，但仍需量入为出。"
    else:
        wealth = "财运整体平稳，不宜进行高风险投资。"

    # ===== 感情 =====
    if zhi_wx == day_master_wx:
        relationship = "感情事务容易成为关注重点，需避免情绪化沟通。"
    elif GENERATES.get(zhi_wx) == day_master_wx:
        relationship = "人际关系较为顺畅，有助于增进感情与合作。"
    else:
        relationship = "感情状态相对平稳，重在维持现有关系的平衡。"

    # ===== 健康 =====
    if CONTROLS.get(zhi_wx) == day_master_wx:
        health = "健康方面需注意劳累与压力问题，保持规律作息尤为重要。"
    elif zhi_wx == day_master_wx:
        health = "精力消耗较大，需注意休息与身体调养。"
    else:
        health = "健康状况总体稳定，注意日常保养即可。"

    return {
        "year": year,
        "gz": gz,
        "career": career,
        "wealth": wealth,
        "relationship": relationship,
        "health": health
    }
