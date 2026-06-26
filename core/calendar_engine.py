from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Optional
import math

TIANGAN = list("甲乙丙丁戊己庚辛壬癸")
DIZHI   = list("子丑寅卯辰巳午未申酉戌亥")

# 12节（用于月界）：从立春开始
# (名称, 黄经, 月支索引)
# 寅=2, 卯=3, ... 丑=1
JIE_12 = [
    ("立春", 315, 2), ("惊蛰", 345, 3), ("清明",  15, 4), ("立夏",  45, 5),
    ("芒种",  75, 6), ("小暑", 105, 7), ("立秋", 135, 8), ("白露", 165, 9),
    ("寒露", 195, 10),("立冬", 225, 11),("大雪", 255, 0), ("小寒", 285, 1),
]

# 24节气（含中气），目标黄经（度）
SOLAR_TERMS_24 = [
    ("立春", 315), ("雨水", 330), ("惊蛰", 345), ("春分",   0),
    ("清明",  15), ("谷雨",  30), ("立夏",  45), ("小满",  60),
    ("芒种",  75), ("夏至",  90), ("小暑", 105), ("大暑", 120),
    ("立秋", 135), ("处暑", 150), ("白露", 165), ("秋分", 180),
    ("寒露", 195), ("霜降", 210), ("立冬", 225), ("小雪", 240),
    ("大雪", 255), ("冬至", 270), ("小寒", 285), ("大寒", 300),
]


@dataclass
class SolarTerm:
    name: str
    target_deg: float
    utc_dt: datetime


@dataclass
class BaziPillars:
    year: Tuple[str, str]
    month: Tuple[str, str]
    day: Tuple[str, str]
    hour: Tuple[str, str]


@dataclass
class CalendarResult:
    solar_terms_24: List[SolarTerm]     # 当年24节气（UTC）
    year_pillar_year: int              # 立春切换后的“命理年”
    pillars: BaziPillars
    lunar_display: Dict[str, str]       # 先占位：可后续替换成精确农历


# ------------------------------
# 天文近似：太阳黄经（度）
# ------------------------------
def _julian_day(dt_utc: datetime) -> float:
    """UTC datetime -> Julian Day (近似，足够用于节气)"""
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_utc = dt_utc.astimezone(timezone.utc)

    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day + (dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)/24

    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + (A // 4)
    jd = int(365.25*(y + 4716)) + int(30.6001*(m + 1)) + d + B - 1524.5
    return jd


def _sun_ecliptic_longitude_deg(dt_utc: datetime) -> float:
    """
    太阳视黄经近似（度），基于常用低精度公式。
    足以用于节气时间搜索（分钟级到十分钟级）。
    """
    jd = _julian_day(dt_utc)
    T = (jd - 2451545.0) / 36525.0

    # 平黄经（度）
    L0 = 280.46646 + 36000.76983*T + 0.0003032*T*T
    L0 %= 360.0

    # 平近点角（度）
    M = 357.52911 + 35999.05029*T - 0.0001537*T*T
    M_rad = math.radians(M % 360.0)

    # 黄经修正（度）
    C = (1.914602 - 0.004817*T - 0.000014*T*T)*math.sin(M_rad) \
        + (0.019993 - 0.000101*T)*math.sin(2*M_rad) \
        + 0.000289*math.sin(3*M_rad)

    true_long = (L0 + C) % 360.0
    return true_long


def _angle_diff(a: float, b: float) -> float:
    """返回 a-b 的最小角差（-180..180）"""
    d = (a - b + 180) % 360 - 180
    return d


def _find_term_time(year: int, target_deg: float) -> datetime:
    """
    搜索某个 target_deg 对应的UTC时间（粗到精：二分搜索）。
    以 year 为主，搜索窗口放宽：从 year-1/12 到 year+1/12 以覆盖跨年节气。
    """
    # 初始猜测：按目标黄经大概分布在一年中的位置
    # 目标角度映射到日序
    approx_day = int(((target_deg % 360) / 360.0) * 365.2422)
    # 搜索窗口必须足够宽以覆盖实际节气日期（地球轨道偏心率导致线性映射偏差可达80+天）
    start = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=max(0, approx_day-90))
    end   = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=min(365, approx_day+90))

    # 角度在 270-360（冬季）的节气可能出现在年初或年末，需要跨年搜索
    if target_deg >= 270:
        start = datetime(year, 1, 1, tzinfo=timezone.utc) - timedelta(days=40)
        end   = datetime(year, 2, 28, tzinfo=timezone.utc) + timedelta(days=40)
    if target_deg <= 60:
        start = datetime(year, 2, 1, tzinfo=timezone.utc) - timedelta(days=40)
        end   = datetime(year, 5, 1, tzinfo=timezone.utc) + timedelta(days=40)

    # 先粗扫找到符号变化区间
    step = timedelta(hours=6)
    t0 = start
    f0 = _angle_diff(_sun_ecliptic_longitude_deg(t0), target_deg)
    t = t0 + step
    while t <= end:
        f = _angle_diff(_sun_ecliptic_longitude_deg(t), target_deg)
        if f0 == 0:
            return t0
        # 过零：符号变化或跨越
        if (f0 < 0 and f >= 0) or (f0 > 0 and f <= 0):
            # 二分精化
            lo, hi = t0, t
            for _ in range(40):  # 足够把精度压到秒级
                mid = lo + (hi - lo)/2
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

    # 兜底：返回窗口中间（极少发生，需记录警告）
    import logging
    logging.getLogger(__name__).warning(
        f"_find_term_time: failed to locate solar term for deg={target_deg} in year={year}, "
        f"using midpoint fallback — result may be inaccurate"
    )
    return start + (end - start)/2


_solar_terms_cache = {}

def build_solar_terms_24(year: int) -> List[SolarTerm]:
    if year in _solar_terms_cache:
        return _solar_terms_cache[year]
    terms = []
    for name, deg in SOLAR_TERMS_24:
        utc_dt = _find_term_time(year, float(deg))
        terms.append(SolarTerm(name=name, target_deg=float(deg), utc_dt=utc_dt))
    terms.sort(key=lambda x: x.utc_dt)
    _solar_terms_cache[year] = terms
    return terms


# ------------------------------
# 干支计算（基于太阳时）
# ------------------------------
def _sexagenary_index_from_year(year: int) -> int:
    # 1984 是甲子年（索引0）
    return (year - 1984) % 60


def _gz_from_index(idx60: int) -> Tuple[str, str]:
    return (TIANGAN[idx60 % 10], DIZHI[idx60 % 12])


def _year_pillar_by_lichun(solar_true_dt_local: datetime, terms_24: List[SolarTerm]) -> Tuple[int, Tuple[str, str]]:
    """
    年柱以立春为界：solar_true_dt_local 对应UTC后对比当年立春UTC。
    返回：命理年（用于年柱）以及年柱干支
    """
    # 找最近的立春（可能在上一年或下一年）
    lichun_terms = [t for t in terms_24 if t.name == "立春"]
    if not lichun_terms:
        # 理论不会发生
        gz_year = solar_true_dt_local.year
        return gz_year, _gz_from_index(_sexagenary_index_from_year(gz_year))

    # 用同一时刻的UTC对比
    dt_utc = solar_true_dt_local.astimezone(timezone.utc)
    lichun_utc = lichun_terms[0].utc_dt  # terms_24 是当前year为主的，排序后通常包含该年立春
    # 如果出生在立春之前，命理年 = 公历年 - 1
    gz_year = solar_true_dt_local.year
    if dt_utc < lichun_utc:
        gz_year -= 1

    return gz_year, _gz_from_index(_sexagenary_index_from_year(gz_year))


def _month_branch_by_jie(solar_true_dt_local: datetime, year: int) -> int:
    """
    月支按12节（从立春开始）：寅月=立春起，卯月=惊蛰起... 丑月=小寒起
    返回：地支索引（0=子,...,11=亥）
    """
    # 计算当年12节的UTC时间
    jie_list = []
    for name, deg, branch_idx in JIE_12:
        utc_dt = _find_term_time(year, float(deg))
        jie_list.append((name, utc_dt, branch_idx))
    jie_list.sort(key=lambda x: x[1])

    dt_utc = solar_true_dt_local.astimezone(timezone.utc)

    # 找落在哪个节气区间
    # print(f"DEBUG: dt_utc={dt_utc}")
    for i in range(len(jie_list)):
        start = jie_list[i][1]
        end = jie_list[i+1][1] if i+1 < len(jie_list) else jie_list[0][1] + timedelta(days=370)
        # print(f"DEBUG: Checking {jie_list[i][0]} ({start}) <= {dt_utc} < {end}")
        if start <= dt_utc < end:
            return jie_list[i][2]

    # 兜底：默认丑月
    return 1


def _day_index_from_anchor(date_local: datetime) -> int:
    """
    日柱用公历日期（按太阳时后的本地日期）计算。
    锚点：1984-02-02 视为甲子日（工程常用锚点） -> 修正为 1984-01-31 为甲子日?
    校准：2006-05-13 应为 壬寅 (38)。原锚点 1984-02-02 算出 36 (庚子)。
    差 2 天。需要把锚点推前 2 天 (1984-01-31) 或在结果 +2。
    经查 1984-02-02 其实是 丙寅日 (3)。 1984-01-31 是 甲子日 (0)。
    所以锚点设为 1984-01-31 是正确的甲子日锚点。
    """
    anchor = datetime(1984, 1, 31)
    delta_days = (date_local.date() - anchor.date()).days
    return delta_days % 60


def _hour_branch_index(solar_true_dt_local: datetime) -> tuple:
    """
    子时：23:00-00:59，丑：01:00-02:59...
    返回 (hour_branch_index, is_early_zishi)
    is_early_zishi=True 表示 23:00-23:59（早子时，日干需顺推）
    """
    h = solar_true_dt_local.hour
    if h == 23:
        return (0, True)   # 早子时，次日
    if h == 0:
        return (0, False)  # 晚子时，当日
    return (((h + 1) // 2) % 12, False)


def _hour_stem_index(day_stem_index: int, hour_branch_index: int) -> int:
    # 常用公式： (day_stem*2 + hour_branch) % 10
    return (day_stem_index * 2 + hour_branch_index) % 10


def compute_bazi_from_solar_time(
    solar_true_dt_local: datetime,
    *,
    solar_terms_24_for_year: Optional[List[SolarTerm]] = None
) -> CalendarResult:
    """
    输入：出生地太阳时（建议用 geo_time_engine 的 solar_true_dt）
    输出：节气、四柱、占位农历展示
    """
    # 以出生公历年为主构建节气（包含跨年排序）
    year = solar_true_dt_local.year
    terms_24 = solar_terms_24_for_year or build_solar_terms_24(year)

    # 年柱（立春切换）
    gz_year, (y_gan, y_zhi) = _year_pillar_by_lichun(solar_true_dt_local, terms_24)
    year_stem_index = (gz_year - 1984) % 10  # 1984 甲
    year_branch_index = (gz_year - 1984) % 12  # 1984 子

    # 月柱（按12节，月支从寅开始）
    month_branch_index = _month_branch_by_jie(solar_true_dt_local, year)
    month_stem_index = (year_stem_index * 2 + month_branch_index) % 10
    m_gan = TIANGAN[month_stem_index]
    m_zhi = DIZHI[month_branch_index]

    # 日柱（按太阳时本地日期）
    day_idx60 = _day_index_from_anchor(solar_true_dt_local)
    d_gan, d_zhi = _gz_from_index(day_idx60)
    day_stem_index = day_idx60 % 10

    # 时柱（按太阳时）— 早子时(23:00-23:59)日干顺推一位
    hb, is_early_zishi = _hour_branch_index(solar_true_dt_local)
    effective_day_stem = (day_stem_index + 1) % 10 if is_early_zishi else day_stem_index
    hs = _hour_stem_index(effective_day_stem, hb)
    h_gan = TIANGAN[hs]
    h_zhi = DIZHI[hb]

    pillars = BaziPillars(
        year=(y_gan, y_zhi),
        month=(m_gan, m_zhi),
        day=(d_gan, d_zhi),
        hour=(h_gan, h_zhi),
    )

    # 农历展示：先占位（后续你要“农历也精准”，我再给你离线农历算法完整版）
    lunar_display = {
        "note": "农历展示模块当前为占位（不影响八字/大运准确性）",
        "solar_date": solar_true_dt_local.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return CalendarResult(
        solar_terms_24=terms_24,
        year_pillar_year=gz_year,
        pillars=pillars,
        lunar_display=lunar_display,
    )
