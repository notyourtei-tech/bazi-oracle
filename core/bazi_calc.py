from datetime import datetime

# =====================================================
# 天干 / 地支 基础表
# =====================================================

GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def ganzhi_from_index(index: int):
    """
    index: 0-based
    """
    return GAN[index % 10], ZHI[index % 12]


# =====================================================
# 八字主函数（标准接口）
# =====================================================

def build_bazi(
    *,
    solar_datetime: datetime,
    with_hour: bool = True,
):
    """
    统一八字生成接口

    参数：
    - solar_datetime: datetime（已是太阳时）
    - with_hour: 是否计算时柱（出生时间未知时为 False）

    返回结构：
    {
        "year": (天干, 地支),
        "month": (天干, 地支),
        "day": (天干, 地支),
        "hour": (天干, 地支) | None
    }
    """

    # ⚠️ 说明：
    # 这里用的是【简化算法占位版】
    # 目的是：系统能稳定跑通 + 接口固定
    # 你后面可以无痛替换成 sxtwl / 自写节气算法

    # ---- 年柱（简化）----
    year_index = solar_datetime.year - 4
    year_pillar = ganzhi_from_index(year_index)

    # ---- 月柱（简化占位）----
    # TODO: Month pillar must be determined by solar terms (节气), not calendar month.
    # For now, approximate using the solar datetime's month. This needs calendar_engine integration.
    month_index = year_index * 12 + solar_datetime.month
    month_pillar = ganzhi_from_index(month_index)

    # ---- 日柱（简化）----
    base_date = datetime(1900, 1, 1)
    delta_days = (solar_datetime.date() - base_date.date()).days
    day_pillar = ganzhi_from_index(delta_days)

    # ---- 时柱 ----
    if with_hour:
        hour_index = ((solar_datetime.hour + 1) // 2) % 12
        day_gan_idx = GAN.index(day_pillar[0]) if day_pillar[0] in GAN else 0
        hour_gan_idx = (day_gan_idx * 2 + hour_index) % 10
        hour_pillar = (GAN[hour_gan_idx], ZHI[hour_index])
    else:
        hour_pillar = None

    return {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar,
    }
