# core/wuxing_engine.py

GAN_WX = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water",
}

ZHI_WX_MAIN = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water",
}

# 地支藏干（简化但专业）
ZHI_CANG = {
    "子": [("癸", 1.0)],
    "丑": [("己", 0.6), ("癸", 0.3), ("辛", 0.1)],
    "寅": [("甲", 0.6), ("丙", 0.3), ("戊", 0.1)],
    "卯": [("乙", 1.0)],
    "辰": [("戊", 0.6), ("乙", 0.3), ("癸", 0.1)],
    "巳": [("丙", 0.6), ("庚", 0.3), ("戊", 0.1)],
    "午": [("丁", 0.7), ("己", 0.3)],
    "未": [("己", 0.6), ("丁", 0.3), ("乙", 0.1)],
    "申": [("庚", 0.6), ("壬", 0.3), ("戊", 0.1)],
    "酉": [("辛", 1.0)],
    "戌": [("戊", 0.6), ("辛", 0.3), ("丁", 0.1)],
    "亥": [("壬", 0.7), ("甲", 0.3)],
}

def calc_wuxing(bazi):
    """
    输入 bazi = {
      "year": ("丙","戌"),
      "month": ("癸","巳"),
      "day": ("甲","辰"),
      "hour": ("?", "?") or None
    }
    """
    score = {
        "wood": 0.0,
        "fire": 0.0,
        "earth": 0.0,
        "metal": 0.0,
        "water": 0.0,
    }

    # 天干权重
    for pillar in ["year", "month", "day", "hour"]:
        if pillar not in bazi or not bazi[pillar]:
            continue
        gan, zhi = bazi[pillar]

        if gan in GAN_WX:
            score[GAN_WX[gan]] += 1.0

        if zhi in ZHI_CANG:
            for cg, w in ZHI_CANG[zhi]:
                score[GAN_WX[cg]] += w

    return {k: round(v * 10, 1) for k, v in score.items()}
