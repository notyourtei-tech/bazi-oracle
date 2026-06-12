from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Optional
import math

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

FIVE_TIGER = {
    "甲": "丙", "己": "丙",
    "乙": "戊", "庚": "戊",
    "丙": "庚", "辛": "庚",
    "丁": "壬", "壬": "壬",
    "戊": "甲", "癸": "甲",
}

FIVE_MOUSE = {
    "甲": "甲", "己": "甲",
    "乙": "丙", "庚": "丙",
    "丙": "戊", "辛": "戊",
    "丁": "庚", "壬": "庚",
    "戊": "壬", "癸": "壬",
}

HOUR_RANGES = [
    ("子", 23, 0, 59),
    ("丑", 1, 2, 59),
    ("寅", 3, 4, 59),
    ("卯", 5, 6, 59),
    ("辰", 7, 8, 59),
    ("巳", 9, 10, 59),
    ("午", 11, 12, 59),
    ("未", 13, 14, 59),
    ("申", 15, 16, 59),
    ("酉", 17, 18, 59),
    ("戌", 19, 20, 59),
    ("亥", 21, 22, 59),
]

def _jdn_from_gregorian(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    jdn = d + ((153 * m2 + 2) // 5) + 365 * y2 + (y2 // 4) - (y2 // 100) + (y2 // 400) - 32045
    return jdn

def _sexagenary_from_index(idx60: int) -> Tuple[str, str]:
    return TIANGAN[idx60 % 10], DIZHI[idx60 % 12]

def _day_ganzhi_from_local_date(local_date: datetime, use_zi_switch: bool) -> Tuple[str, str, int]:
    base = datetime(1984, 1, 31)
    jdn = _jdn_from_gregorian(local_date.year, local_date.month, local_date.day)
    jdn_base = _jdn_from_gregorian(base.year, base.month, base.day)
    idx = (jdn - jdn_base) % 60
    gan, zhi = _sexagenary_from_index(idx)
    return gan, zhi, idx

def _eot_minutes(dt: datetime) -> float:
    day = dt.timetuple().tm_yday
    B = 2 * math.pi * (day - 81) / 365.0
    eot = 229.18 * (0.000075 + 0.001868 * math.cos(B) - 0.032077 * math.sin(B) - 0.014615 * math.cos(2 * B) - 0.040849 * math.sin(2 * B))
    return eot

def _true_solar_time(local_dt: datetime, longitude_deg: float, tz_offset_hours: float, dst_enabled: bool, use_true_solar: bool) -> Tuple[datetime, Dict[str, float]]:
    dst_hours = 1.0 if dst_enabled else 0.0
    std_meridian = (tz_offset_hours) * 15.0
    lon_corr_min = (longitude_deg - std_meridian) * 4.0
    eot_min = _eot_minutes(local_dt)
    delta_min = lon_corr_min + eot_min if use_true_solar else 0.0
    solar_dt = local_dt + timedelta(minutes=delta_min)
    return solar_dt, {
        "longitude_deg": longitude_deg,
        "standard_meridian_deg": std_meridian,
        "longitude_correction_min": lon_corr_min,
        "equation_of_time_min": eot_min,
        "delta_minutes_applied": delta_min,
        "tz_offset_hours": tz_offset_hours,
        "dst_hours": dst_hours,
    }

def _sun_ecliptic_longitude_deg(dt_utc: datetime) -> float:
    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day + (dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0) / 24.0
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5
    T = (jd - 2451545.0) / 36525.0
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    L0 %= 360.0
    M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T
    Mr = math.radians(M % 360.0)
    C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(Mr) + (0.019993 - 0.000101 * T) * math.sin(2 * Mr) + 0.000289 * math.sin(3 * Mr)
    lon = (L0 + C) % 360.0
    return lon

def _angle_diff(a: float, b: float) -> float:
    return (a - b + 180) % 360 - 180

def _find_term_time_utc(year: int, target_deg: float) -> datetime:
    diff_deg = (target_deg - 280) % 360
    approx_day = int((diff_deg / 360.0) * 365.2422)
    start = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=max(0, approx_day - 20))
    end = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=min(365, approx_day + 20))
    if target_deg >= 270:
        start = datetime(year, 1, 1, tzinfo=timezone.utc) - timedelta(days=40)
        end = datetime(year, 2, 28, tzinfo=timezone.utc) + timedelta(days=40)
    if target_deg <= 60:
        start = datetime(year, 2, 1, tzinfo=timezone.utc) - timedelta(days=40)
        end = datetime(year, 5, 1, tzinfo=timezone.utc) + timedelta(days=40)
    step = timedelta(hours=6)
    t0 = start
    f0 = _angle_diff(_sun_ecliptic_longitude_deg(t0), target_deg)
    t = t0 + step
    while t <= end:
        f = _angle_diff(_sun_ecliptic_longitude_deg(t), target_deg)
        if f0 == 0:
            return t0
        if (f0 < 0 and f >= 0) or (f0 > 0 and f <= 0):
            lo, hi = t0, t
            for _ in range(40):
                mid = lo + (hi - lo) / 2
                fm = _angle_diff(_sun_ecliptic_longitude_deg(mid), target_deg)
                if (f0 < 0 and fm >= 0) or (f0 > 0 and fm <= 0):
                    hi = mid
                    f = fm
                else:
                    lo = mid
                    f0 = fm
            return hi
        t0, f0 = t, f
        t += step
    return start + (end - start) / 2

JIE_12 = [
    ("立春", 315, 2),
    ("惊蛰", 345, 3),
    ("清明", 15, 4),
    ("立夏", 45, 5),
    ("芒种", 75, 6),
    ("小暑", 105, 7),
    ("立秋", 135, 8),
    ("白露", 165, 9),
    ("寒露", 195, 10),
    ("立冬", 225, 11),
    ("大雪", 255, 0),
    ("小寒", 285, 1),
]

SOLAR_TERMS_24 = [
    ("立春", 315), ("雨水", 330), ("惊蛰", 345), ("春分", 0),
    ("清明", 15), ("谷雨", 30), ("立夏", 45), ("小满", 60),
    ("芒种", 75), ("夏至", 90), ("小暑", 105), ("大暑", 120),
    ("立秋", 135), ("处暑", 150), ("白露", 165), ("秋分", 180),
    ("寒露", 195), ("霜降", 210), ("立冬", 225), ("小雪", 240),
    ("大雪", 255), ("冬至", 270), ("小寒", 285), ("大寒", 300),
]

def _build_terms_utc(year: int) -> List[Tuple[str, float, datetime]]:
    terms = []
    for name, deg in SOLAR_TERMS_24:
        dt = _find_term_time_utc(year, float(deg))
        terms.append((name, float(deg), dt))
    terms.sort(key=lambda x: x[2])
    return terms

def _year_pillar_by_lichun(local_solar_dt: datetime, tz_offset_hours: float) -> Tuple[int, Tuple[str, str], List[Dict]]:
    year = local_solar_dt.year
    terms = _build_terms_utc(year)
    lichun = [t for t in terms if t[0] == "立春"][0][2]
    dt_utc = local_solar_dt.astimezone(timezone.utc)
    gz_year = year
    if dt_utc < lichun:
        gz_year -= 1
    idx60 = (gz_year - 1984) % 60
    gan, zhi = TIANGAN[idx60 % 10], DIZHI[idx60 % 12]
    tz = timezone(timedelta(hours=tz_offset_hours))
    terms_local = []
    for name, deg, utc_dt in terms:
        terms_local.append({
            "name": name,
            "target_deg": deg,
            "utc": utc_dt.isoformat(),
            "local": utc_dt.astimezone(tz).isoformat()
        })
    return gz_year, (gan, zhi), terms_local

def _month_branch_by_jie(local_solar_dt: datetime, tz_offset_hours: float) -> Tuple[int, str, List[Dict], Tuple[str, str]]:
    year = local_solar_dt.year
    jie_list = []
    for name, deg, bidx in JIE_12:
        utc_dt = _find_term_time_utc(year, float(deg))
        jie_list.append((name, deg, bidx, utc_dt))
    jie_list.sort(key=lambda x: x[3])
    tz = timezone(timedelta(hours=tz_offset_hours))
    dt_utc = local_solar_dt.astimezone(timezone.utc)
    selected = None
    for i in range(len(jie_list)):
        start = jie_list[i][3]
        end = jie_list[i + 1][3] if i + 1 < len(jie_list) else jie_list[0][3] + timedelta(days=370)
        if start <= dt_utc < end:
            selected = jie_list[i]
            break
    month_branch_index = selected[2] if selected else 1
    month_branch = DIZHI[month_branch_index]
    intervals = []
    hit = None
    for i in range(len(jie_list)):
        start = jie_list[i][3].astimezone(tz)
        end = (jie_list[i + 1][3] if i + 1 < len(jie_list) else jie_list[0][3] + timedelta(days=370)).astimezone(tz)
        item = {
            "start_name": jie_list[i][0],
            "start_local": start.isoformat(),
            "end_local": end.isoformat(),
            "month_branch": DIZHI[jie_list[i][2]]
        }
        if selected and jie_list[i][0] == selected[0]:
            hit = (item["start_name"], item["month_branch"])
        intervals.append(item)
    return month_branch_index, month_branch, intervals, hit

def _month_stem_by_five_tiger(year_stem: str, month_branch_index: int) -> str:
    start_gan = FIVE_TIGER[year_stem]
    start_idx = TIANGAN.index(start_gan)
    offset = (month_branch_index - 2) % 12
    idx = (start_idx + offset) % 10
    return TIANGAN[idx]

def _hour_branch_from_tst(solar_dt: datetime) -> int:
    h = solar_dt.hour
    m = solar_dt.minute
    if h == 23 or (h == 0 and m <= 59):
        return 0
    ranges = [
        (1, 2, 1), (3, 4, 2), (5, 6, 3), (7, 8, 4),
        (9, 10, 5), (11, 12, 6), (13, 14, 7), (15, 16, 8),
        (17, 18, 9), (19, 20, 10), (21, 22, 11)
    ]
    for s, e, idx in ranges:
        if h >= s and h <= e:
            return idx
    return 0

def _hour_stem_by_five_mouse(day_stem: str, hour_branch_index: int) -> str:
    start_gan = FIVE_MOUSE[day_stem]
    start_idx = TIANGAN.index(start_gan)
    idx = (start_idx + hour_branch_index) % 10
    return TIANGAN[idx]

def compute_bazi(
    birth_dt_local: datetime,
    longitude_deg: float,
    latitude_deg: float,
    tz_offset_hours: float,
    dst_enabled: bool = False,
    use_true_solar: bool = True,
    use_zi_switch: bool = False
) -> Dict:
    solar_dt, tst_detail = _true_solar_time(birth_dt_local, longitude_deg, tz_offset_hours, dst_enabled, use_true_solar)
    gz_year_val, (y_gan, y_zhi), terms_local = _year_pillar_by_lichun(solar_dt, tz_offset_hours)
    mb_idx, m_zhi, month_intervals, hit_interval = _month_branch_by_jie(solar_dt, tz_offset_hours)
    y_stem_idx = (gz_year_val - 1984) % 10
    year_stem = TIANGAN[y_stem_idx]
    m_gan = _month_stem_by_five_tiger(year_stem, mb_idx)
    d_gan, d_zhi, d_idx = _day_ganzhi_from_local_date(birth_dt_local, use_zi_switch)
    hb_idx = _hour_branch_from_tst(solar_dt)
    h_zhi = DIZHI[hb_idx]
    h_gan = _hour_stem_by_five_mouse(d_gan, hb_idx)
    from core.bazi_utils import get_nayin, get_hidden_stems, get_shishen
    nayin_year = get_nayin(y_gan + y_zhi)
    nayin_month = get_nayin(m_gan + m_zhi)
    nayin_day = get_nayin(d_gan + d_zhi)
    nayin_hour = get_nayin(h_gan + h_zhi)
    hidden_year = get_hidden_stems(y_zhi)
    hidden_month = get_hidden_stems(m_zhi)
    hidden_day = get_hidden_stems(d_zhi)
    hidden_hour = get_hidden_stems(h_zhi)
    shishen_year = [get_shishen(d_gan, g) for g in hidden_year]
    shishen_month = [get_shishen(d_gan, g) for g in hidden_month]
    shishen_day = [get_shishen(d_gan, g) for g in hidden_day]
    shishen_hour = [get_shishen(d_gan, g) for g in hidden_hour]
    tz = timezone(timedelta(hours=tz_offset_hours))
    utc_dt = birth_dt_local.astimezone(timezone.utc)
    return {
        "input": {
            "local_dt": birth_dt_local.isoformat(),
            "utc_dt": utc_dt.isoformat(),
            "longitude": longitude_deg,
            "latitude": latitude_deg,
            "tz_offset_hours": tz_offset_hours,
            "dst_enabled": dst_enabled,
            "use_true_solar": use_true_solar,
            "use_zi_switch": use_zi_switch
        },
        "time_correction": {
            "true_solar_dt": solar_dt.isoformat(),
            "details": tst_detail
        },
        "solar_terms": {
            "terms_24_local": terms_local,
            "month_intervals_local": month_intervals,
            "interval_hit": {
                "start_name": hit_interval[0] if hit_interval else None,
                "month_branch": hit_interval[1] if hit_interval else None
            }
        },
        "pillars": {
            "year": {"gan": y_gan, "zhi": y_zhi, "nayin": nayin_year, "hidden_stems": hidden_year, "hidden_shishen": shishen_year},
            "month": {"gan": m_gan, "zhi": m_zhi, "nayin": nayin_month, "hidden_stems": hidden_month, "hidden_shishen": shishen_month},
            "day": {"gan": d_gan, "zhi": d_zhi, "index60": d_idx, "nayin": nayin_day, "hidden_stems": hidden_day, "hidden_shishen": shishen_day},
            "hour": {"gan": h_gan, "zhi": h_zhi, "nayin": nayin_hour, "hidden_stems": hidden_hour, "hidden_shishen": shishen_hour}
        }
    }
