# core/geo_time_engine.py
from datetime import datetime, timedelta, timezone

COUNTRY_GEO_CONFIG = {
    "CN": {
        "name": "China",
        "timezone": "Asia/Shanghai",
        "tz_offset_hours": 8.0,
        "center_longitude": 116.4074,  # Beijing
        "cities": {}
    },
    "JP": {
        "name": "Japan",
        "timezone": "Asia/Tokyo",
        "tz_offset_hours": 9.0,
        "center_longitude": 139.6917,  # Tokyo
        "cities": {}
    },
    "VN": {
        "name": "Vietnam",
        "timezone": "Asia/Ho_Chi_Minh",
        "tz_offset_hours": 7.0,
        "center_longitude": 105.8542,  # Hanoi
        "cities": {}
    },
    "MM": {
        "name": "Myanmar",
        "timezone": "Asia/Yangon",
        "tz_offset_hours": 6.5,
        "center_longitude": 96.0785,  # Naypyidaw
        "cities": {}
    },
    "LK": {
        "name": "Sri Lanka",
        "timezone": "Asia/Colombo",
        "tz_offset_hours": 5.5,
        "center_longitude": 79.8612,  # Colombo
        "cities": {}
    }
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

    # 用户要求：不管是否填写城市，均使用该国首都经度（center_longitude）
    longitude = cfg["center_longitude"]
    tz_offset = cfg.get("tz_offset_hours", 8.0)

    # city_key 仅作为记录，不影响经度计算
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
