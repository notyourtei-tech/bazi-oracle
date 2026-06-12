
# core/personality_engine.py

def calculate_body_strength(dm_wx, month_zhi_wx):
    """
    简易身强身弱判断 (得令与否)
    Returns a dict with key for i18n
    """
    if not month_zhi_wx:
        return {"key": "body_unknown", "desc_key": "body_unknown_desc"}
        
    # 生助日主五行的算身强 (印、比)
    STRONG_MAP = {
        "wood": ["wood", "water"],
        "fire": ["fire", "wood"],
        "earth": ["earth", "fire"],
        "metal": ["metal", "earth"],
        "water": ["water", "metal"]
    }
    
    is_strong = month_zhi_wx in STRONG_MAP.get(dm_wx, [])
    
    if is_strong:
        return {"key": "body_strong", "desc_key": "body_strong_desc"}
    else:
        return {"key": "body_weak", "desc_key": "body_weak_desc"}

def get_wuxing_advice(wuxing_strength):
    """
    根据五行强弱提供建议
    """
    if not wuxing_strength:
        return None
        
    sorted_wx = sorted(wuxing_strength.items(), key=lambda x: x[1])
    weakest_wx = sorted_wx[0][0]
    strongest_wx = sorted_wx[-1][0]
    
    return {
        "weakest": weakest_wx,
        "strongest": strongest_wx,
        "supplement_key": f"advice_supplement_{weakest_wx}",
        "control_key": f"advice_control_{strongest_wx}"
    }

def build_personality_yongshen_analysis(day_master_wx: str, month_zhi_wx: str | None, yongshen: str | None = None, wuxing_strength: dict = None):
    # Return keys instead of text
    
    body_info = calculate_body_strength(day_master_wx, month_zhi_wx)
    wx_advice = get_wuxing_advice(wuxing_strength) if wuxing_strength else None

    # Keys for Day Master Personality
    pm_key_base = f"personality_{day_master_wx}"
    
    result = {
        "personality_key": f"{pm_key_base}_trait",
        "strength_key": f"{pm_key_base}_strength",
        "risk_key": f"{pm_key_base}_risk",
        "body_strength_key": body_info["key"],
        "body_strength_desc_key": body_info["desc_key"],
        "body_strength_career_key": body_info.get("career_key"),
        "body_strength_daily_key": body_info.get("daily_key"),
        "body_strength_caution_key": body_info.get("caution_key"),
        "wuxing_advice": wx_advice
    }

    if yongshen:
        ys_key_base = f"yongshen_{yongshen}"
        result.update({
            "career_advice_key": f"{ys_key_base}_career",
            "relationship_advice_key": f"{ys_key_base}_relationship",
            "risk_advice_key": f"{ys_key_base}_risk"
        })
    else:
        # Fallback or generic keys
        result.update({
            "career_advice_key": "yongshen_general_career",
            "relationship_advice_key": "yongshen_general_relationship",
            "risk_advice_key": "yongshen_general_risk"
        })

    return result

