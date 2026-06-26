# core/geo_time_engine.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from core.city_lookup import lookup_city_longitude

COUNTRY_GEO_CONFIG = {
    # 东亚
    "CN": {"name": "中国", "timezone": "Asia/Shanghai", "tz_offset_hours": 8.0, "center_longitude": 116.4},
    "JP": {"name": "日本", "timezone": "Asia/Tokyo", "tz_offset_hours": 9.0, "center_longitude": 139.7},
    "KR": {"name": "韩国", "timezone": "Asia/Seoul", "tz_offset_hours": 9.0, "center_longitude": 127.0},
    "TW": {"name": "台湾", "timezone": "Asia/Taipei", "tz_offset_hours": 8.0, "center_longitude": 121.5},
    "HK": {"name": "香港", "timezone": "Asia/Hong_Kong", "tz_offset_hours": 8.0, "center_longitude": 114.2},
    "MO": {"name": "澳门", "timezone": "Asia/Macau", "tz_offset_hours": 8.0, "center_longitude": 113.5},
    "MN": {"name": "蒙古", "timezone": "Asia/Ulaanbaatar", "tz_offset_hours": 8.0, "center_longitude": 106.9},
    # 东南亚
    "VN": {"name": "越南", "timezone": "Asia/Ho_Chi_Minh", "tz_offset_hours": 7.0, "center_longitude": 105.8},
    "TH": {"name": "泰国", "timezone": "Asia/Bangkok", "tz_offset_hours": 7.0, "center_longitude": 100.5},
    "PH": {"name": "菲律宾", "timezone": "Asia/Manila", "tz_offset_hours": 8.0, "center_longitude": 121.0},
    "MY": {"name": "马来西亚", "timezone": "Asia/Kuala_Lumpur", "tz_offset_hours": 8.0, "center_longitude": 101.7},
    "SG": {"name": "新加坡", "timezone": "Asia/Singapore", "tz_offset_hours": 8.0, "center_longitude": 103.8},
    "ID": {"name": "印度尼西亚", "timezone": "Asia/Jakarta", "tz_offset_hours": 7.0, "center_longitude": 106.8},
    "MM": {"name": "缅甸", "timezone": "Asia/Yangon", "tz_offset_hours": 6.5, "center_longitude": 96.1},
    "KH": {"name": "柬埔寨", "timezone": "Asia/Phnom_Penh", "tz_offset_hours": 7.0, "center_longitude": 104.9},
    "LA": {"name": "老挝", "timezone": "Asia/Vientiane", "tz_offset_hours": 7.0, "center_longitude": 102.6},
    "BN": {"name": "文莱", "timezone": "Asia/Brunei", "tz_offset_hours": 8.0, "center_longitude": 114.9},
    # 南亚
    "IN": {"name": "印度", "timezone": "Asia/Kolkata", "tz_offset_hours": 5.5, "center_longitude": 77.2},
    "PK": {"name": "巴基斯坦", "timezone": "Asia/Karachi", "tz_offset_hours": 5.0, "center_longitude": 67.0},
    "BD": {"name": "孟加拉国", "timezone": "Asia/Dhaka", "tz_offset_hours": 6.0, "center_longitude": 90.4},
    "LK": {"name": "斯里兰卡", "timezone": "Asia/Colombo", "tz_offset_hours": 5.5, "center_longitude": 79.9},
    "NP": {"name": "尼泊尔", "timezone": "Asia/Kathmandu", "tz_offset_hours": 5.75, "center_longitude": 85.3},
    "MV": {"name": "马尔代夫", "timezone": "Indian/Maldives", "tz_offset_hours": 5.0, "center_longitude": 73.5},
    # 中亚/西亚
    "TR": {"name": "土耳其", "timezone": "Europe/Istanbul", "tz_offset_hours": 3.0, "center_longitude": 29.0},
    "SA": {"name": "沙特阿拉伯", "timezone": "Asia/Riyadh", "tz_offset_hours": 3.0, "center_longitude": 46.7},
    "AE": {"name": "阿联酋", "timezone": "Asia/Dubai", "tz_offset_hours": 4.0, "center_longitude": 55.3},
    "QA": {"name": "卡塔尔", "timezone": "Asia/Qatar", "tz_offset_hours": 3.0, "center_longitude": 51.5},
    "KW": {"name": "科威特", "timezone": "Asia/Kuwait", "tz_offset_hours": 3.0, "center_longitude": 47.9},
    "BH": {"name": "巴林", "timezone": "Asia/Bahrain", "tz_offset_hours": 3.0, "center_longitude": 50.6},
    "OM": {"name": "阿曼", "timezone": "Asia/Muscat", "tz_offset_hours": 4.0, "center_longitude": 58.5},
    "IL": {"name": "以色列", "timezone": "Asia/Jerusalem", "tz_offset_hours": 2.0, "center_longitude": 35.2},
    "JO": {"name": "约旦", "timezone": "Asia/Amman", "tz_offset_hours": 2.0, "center_longitude": 35.9},
    "LB": {"name": "黎巴嫩", "timezone": "Asia/Beirut", "tz_offset_hours": 2.0, "center_longitude": 35.5},
    "IQ": {"name": "伊拉克", "timezone": "Asia/Baghdad", "tz_offset_hours": 3.0, "center_longitude": 44.4},
    "IR": {"name": "伊朗", "timezone": "Asia/Tehran", "tz_offset_hours": 3.5, "center_longitude": 51.4},
    "KZ": {"name": "哈萨克斯坦", "timezone": "Asia/Almaty", "tz_offset_hours": 6.0, "center_longitude": 76.9},
    "UZ": {"name": "乌兹别克斯坦", "timezone": "Asia/Tashkent", "tz_offset_hours": 5.0, "center_longitude": 69.3},
    # 北美
    "US": {"name": "美国", "timezone": "America/New_York", "tz_offset_hours": -5.0, "center_longitude": -74.0},
    "CA": {"name": "加拿大", "timezone": "America/Toronto", "tz_offset_hours": -5.0, "center_longitude": -79.4},
    "MX": {"name": "墨西哥", "timezone": "America/Mexico_City", "tz_offset_hours": -6.0, "center_longitude": -99.1},
    "GT": {"name": "危地马拉", "timezone": "America/Guatemala", "tz_offset_hours": -6.0, "center_longitude": -90.5},
    "CU": {"name": "古巴", "timezone": "America/Havana", "tz_offset_hours": -5.0, "center_longitude": -82.4},
    "JM": {"name": "牙买加", "timezone": "America/Jamaica", "tz_offset_hours": -5.0, "center_longitude": -76.8},
    "PA": {"name": "巴拿马", "timezone": "America/Panama", "tz_offset_hours": -5.0, "center_longitude": -79.5},
    # 南美
    "BR": {"name": "巴西", "timezone": "America/Sao_Paulo", "tz_offset_hours": -3.0, "center_longitude": -46.6},
    "AR": {"name": "阿根廷", "timezone": "America/Argentina/Buenos_Aires", "tz_offset_hours": -3.0, "center_longitude": -58.4},
    "CL": {"name": "智利", "timezone": "America/Santiago", "tz_offset_hours": -4.0, "center_longitude": -70.7},
    "CO": {"name": "哥伦比亚", "timezone": "America/Bogota", "tz_offset_hours": -5.0, "center_longitude": -74.1},
    "PE": {"name": "秘鲁", "timezone": "America/Lima", "tz_offset_hours": -5.0, "center_longitude": -77.0},
    "VE": {"name": "委内瑞拉", "timezone": "America/Caracas", "tz_offset_hours": -4.0, "center_longitude": -66.9},
    "EC": {"name": "厄瓜多尔", "timezone": "America/Guayaquil", "tz_offset_hours": -5.0, "center_longitude": -79.9},
    # 欧洲
    "GB": {"name": "英国", "timezone": "Europe/London", "tz_offset_hours": 0.0, "center_longitude": -0.1},
    "DE": {"name": "德国", "timezone": "Europe/Berlin", "tz_offset_hours": 1.0, "center_longitude": 13.4},
    "FR": {"name": "法国", "timezone": "Europe/Paris", "tz_offset_hours": 1.0, "center_longitude": 2.3},
    "RU": {"name": "俄罗斯", "timezone": "Europe/Moscow", "tz_offset_hours": 3.0, "center_longitude": 37.6},
    "IT": {"name": "意大利", "timezone": "Europe/Rome", "tz_offset_hours": 1.0, "center_longitude": 12.5},
    "ES": {"name": "西班牙", "timezone": "Europe/Madrid", "tz_offset_hours": 1.0, "center_longitude": -3.7},
    "PT": {"name": "葡萄牙", "timezone": "Europe/Lisbon", "tz_offset_hours": 0.0, "center_longitude": -9.1},
    "NL": {"name": "荷兰", "timezone": "Europe/Amsterdam", "tz_offset_hours": 1.0, "center_longitude": 4.9},
    "BE": {"name": "比利时", "timezone": "Europe/Brussels", "tz_offset_hours": 1.0, "center_longitude": 4.4},
    "CH": {"name": "瑞士", "timezone": "Europe/Zurich", "tz_offset_hours": 1.0, "center_longitude": 8.5},
    "AT": {"name": "奥地利", "timezone": "Europe/Vienna", "tz_offset_hours": 1.0, "center_longitude": 16.4},
    "SE": {"name": "瑞典", "timezone": "Europe/Stockholm", "tz_offset_hours": 1.0, "center_longitude": 18.1},
    "NO": {"name": "挪威", "timezone": "Europe/Oslo", "tz_offset_hours": 1.0, "center_longitude": 10.8},
    "DK": {"name": "丹麦", "timezone": "Europe/Copenhagen", "tz_offset_hours": 1.0, "center_longitude": 12.6},
    "FI": {"name": "芬兰", "timezone": "Europe/Helsinki", "tz_offset_hours": 2.0, "center_longitude": 24.9},
    "PL": {"name": "波兰", "timezone": "Europe/Warsaw", "tz_offset_hours": 1.0, "center_longitude": 21.0},
    "CZ": {"name": "捷克", "timezone": "Europe/Prague", "tz_offset_hours": 1.0, "center_longitude": 14.4},
    "GR": {"name": "希腊", "timezone": "Europe/Athens", "tz_offset_hours": 2.0, "center_longitude": 23.7},
    "IE": {"name": "爱尔兰", "timezone": "Europe/Dublin", "tz_offset_hours": 0.0, "center_longitude": -6.3},
    "RO": {"name": "罗马尼亚", "timezone": "Europe/Bucharest", "tz_offset_hours": 2.0, "center_longitude": 26.1},
    "UA": {"name": "乌克兰", "timezone": "Europe/Kyiv", "tz_offset_hours": 2.0, "center_longitude": 30.5},
    "HU": {"name": "匈牙利", "timezone": "Europe/Budapest", "tz_offset_hours": 1.0, "center_longitude": 19.0},
    # 非洲
    "EG": {"name": "埃及", "timezone": "Africa/Cairo", "tz_offset_hours": 2.0, "center_longitude": 31.2},
    "ZA": {"name": "南非", "timezone": "Africa/Johannesburg", "tz_offset_hours": 2.0, "center_longitude": 28.0},
    "NG": {"name": "尼日利亚", "timezone": "Africa/Lagos", "tz_offset_hours": 1.0, "center_longitude": 3.4},
    "KE": {"name": "肯尼亚", "timezone": "Africa/Nairobi", "tz_offset_hours": 3.0, "center_longitude": 36.8},
    "GH": {"name": "加纳", "timezone": "Africa/Accra", "tz_offset_hours": 0.0, "center_longitude": -0.2},
    "MA": {"name": "摩洛哥", "timezone": "Africa/Casablanca", "tz_offset_hours": 1.0, "center_longitude": -7.6},
    "ET": {"name": "埃塞俄比亚", "timezone": "Africa/Addis_Ababa", "tz_offset_hours": 3.0, "center_longitude": 38.7},
    "TZ": {"name": "坦桑尼亚", "timezone": "Africa/Dar_es_Salaam", "tz_offset_hours": 3.0, "center_longitude": 39.3},
    "DZ": {"name": "阿尔及利亚", "timezone": "Africa/Algiers", "tz_offset_hours": 1.0, "center_longitude": 3.1},
    # 大洋洲
    "AU": {"name": "澳大利亚", "timezone": "Australia/Sydney", "tz_offset_hours": 10.0, "center_longitude": 151.2},
    "NZ": {"name": "新西兰", "timezone": "Pacific/Auckland", "tz_offset_hours": 12.0, "center_longitude": 174.8},
    "FJ": {"name": "斐济", "timezone": "Pacific/Fiji", "tz_offset_hours": 12.0, "center_longitude": 178.4},
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
