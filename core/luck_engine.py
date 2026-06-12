from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import List, Tuple, Dict, Optional

TIANGAN = list("甲乙丙丁戊己庚辛壬癸")
DIZHI   = list("子丑寅卯辰巳午未申酉戌亥")
YANG_GAN = set("甲丙戊庚壬")
YIN_GAN  = set("乙丁己辛癸")


@dataclass
class StartLuck:
    direction: str          # "forward" or "backward"
    start_years: int
    start_months: int
    start_days: int
    detail: str


@dataclass
class DaYunItem:
    index: int              # 第几步大运（从1开始）
    gan: str
    zhi: str
    start_age_years: int
    end_age_years: int


@dataclass
class LuckResult:
    start_luck: StartLuck
    dayun: List[DaYunItem]
    liunian: List[Tuple[int, str, str]]  # (year, gan, zhi)


def _gz_next(gan: str, zhi: str, step: int) -> Tuple[str, str]:
    gi = TIANGAN.index(gan)
    zi = DIZHI.index(zhi)
    return TIANGAN[(gi + step) % 10], DIZHI[(zi + step) % 12]


def _year_gz(year: int) -> Tuple[str, str]:
    # 1984 甲子年
    idx60 = (year - 1984) % 60
    return TIANGAN[idx60 % 10], DIZHI[idx60 % 12]


def _direction(year_gan: str, gender: str) -> str:
    """
    顺逆：阳男阴女顺；阴男阳女逆
    gender: "male" or "female"
    """
    g = gender.lower()
    if year_gan in YANG_GAN:
        return "forward" if g == "male" else "backward"
    else:
        return "forward" if g == "female" else "backward"


def _pick_jie_boundary(
    solar_true_dt_local: datetime,
    *,
    direction: str,
    jie_times_utc: List[datetime],
) -> Tuple[datetime, str]:
    """
    起运按“节”差（常见做法）：顺排取下一个节；逆排取上一个节。
    输入：出生地太阳时（本地） + 该年12节对应的UTC时间列表
    """
    dt_utc = solar_true_dt_local.astimezone(timezone.utc)
    jie_sorted = sorted(jie_times_utc)

    if direction == "forward":
        for t in jie_sorted:
            if t > dt_utc:
                return t, "next_jie"
        return jie_sorted[0] + timedelta(days=370), "next_jie_wrap"
    else:
        for t in reversed(jie_sorted):
            if t < dt_utc:
                return t, "prev_jie"
        return jie_sorted[-1] - timedelta(days=370), "prev_jie_wrap"


def compute_start_luck(
    solar_true_dt_local: datetime,
    *,
    year_gan: str,
    gender: str,
    jie_times_utc: List[datetime],
) -> StartLuck:
    """
    起运：出生到最近“节”的时间差 -> 三天一岁
    细分：1天=4个月，1小时≈5天？（我们用天/小时精确拆分到月/日）
    """
    direction = _direction(year_gan, gender)
    boundary_utc, mode = _pick_jie_boundary(solar_true_dt_local, direction=direction, jie_times_utc=jie_times_utc)

    dt_utc = solar_true_dt_local.astimezone(timezone.utc)
    diff = boundary_utc - dt_utc if direction == "forward" else dt_utc - boundary_utc
    total_minutes = int(diff.total_seconds() // 60)

    # 三天一岁： 1天=4个月，1小时≈(4个月/24)=~5天? 这里用分钟级拆分成“月、日”更稳
    total_days = total_minutes / (60 * 24)
    start_years = int(total_days // 3)
    rem_days = total_days - start_years * 3

    # 1天=4个月 => rem_days * 4 months
    total_months = rem_days * 4
    start_months = int(total_months)
    rem_month = total_months - start_months

    # 1个月按30天近似拆分（用于显示；起运点核心已由分钟差决定）
    start_days = int(round(rem_month * 30))

    detail = f"direction={direction}, mode={mode}, diff_days≈{total_days:.3f} -> {start_years}y {start_months}m {start_days}d"
    return StartLuck(direction=direction, start_years=start_years, start_months=start_months, start_days=start_days, detail=detail)


def compute_dayun(
    month_pillar: Tuple[str, str],
    *,
    start_age_years: int,
    direction: str,
    steps: int = 10
) -> List[DaYunItem]:
    """
    大运：从月柱起，每10年一柱，顺/逆走干支
    """
    m_gan, m_zhi = month_pillar
    items: List[DaYunItem] = []
    step_dir = 1 if direction == "forward" else -1

    for i in range(1, steps + 1):
        gan, zhi = _gz_next(m_gan, m_zhi, step_dir * i)
        start_age = start_age_years + (i - 1) * 10
        end_age = start_age + 10
        items.append(DaYunItem(index=i, gan=gan, zhi=zhi, start_age_years=start_age, end_age_years=end_age))
    return items


def compute_liunian(
    start_year: int,
    years: int = 10
) -> List[Tuple[int, str, str]]:
    out = []
    for y in range(start_year, start_year + years):
        g, z = _year_gz(y)
        out.append((y, g, z))
    return out


def build_luck(
    solar_true_dt_local: datetime,
    *,
    pillars: Dict[str, Tuple[str, str]],
    gender: str,
    jie_times_utc: List[datetime],
    liunian_from_year: int,
    liunian_years: int = 10
) -> LuckResult:
    """
    综合输出：起运 + 大运 + 流年
    pillars: {"year":(gan,zhi),"month":(...),"day":(...),"hour":(...)}
    """
    year_gan, _ = pillars["year"]
    start_luck = compute_start_luck(
        solar_true_dt_local,
        year_gan=year_gan,
        gender=gender,
        jie_times_utc=jie_times_utc,
    )

    dayun = compute_dayun(
        pillars["month"],
        start_age_years=start_luck.start_years,
        direction=start_luck.direction,
        steps=10,
    )

    liunian = compute_liunian(liunian_from_year, years=liunian_years)
    return LuckResult(start_luck=start_luck, dayun=dayun, liunian=liunian)
