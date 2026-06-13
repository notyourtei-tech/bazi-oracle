"""
Compatibility Analysis Engine
Analyzes compatibility between two bazi charts
"""
from core.bazi_utils import GAN_WUXING, ZHI_WUXING


WUXING_GENERATE = {
    "wood": "fire", "fire": "earth", "earth": "metal",
    "metal": "water", "water": "wood"
}
WUXING_OVERCOME = {
    "wood": "earth", "earth": "water", "water": "fire",
    "fire": "metal", "metal": "wood"
}


def analyze_compatibility(result1, result2):
    """
    Analyze compatibility between two bazi charts.
    
    Args:
        result1: First person's bazi result dict
        result2: Second person's bazi result dict
    
    Returns:
        dict with compatibility analysis
    """
    # Get day masters
    dm1_gan = result1.get("bazi_detail", {}).get("day", {}).get("gan", "甲")
    dm2_gan = result2.get("bazi_detail", {}).get("day", {}).get("gan", "甲")
    
    dm1_wx = GAN_WUXING.get(dm1_gan, "wood")
    dm2_wx = GAN_WUXING.get(dm2_gan, "wood")
    
    # Get wuxing strength
    wx1 = result1.get("wuxing_strength", {})
    wx2 = result2.get("wuxing_strength", {})
    
    # Get personality
    p1 = result1.get("personality", {})
    p2 = result2.get("personality", {})
    
    # Calculate scores
    scores = {}
    
    # 1. Five Element Complementarity (how well they balance each other)
    scores["element_complement"] = _calc_element_complement(wx1, wx2)
    
    # 2. Day Master Relationship
    scores["day_master_match"] = _calc_day_master_match(dm1_wx, dm2_wx)
    
    # 3. Day Branch Harmony (marriage palace)
    zhi1 = result1.get("bazi_detail", {}).get("day", {}).get("zhi", "子")
    zhi2 = result2.get("bazi_detail", {}).get("day", {}).get("zhi", "子")
    scores["day_branch_harmony"] = _calc_branch_harmony(zhi1, zhi2)
    
    # 4. Body Strength Balance
    s1 = 1 if "strong" in p1.get("body_strength_key", "") else 0
    s2 = 1 if "strong" in p2.get("body_strength_key", "") else 0
    scores["strength_balance"] = 80 if s1 != s2 else 50
    
    # Overall score
    weights = {
        "element_complement": 0.3,
        "day_master_match": 0.25,
        "day_branch_harmony": 0.25,
        "strength_balance": 0.2,
    }
    overall = sum(scores[k] * weights[k] for k in weights)
    
    # Determine compatibility level
    if overall >= 80:
        level = "excellent"
        level_text = "天作之合"
        emoji = "💕"
    elif overall >= 65:
        level = "good"
        level_text = "相得益彰"
        emoji = "✨"
    elif overall >= 50:
        level = "neutral"
        level_text = "平淡稳定"
        emoji = "🤝"
    elif overall >= 35:
        level = "challenging"
        level_text = "需要磨合"
        emoji = "⚡"
    else:
        level = "difficult"
        level_text = "挑战较多"
        emoji = "🔥"
    
    return {
        "scores": scores,
        "overall_score": round(overall),
        "level": level,
        "level_text": level_text,
        "emoji": emoji,
        "person1": {
            "name": result1.get("name", "甲"),
            "day_master": dm1_gan,
            "wuxing": dm1_wx,
            "body_strength": p1.get("body_strength_key", ""),
        },
        "person2": {
            "name": result2.get("name", "乙"),
            "day_master": dm2_gan,
            "wuxing": dm2_wx,
            "body_strength": p2.get("body_strength_key", ""),
        },
        "analysis": _generate_analysis(dm1_wx, dm2_wx, wx1, wx2, scores, level),
        "advice": _generate_advice(dm1_wx, dm2_wx, level),
    }


def _calc_element_complement(wx1, wx2):
    """Calculate how well two charts complement each other's weak elements."""
    score = 50
    
    for element in ["wood", "fire", "earth", "metal", "water"]:
        v1 = wx1.get(element, 0)
        v2 = wx2.get(element, 0)
        
        # If one is strong and the other is weak in the same element, that's complementary
        if v1 > 60 and v2 < 30:
            score += 8
        elif v2 > 60 and v1 < 30:
            score += 8
        # If both are weak, that's a gap
        elif v1 < 20 and v2 < 20:
            score -= 5
    
    return max(20, min(100, score))


def _calc_day_master_match(wx1, wx2):
    """Calculate compatibility based on day master wuxing relationship."""
    # Same element: friendly but not passionate
    if wx1 == wx2:
        return 60
    
    # One generates the other: supportive
    if WUXING_GENERATE.get(wx1) == wx2:
        return 85  # Person 1 supports Person 2
    if WUXING_GENERATE.get(wx2) == wx1:
        return 85  # Person 2 supports Person 1
    
    # One overcomes the other: challenging
    if WUXING_OVERCOME.get(wx1) == wx2:
        return 40  # Person 1 overcomes Person 2
    if WUXING_OVERCOME.get(wx2) == wx1:
        return 40  # Person 2 overcomes Person 1
    
    return 50


def _calc_branch_harmony(zhi1, zhi2):
    """Calculate day branch (marriage palace) harmony."""
    # Six Harmonies (六合)
    liuhe = {
        "子": "丑", "丑": "子", "寅": "亥", "亥": "寅",
        "卯": "戌", "戌": "卯", "辰": "酉", "酉": "辰",
        "巳": "申", "申": "巳", "午": "未", "未": "午",
    }
    
    # Three Harmonies (三合)
    sanhe = {
        "申": "子", "子": "辰", "辰": "申",  # Water
        "寅": "午", "午": "戌", "戌": "寅",  # Fire
        "巳": "酉", "酉": "丑", "丑": "巳",  # Metal
        "亥": "卯", "卯": "未", "未": "亥",  # Wood
    }
    
    # Six Chats (六冲)
    liuchong = {
        "子": "午", "午": "子", "丑": "未", "未": "丑",
        "寅": "申", "申": "寅", "卯": "酉", "酉": "卯",
        "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳",
    }
    
    if liuhe.get(zhi1) == zhi2:
        return 95  # Six Harmony - excellent
    if sanhe.get(zhi1) == zhi2 or sanhe.get(zhi2) == zhi1:
        return 80  # Three Harmony - very good
    if liuchong.get(zhi1) == zhi2:
        return 30  # Six Clash - challenging
    
    return 55  # Neutral


def _generate_analysis(wx1, wx2, wx1_strength, wx2_strength, scores, level):
    """Generate detailed compatibility analysis text."""
    wx_names = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
    
    parts = []
    
    # Element relationship
    if wx1 == wx2:
        parts.append(f"两人日主同属{wx_names[wx1]}，性格相近，容易理解对方。")
    elif WUXING_GENERATE.get(wx1) == wx2:
        parts.append(f"甲为{wx_names[wx1]}，乙为{wx_names[wx2]}，{wx_names[wx1]}生{wx_names[wx2]}，甲对乙有天然的滋养和帮助。")
    elif WUXING_GENERATE.get(wx2) == wx1:
        parts.append(f"甲为{wx_names[wx1]}，乙为{wx_names[wx2]}，{wx_names[wx2]}生{wx_names[wx1]}，乙对甲有天然的支持。")
    elif WUXING_OVERCOME.get(wx1) == wx2:
        parts.append(f"甲为{wx_names[wx1]}，乙为{wx_names[wx2]}，{wx_names[wx1]}克{wx_names[wx2]}，相处中甲可能给乙压力。")
    elif WUXING_OVERCOME.get(wx2) == wx1:
        parts.append(f"甲为{wx_names[wx1]}，乙为{wx_names[wx2]}，{wx_names[wx2]}克{wx_names[wx1]}，相处中乙可能给甲压力。")
    
    # Element complementarity
    weak_elements = []
    for element in ["wood", "fire", "earth", "metal", "water"]:
        if wx1_strength.get(element, 0) < 25 and wx2_strength.get(element, 0) < 25:
            weak_elements.append(wx_names[element])
    
    if weak_elements:
        parts.append(f"两人共同缺乏{'、'.join(weak_elements)}元素，建议在生活中补充相关能量。")
    
    # Overall assessment
    if level in ["excellent", "good"]:
        parts.append("整体来看，两人的命盘互补性强，相处融洽。")
    elif level == "neutral":
        parts.append("整体来看，两人需要互相理解和包容。")
    else:
        parts.append("整体来看，两人相处需要更多耐心和智慧。")
    
    return "".join(parts)


def _generate_advice(wx1, wx2, level):
    """Generate relationship advice."""
    wx_names = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
    
    if level == "excellent":
        return f"天作之合！{wx_names[wx1]}与{wx_names[wx2]}的组合非常和谐，珍惜彼此，共同成长。"
    elif level == "good":
        return f"{wx_names[wx1]}与{wx_names[wx2]}的组合相得益彰，多沟通、多理解，感情会越来越好。"
    elif level == "neutral":
        return f"{wx_names[wx1]}与{wx_names[wx2]}的组合平淡稳定，需要主动制造浪漫和惊喜。"
    elif level == "challenging":
        return f"{wx_names[wx1]}与{wx_names[wx2]}的组合需要磨合，学会换位思考，互相包容。"
    else:
        return f"{wx_names[wx1]}与{wx_names[wx2]}的组合挑战较多，需要极大的耐心和智慧来经营。"
