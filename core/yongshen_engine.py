# core/yongshen_engine.py
from core.constants import KE, SHENG, SHENG_REVERSE


def analyze_yongshen(rizhu_wx, strength_level, wuxing):
    if strength_level == "strong":
        use = KE[rizhu_wx]
        explain = "日主偏强，应取克泄之五行为用。"
    elif strength_level == "weak":
        use = SHENG_REVERSE[rizhu_wx]
        explain = "日主偏弱，应取生扶之五行为用。"
    else:
        # 平衡则取缺失最多者
        use = min(wuxing, key=wuxing.get)
        explain = "日主平衡，取命局中相对不足之五行为用。"

    return {
        "element": use,
        "explain": explain
    }
