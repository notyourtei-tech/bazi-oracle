"""
Daily Fortune Engine
Calculates daily fortune based on bazi and current day's ganzhi
"""
from datetime import datetime, date
from core.bazi_utils import GAN_WUXING, ZHI_WUXING, SHISHEN_MAP


def get_ganzhi_index(gan_idx, zhi_idx):
    """Get sexagenary cycle index from gan and zhi indices."""
    return (gan_idx * 6 + (zhi_idx - gan_idx * 1) % 10) % 60


def date_to_ganzhi(target_date):
    """Convert a date to ganzhi (heavenly stem + earthly branch)."""
    # Anchor: 1984-01-31 = Jia Zi (index 0)
    anchor = date(1984, 1, 31)
    delta = (target_date - anchor).days
    idx = delta % 60
    
    gan_idx = idx % 10
    zhi_idx = idx % 12
    
    gans = "甲乙丙丁戊己庚辛壬癸"
    zhis = "子丑寅卯辰巳午未申酉戌亥"
    
    return {
        "gan": gans[gan_idx],
        "zhi": zhis[zhi_idx],
        "gan_idx": gan_idx,
        "zhi_idx": zhi_idx,
        "gz": gans[gan_idx] + zhis[zhi_idx],
    }


def calc_daily_fortune(bazi_result, target_date=None):
    """
    Calculate daily fortune based on bazi chart and current day.
    
    Args:
        bazi_result: Full bazi analysis result dict
        target_date: Date to calculate for (default: today)
    
    Returns:
        dict with daily fortune information
    """
    if target_date is None:
        target_date = date.today()
    
    # Get today's ganzhi
    today_gz = date_to_ganzhi(target_date)
    
    # Get day master from bazi
    day_pillar = bazi_result.get("bazi_detail", {}).get("day", {})
    day_master_gan = day_pillar.get("gan", "甲")
    
    # Map gan to index
    gans = "甲乙丙丁戊己庚辛壬癸"
    dm_idx = gans.index(day_master_gan) if day_master_gan in gans else 0
    
    # Get wuxing of day master
    dm_wx = GAN_WUXING.get(day_master_gan, "wood")
    
    # Get today's gan wuxing
    today_gan_wx = GAN_WUXING.get(today_gz["gan"], "wood")
    today_zhi_wx = ZHI_WUXING.get(today_gz["zhi"], "earth")
    
    # Calculate shishen relationship between day master and today's gan
    shishen = SHISHEN_MAP.get((dm_idx, gans.index(today_gz["gan"])), "比肩")
    
    # Calculate favorability based on wuxing relationships
    wx_order = ["wood", "fire", "earth", "metal", "water"]
    wx_generate = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}
    wx_overcome = {"wood": "earth", "earth": "water", "water": "fire", "fire": "metal", "metal": "wood"}
    
    # Determine if today's elements help or harm the day master
    score = 50  # Base score
    
    # Today's gan relationship
    if today_gan_wx == dm_wx:
        score += 10  # Same element = support
    elif wx_generate.get(today_gan_wx) == dm_wx:
        score += 15  # Generates day master = very good
    elif wx_generate.get(dm_wx) == today_gan_wx:
        score += 5   # Day master generates = slightly draining
    elif wx_overcome.get(today_gan_wx) == dm_wx:
        score -= 15  # Overcomes day master = challenging
    elif wx_overcome.get(dm_wx) == today_gan_wx:
        score -= 5   # Day master overcomes = slight effort
    
    # Today's zhi relationship
    if today_zhi_wx == dm_wx:
        score += 5
    elif wx_generate.get(today_zhi_wx) == dm_wx:
        score += 10
    elif wx_overcome.get(today_zhi_wx) == dm_wx:
        score -= 10
    
    # Clamp score
    score = max(20, min(90, score))
    
    # Determine fortune level
    if score >= 75:
        level = "excellent"
        level_text = "大吉"
        color = "#8fd19e"
    elif score >= 60:
        level = "good"
        level_text = "吉"
        color = "#7ec8e3"
    elif score >= 45:
        level = "neutral"
        level_text = "平"
        color = "#e0c36b"
    elif score >= 30:
        level = "caution"
        level_text = "注意"
        color = "#ff826e"
    else:
        level = "challenging"
        level_text = "挑战"
        color = "#b00020"
    
    # Lucky elements
    lucky_colors = {
        "wood": "绿色", "fire": "红色", "earth": "黄色",
        "metal": "白色", "water": "黑色/蓝色"
    }
    lucky_numbers = {
        "wood": "3, 8", "fire": "2, 7", "earth": "5, 0",
        "metal": "4, 9", "water": "1, 6"
    }
    lucky_directions = {
        "wood": "东方", "fire": "南方", "earth": "中央/本地",
        "metal": "西方", "water": "北方"
    }
    
    # Determine what element to supplement today
    # Look at what's weak in the chart
    wuxing = bazi_result.get("wuxing_strength", {})
    min_wx = min(wuxing.items(), key=lambda x: x[1])[0] if wuxing else "wood"
    
    return {
        "date": target_date.isoformat(),
        "day_ganzhi": today_gz["gz"],
        "day_gan": today_gz["gan"],
        "day_zhi": today_gz["zhi"],
        "shishen": shishen,
        "score": score,
        "level": level,
        "level_text": level_text,
        "color": color,
        "lucky_color": lucky_colors.get(min_wx, "金色"),
        "lucky_number": lucky_numbers.get(min_wx, "6, 8"),
        "lucky_direction": lucky_directions.get(min_wx, "南方"),
        "avoid_color": lucky_colors.get(dm_wx, "红色"),
        "summary": _generate_summary(shishen, level, dm_wx, today_gan_wx),
    }


def _generate_summary(shishen, level, dm_wx, today_wx):
    """Generate a brief fortune summary."""
    summaries = {
        "excellent": {
            "比肩": "今日适合与人合作，社交运旺盛。",
            "劫财": "今日人际活跃，注意理财。",
            "食神": "今日心情愉快，适合创作和学习。",
            "伤官": "今日创意十足，适合突破创新。",
            "正财": "今日财运稳定，适合正经生意。",
            "偏财": "今日有意外收获，适合投资。",
            "正官": "今日事业运好，利于升职。",
            "七杀": "今日有挑战但能克服。",
            "正印": "今日贵人运好，适合学习。",
            "偏印": "今日灵感丰富，适合研究。",
        },
        "good": {
            "比肩": "今日适合团队协作。",
            "食神": "今日心情不错，适合享受生活。",
            "正财": "今日收入稳定。",
            "正官": "今日工作顺利。",
            "正印": "今日有人帮助。",
        },
        "neutral": {
            "default": "今日平稳，按部就班即可。",
        },
        "caution": {
            "劫财": "今日注意破财风险。",
            "七杀": "今日压力较大，注意休息。",
            "伤官": "今日注意口舌是非。",
        },
        "challenging": {
            "default": "今日宜守不宜攻，谨慎行事。",
        },
    }
    
    level_summaries = summaries.get(level, {})
    return level_summaries.get(shishen, level_summaries.get("default", "今日运势平稳。"))


def calc_weekly_fortune(bazi_result):
    """Calculate fortune for the current week."""
    today = date.today()
    results = []
    for i in range(7):
        d = date.fromordinal(today.toordinal() + i)
        fortune = calc_daily_fortune(bazi_result, d)
        results.append(fortune)
    return results


def calc_monthly_fortune(bazi_result, year=None, month=None):
    """Calculate fortune for a given month."""
    if year is None or month is None:
        today = date.today()
        year = today.year
        month = today.month
    
    import calendar
    _, days_in_month = calendar.monthrange(year, month)
    
    results = []
    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        fortune = calc_daily_fortune(bazi_result, d)
        results.append(fortune)
    
    return {
        "year": year,
        "month": month,
        "days": results,
        "avg_score": sum(r["score"] for r in results) / len(results) if results else 50,
    }
