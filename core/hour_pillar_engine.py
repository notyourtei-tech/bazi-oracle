# core/hour_pillar_engine.py
from datetime import datetime, timedelta

GAN = list("甲乙丙丁戊己庚辛壬癸")
ZHI = list("子丑寅卯辰巳午未申酉戌亥")

# 时辰起点（小时）
HOUR_ZHI_RANGES = [
    ("子", 23, 1),
    ("丑", 1, 3),
    ("寅", 3, 5),
    ("卯", 5, 7),
    ("辰", 7, 9),
    ("巳", 9, 11),
    ("午", 11, 13),
    ("未", 13, 15),
    ("申", 15, 17),
    ("酉", 17, 19),
    ("戌", 19, 21),
    ("亥", 21, 23),
]


def get_hour_zhi(solar_dt: datetime):
    """
    根据太阳时判断时支
    返回：(hour_zhi, is_next_day)
    """
    hour = solar_dt.hour

    for zhi, start, end in HOUR_ZHI_RANGES:
        if start <= hour < end:
            return zhi, False

    # 23:00 - 23:59 → 子时（次日）
    return "子", True


def get_hour_gan(day_gan: str, hour_zhi: str):
    """
    根据日干推时干
    口诀：甲己起甲，乙庚起丙，丙辛起戊，丁壬起庚，戊癸起壬
    """
    start_map = {
        "甲": "甲", "己": "甲",
        "乙": "丙", "庚": "丙",
        "丙": "戊", "辛": "戊",
        "丁": "庚", "壬": "庚",
        "戊": "壬", "癸": "壬"
    }

    start_gan = start_map[day_gan]
    start_index = GAN.index(start_gan)
    zhi_index = ZHI.index(hour_zhi)

    return GAN[(start_index + zhi_index) % 10]


def calc_hour_pillar(
    *,
    solar_time: datetime,
    day_gan: str,
    known_time: bool
):
    """
    对外主入口：计算时柱

    返回结构：
    {
      "pillar": "甲子" | None,
      "hour_zhi": "子" | None,
      "note": "..."（用于 UI 解释）
    }
    """

    # ===== 出生时间不详 =====
    if not known_time:
        return {
            "pillar": None,
            "hour_zhi": None,
            "note": "出生时间不详，时柱未参与计算。"
        }

    # ===== 已知出生时间 =====
    hour_zhi, is_next_day = get_hour_zhi(solar_time)

    # ⚠️ 子时跨日
    effective_day_gan = day_gan
    if is_next_day:
        # 日干顺推一位
        idx = GAN.index(day_gan)
        effective_day_gan = GAN[(idx + 1) % 10]

    hour_gan = get_hour_gan(effective_day_gan, hour_zhi)

    return {
        "pillar": hour_gan + hour_zhi,
        "hour_zhi": hour_zhi,
        "note": "时柱基于太阳时计算。"
    }
