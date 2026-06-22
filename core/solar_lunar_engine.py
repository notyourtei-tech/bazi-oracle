# core/solar_lunar_engine.py
from datetime import datetime, timedelta

# =========================
# 节气表（示例版，可扩展）
# 时间：北京时间（UTC+8）
# =========================

SOLAR_TERMS = [
    ("立春", (2, 4, 10)),   # 2月4日 10:00
    ("惊蛰", (3, 6, 5)),
    ("清明", (4, 5, 9)),
    ("立夏", (5, 5, 15)),
    ("芒种", (6, 6, 6)),
    ("小暑", (7, 7, 11)),
    ("立秋", (8, 7, 14)),
    ("白露", (9, 7, 17)),
    ("寒露", (10, 8, 9)),
    ("立冬", (11, 7, 0)),
    ("大雪", (12, 7, 5)),
    ("小寒", (1, 6, 11)),
]

# 天干地支
GAN = list("甲乙丙丁戊己庚辛壬癸")
ZHI = list("子丑寅卯辰巳午未申酉戌亥")


# =========================
# 60甲子日计算基准
# =========================

BASE_DAY = datetime(1984, 1, 31)  # 甲子日（公认基准）


def ganzhi_day(solar_dt: datetime):
    delta_days = (solar_dt.date() - BASE_DAY.date()).days
    idx = delta_days % 60
    return GAN[idx % 10] + ZHI[idx % 12]


# =========================
# 判断节气年 / 月
# =========================

def get_jieqi_year(solar_dt: datetime):
    """
    立春前算上一年
    """
    year = solar_dt.year
    lichun = datetime(year, 2, 4, 10)

    if solar_dt < lichun:
        return year - 1
    return year


def get_jieqi_month(solar_dt: datetime):
    """
    根据节气确定月支
    """
    year = solar_dt.year
    term_times = []

    for name, (m, d, h) in SOLAR_TERMS:
        term_times.append((name, datetime(year, m, d, h)))

    term_times.sort(key=lambda x: x[1])

    for i in range(len(term_times) - 1):
        if term_times[i][1] <= solar_dt < term_times[i + 1][1]:
            return i

    return len(term_times) - 1


# =========================
# 对外主入口
# =========================

def solar_to_ganzhi(solar_dt: datetime):
    """
    输入：太阳时 datetime
    输出：年柱 / 月柱 / 日柱（字符串）
    """

    year = get_jieqi_year(solar_dt)
    year_gz = GAN[(year - 4) % 10] + ZHI[(year - 4) % 12]

    month_index = get_jieqi_month(solar_dt)
    month_gz = GAN[(month_index + year * 2) % 10] + ZHI[(month_index + 2) % 12]

    day_gz = ganzhi_day(solar_dt)

    return {
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
    }
