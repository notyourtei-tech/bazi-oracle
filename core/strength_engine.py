# core/strength_engine.py

GAN_WX = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water",
}

def analyze_strength(bazi, wuxing):
    day_gan = bazi["day"][0]
    wx = GAN_WX.get(day_gan, "earth")

    total = sum(wuxing.values())
    ratio = wuxing.get(wx, 0) / total if total else 0

    if ratio >= 0.28:
        level = "strong"
        text = "日主偏强，承压能力较好，但需避免过刚。"
    elif ratio <= 0.18:
        level = "weak"
        text = "日主偏弱，易受环境影响，需借助外力。"
    else:
        level = "balanced"
        text = "日主强弱适中，整体较为平衡。"

    return {
        "level": level,
        "ratio": round(ratio * 100, 1),
        "detail": text
    }
