# core/geo_time_engine.py
from datetime import datetime, timedelta, timezone
from core.city_lookup import lookup_city_longitude

COUNTRY_GEO_CONFIG = {
    "CN": {"name": "中国", "timezone": "Asia/Shanghai", "tz_offset_hours": 8.0, "center_longitude": 116.4},
    "JP": {"name": "日本", "timezone": "Asia/Tokyo", "tz_offset_hours": 9.0, "center_longitude": 139.7},
    "VN": {"name": "越南", "timezone": "Asia/Ho_Chi_Minh", "tz_offset_hours": 7.0, "center_longitude": 105.8},
    "MM": {"name": "缅甸", "timezone": "Asia/Yangon", "tz_offset_hours": 6.5, "center_longitude": 96.1},
    "LK": {"name": "斯里兰卡", "timezone": "Asia/Colombo", "tz_offset_hours": 5.5, "center_longitude": 79.9},
    "KR": {"name": "韩国", "timezone": "Asia/Seoul", "tz_offset_hours": 9.0, "center_longitude": 127.0},
    "TH": {"name": "泰国", "timezone": "Asia/Bangkok", "tz_offset_hours": 7.0, "center_longitude": 100.5},
    "PH": {"name": "菲律宾", "timezone": "Asia/Manila", "tz_offset_hours": 8.0, "center_longitude": 121.0},
    "MY": {"name": "马来西亚", "timezone": "Asia/Kuala_Lumpur", "tz_offset_hours": 8.0, "center_longitude": 101.7},
    "SG": {"name": "新加坡", "timezone": "Asia/Singapore", "tz_offset_hours": 8.0, "center_longitude": 103.8},
    "ID": {"name": "印度尼西亚", "timezone": "Asia/Jakarta", "tz_offset_hours": 7.0, "center_longitude": 106.8},
    "IN": {"name": "印度", "timezone": "Asia/Kolkata", "tz_offset_hours": 5.5, "center_longitude": 77.2},
    "US": {"name": "美国", "timezone": "America/New_York", "tz_offset_hours": -5.0, "center_longitude": -74.0},
    "GB": {"name": "英国", "timezone": "Europe/London", "tz_offset_hours": 0.0, "center_longitude": -0.1},
    "AU": {"name": "澳大利亚", "timezone": "Australia/Sydney", "tz_offset_hours": 10.0, "center_longitude": 151.2},
    "CA": {"name": "加拿大", "timezone": "America/Toronto", "tz_offset_hours": -5.0, "center_longitude": -79.4},
    "DE": {"name": "德国", "timezone": "Europe/Berlin", "tz_offset_hours": 1.0, "center_longitude": 13.4},
    "FR": {"name": "法国", "timezone": "Europe/Paris", "tz_offset_hours": 1.0, "center_longitude": 2.3},
    "RU": {"name": "俄罗斯", "timezone": "Europe/Moscow", "tz_offset_hours": 3.0, "center_longitude": 37.6},
    "BR": {"name": "巴西", "timezone": "America/Sao_Paulo", "tz_offset_hours": -3.0, "center_longitude": -46.6},
    "MX": {"name": "墨西哥", "timezone": "America/Mexico_City", "tz_offset_hours": -6.0, "center_longitude": -99.1},
    "EG": {"name": "埃及", "timezone": "Africa/Cairo", "tz_offset_hours": 2.0, "center_longitude": 31.2},
    "ZA": {"name": "南非", "timezone": "Africa/Johannesburg", "tz_offset_hours": 2.0, "center_longitude": 28.0},
    "NG": {"name": "尼日利亚", "timezone": "Africa/Lagos", "tz_offset_hours": 1.0, "center_longitude": 3.4},
    "TR": {"name": "土耳其", "timezone": "Europe/Istanbul", "tz_offset_hours": 3.0, "center_longitude": 29.0},
    "SA": {"name": "沙特阿拉伯", "timezone": "Asia/Riyadh", "tz_offset_hours": 3.0, "center_longitude": 46.7},
    "AE": {"name": "阿联酋", "timezone": "Asia/Dubai", "tz_offset_hours": 4.0, "center_longitude": 55.3},
    "NP": {"name": "尼泊尔", "timezone": "Asia/Kathmandu", "tz_offset_hours": 5.75, "center_longitude": 85.3},
    "BD": {"name": "孟加拉国", "timezone": "Asia/Dhaka", "tz_offset_hours": 6.0, "center_longitude": 90.4},
    "PK": {"name": "巴基斯坦", "timezone": "Asia/Karachi", "tz_offset_hours": 5.0, "center_longitude": 67.0},
    "TW": {"name": "台湾", "timezone": "Asia/Taipei", "tz_offset_hours": 8.0, "center_longitude": 121.5},
    "HK": {"name": "香港", "timezone": "Asia/Hong_Kong", "tz_offset_hours": 8.0, "center_longitude": 114.2},
    "MO": {"name": "澳门", "timezone": "Asia/Macau", "tz_offset_hours": 8.0, "center_longitude": 113.5},
}


def calc_solar_time(local_time: datetime, longitude: float, tz_offset_hours: float):
    """
    太阳时修正：
    基准经度 = 时区偏移(小时) × 15°
    每 1° ≈ 4 分钟
    """
    base_longitude = tz_offset_hours * 15.0
    delta_minutes = (longitude - base_longitude) * 4
    # 保持本地时区信息（使后续 astimezone 到 UTC 正确）
    tz = timezone(timedelta(hours=tz_offset_hours))
    if local_time.tzinfo is None:
        local_time = local_time.replace(tzinfo=tz)
    solar_local = local_time + timedelta(minutes=delta_minutes)
    # 太阳时仍在本地时区语义下
    solar_local = solar_local.replace(tzinfo=tz)
    return solar_local


def build_time_bundle(
    country_code: str,
    local_naive: datetime,
    city_key: str | None = None
):
    if country_code not in COUNTRY_GEO_CONFIG:
        raise ValueError(f"Unsupported country code: {country_code}")

    cfg = COUNTRY_GEO_CONFIG[country_code]
    tz_offset = cfg.get("tz_offset_hours", 8.0)

    # 使用城市经度进行更精确的太阳时计算
    if city_key:
        city_info = lookup_city_longitude(country_code, city_key)
        longitude = city_info["longitude"]
    else:
        longitude = cfg["center_longitude"]

    solar_time = calc_solar_time(local_naive, longitude, tz_offset)

    return {
        "country": country_code,
        "city": city_key,
        "timezone": cfg["timezone"],
        "tz_offset_hours": tz_offset,
        "longitude": longitude,
        "local_time": local_naive.replace(tzinfo=timezone(timedelta(hours=tz_offset))),
        "solar_time": solar_time
    }
