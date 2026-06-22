# core/qiyun_engine.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Tuple
from core.calendar_engine import _find_term_time as _find_term_time_utc

GAN = list("甲乙丙丁戊己庚辛壬癸")
ZHI = list("子丑寅卯辰巳午未申酉戌亥")

YANG_GAN = set(list("甲丙戊庚壬"))  # 阳干
YIN_GAN = set(list("乙丁己辛癸"))   # 阴干

JIE_12_DEG = [
    ("立春", 315), ("惊蛰", 345), ("清明", 15), ("立夏", 45),
    ("芒种", 75), ("小暑", 105), ("立秋", 135), ("白露", 165),
    ("寒露", 195), ("立冬", 225), ("大雪", 255), ("小寒", 285),
]


def _term_datetimes_for_year(year: int) -> List[Tuple[str, datetime]]:
    items = []
    for name, deg in JIE_12_DEG:
        utc_dt = _find_term_time_utc(year, float(deg))
        items.append((name, utc_dt))
    items.sort(key=lambda x: x[1])
    return items


def _find_next_prev_term(solar_dt: datetime, tz_offset_hours: float):
    year = solar_dt.year
    terms = _term_datetimes_for_year(year)

    local_tz = timezone(timedelta(hours=tz_offset_hours))
    local_dt = solar_dt.astimezone(local_tz)
    local_dt_utc = local_dt.astimezone(timezone.utc)

    if local_dt_utc < terms[0][1]:
        prev_terms = _term_datetimes_for_year(year - 1)
        prev_name, prev_dt = prev_terms[-1]
        next_name, next_dt = terms[0]
        return (prev_name, prev_dt), (next_name, next_dt)

    if local_dt_utc >= terms[-1][1]:
        next_terms = _term_datetimes_for_year(year + 1)
        next_name, next_dt = next_terms[0]
        prev_name, prev_dt = terms[-1]
        return (prev_name, prev_dt), (next_name, next_dt)

    prev_item = None
    next_item = None
    for i in range(len(terms)):
        if terms[i][1] <= local_dt_utc:
            prev_item = terms[i]
        if terms[i][1] > local_dt_utc and next_item is None:
            next_item = terms[i]
            break

    if prev_item is None:
        prev_terms = _term_datetimes_for_year(year - 1)
        prev_item = prev_terms[-1]
    if next_item is None:
        next_terms = _term_datetimes_for_year(year + 1)
        next_item = next_terms[0]

    return prev_item, next_item


def _direction_by_gender_and_year_gan(gender: str, year_gan: str) -> str:
    """
    顺逆规则（常用标准）：
    男命：年干为阳 → 顺；年干为阴 → 逆
    女命：年干为阴 → 顺；年干为阳 → 逆
    """
    g = (gender or "").lower()
    if g not in ("male", "female"):
        # 未知性别：默认顺（你也可以改成报错）
        return "forward"

    is_yang = year_gan in YANG_GAN
    if g == "male":
        return "forward" if is_yang else "backward"
    else:
        return "forward" if (year_gan in YIN_GAN) else "backward"


def _age_from_delta(delta: timedelta):
    """
    起运换算（传统常用口径）：
    3天 = 1年
    1天 = 4个月
    1小时 = 5天（因为 24小时=120天）
    => 用天数（含小数）换算成年/月/天
    """
    total_days = delta.total_seconds() / 86400.0
    if total_days < 0:
        total_days = -total_days

    # 3天=1年 => 年 = days/3
    years_float = total_days / 3.0

    years = int(years_float)
    rem_year = years_float - years

    # 1年=12月
    months_float = rem_year * 12.0
    months = int(months_float)
    rem_month = months_float - months

    # 月按30天近似（工程版）
    days = int(round(rem_month * 30.0))

    # 进位修正
    if days >= 30:
        months += 1
        days -= 30
    if months >= 12:
        years += 1
        months -= 12

    return years, months, days


def _gan_zhi_next(gz: str, step: int):
    """对某个干支，按60甲子往前/往后 step（step可负）"""
    # 生成60甲子序列
    seq = []
    for i in range(60):
        seq.append(GAN[i % 10] + ZHI[i % 12])

    try:
        idx = seq.index(gz)
    except ValueError:
        idx = 0
    return seq[(idx + step) % 60]


def build_dayun_list(month_gz: str, direction: str, start_dt: datetime, start_age, count: int = 8):
    """
    month_gz：月柱干支（如 甲寅）
    direction：forward/backward
    start_dt：起运时间（太阳时对应的起运点，工程版）
    start_age：(years, months, days)
    """
    results = []
    age_y, age_m, age_d = start_age

    step_sign = 1 if direction == "forward" else -1

    for i in range(count):
        # 大运干支：以月柱为基准，顺推/逆推
        yun_gz = _gan_zhi_next(month_gz, step_sign * (i + 1))  # 常见做法：起运后第一运从月柱下一步开始

        # 时间段：10年一运（工程版）
        yun_start = start_dt + timedelta(days=365 * 10 * i)
        yun_end = yun_start + timedelta(days=365 * 10) - timedelta(days=1)

        results.append({
            "index": i + 1,
            "gan": yun_gz[0],
            "zhi": yun_gz[1],
            "gz": yun_gz,
            "start_year": yun_start.year,
            "end_year": yun_end.year,
            "start_dt": yun_start.strftime("%Y-%m-%d %H:%M"),
            "end_dt": yun_end.strftime("%Y-%m-%d %H:%M"),
            "age_range": f"{age_y + 10*i}岁起",
            "risk": "mid",
            "text": f"{yun_start.year}–{yun_end.year} 为阶段性运势周期，可用于规划方向与节奏。",
            "advice": "先稳后攻，重视长期积累。"
        })
    return results


def calc_qiyun_and_dayun(
    *,
    birth_solar_dt: datetime,
    year_gz: str,
    month_gz: str,
    gender: str,
    tz_offset_hours: float
):
    """
    输入：出生太阳时、年柱、月柱、性别
    输出：起运信息 + 大运列表
    """
    year_gan = year_gz[0]
    direction = _direction_by_gender_and_year_gan(gender, year_gan)

    prev_term, next_term = _find_next_prev_term(birth_solar_dt, tz_offset_hours)

    local_tz = timezone(timedelta(hours=tz_offset_hours))
    birth_local = birth_solar_dt.astimezone(local_tz)
    if direction == "forward":
        target_name, target_dt_utc = next_term
        target_local = target_dt_utc.astimezone(local_tz)
        delta = target_local - birth_local
    else:
        target_name, target_dt_utc = prev_term
        target_local = target_dt_utc.astimezone(local_tz)
        delta = birth_local - target_local

    age_y, age_m, age_d = _age_from_delta(delta)

    start_dt = birth_local + (delta if direction == "forward" else (-delta))

    qiyun_info = {
        "direction": direction,
        "target_term": target_name,
        "target_term_time_local": target_local.strftime("%Y-%m-%d %H:%M"),
        "target_term_time_utc": target_dt_utc.strftime("%Y-%m-%d %H:%M"),
        "delta_hours": round(delta.total_seconds() / 3600.0, 2),
        "qiyun_age": {"years": age_y, "months": age_m, "days": age_d},
        "qiyun_time": start_dt.strftime("%Y-%m-%d %H:%M"),
        "note": "起运点按“出生太阳时”与最近节气差换算（3天=1年）计算；节气时刻为逐年太阳黄经逼近所得。"
    }

    dayun = build_dayun_list(
        month_gz=month_gz,
        direction=direction,
        start_dt=start_dt,
        start_age=(age_y, age_m, age_d),
        count=8
    )

    return qiyun_info, dayun
