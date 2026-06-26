# core/wuxing_engine.py
from core.constants import GAN_WX, ZHI_WX_MAIN, ZHI_CANG

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
