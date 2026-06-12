# core/solar_time.py
# ==========================================
# 真太阳时计算模块
# ==========================================

from datetime import datetime, timedelta

# 国家 → 时区偏移（示例，可继续扩展）
COUNTRY_TIMEZONE = {
    "CN": 8,   # 中国
    "JP": 9,   # 日本
    "KR": 9,   # 韩国
    "VN": 7,   # 越南
    "SG": 8,   # 新加坡
}

def to_solar_time(
    *,
    dt: datetime,
    country: str,
    city: str | None = None
) -> datetime:
    """
    将【证件/官方时间】转换为【中国真太阳时】
    当前版本：先用国家时区占位，后续可接经纬度
    """

    # 1. 取得国家时区
    tz = COUNTRY_TIMEZONE.get(country, 8)

    # 2. 转为北京时间
    beijing_time = dt - timedelta(hours=tz - 8)

    # 3. 真太阳时（占位：后续可接 longitude）
    # 现在先直接返回北京时间
    return beijing_time
