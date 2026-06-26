
# core/interpretation_engine.py
# 综合解读引擎：神煞解释、五行分析、十神分析、性格分析、人生建议

from core.bazi_utils import GAN_WUXING, ZHI_WUXING, get_shishen, YIN_YANG, TIANGAN
from core.wuxing_engine import calc_wuxing, ZHI_CANG
from core.shensha_engine import compute_shensha

# ========================
# 神煞名称与详细解释
# ========================
SHENSHA_EXPLANATIONS = {
    "shensha_tianyi_name": {"title_key": "shensha_tianyi_title", "category_key": "shensha_tianyi_cat", "summary_key": "shensha_tianyi_summary", "detail_key": "shensha_tianyi_detail", "career_key": "shensha_tianyi_career", "health_key": "shensha_tianyi_health", "relationship_key": "shensha_tianyi_relationship", "advice_key": "shensha_tianyi_advice", "category": "shensha_cat_jixing"},
    "shensha_yima_name": {"title_key": "shensha_yima_title", "category_key": "shensha_yima_cat", "summary_key": "shensha_yima_summary", "detail_key": "shensha_yima_detail", "career_key": "shensha_yima_career", "health_key": "shensha_yima_health", "relationship_key": "shensha_yima_relationship", "advice_key": "shensha_yima_advice", "category": "shensha_cat_dongxing"},
    "shensha_taohua_name": {"title_key": "shensha_taohua_title", "category_key": "shensha_taohua_cat", "summary_key": "shensha_taohua_summary", "detail_key": "shensha_taohua_detail", "career_key": "shensha_taohua_career", "health_key": "shensha_taohua_health", "relationship_key": "shensha_taohua_relationship", "advice_key": "shensha_taohua_advice", "category": "shensha_cat_ganqingxing"},
    "shensha_wenchang_name": {"title_key": "shensha_wenchang_title", "category_key": "shensha_wenchang_cat", "summary_key": "shensha_wenchang_summary", "detail_key": "shensha_wenchang_detail", "career_key": "shensha_wenchang_career", "health_key": "shensha_wenchang_health", "relationship_key": "shensha_wenchang_relationship", "advice_key": "shensha_wenchang_advice", "category": "shensha_cat_wenxing"},
    "shensha_jiangxing_name": {"title_key": "shensha_jiangxing_title", "category_key": "shensha_jiangxing_cat", "summary_key": "shensha_jiangxing_summary", "detail_key": "shensha_jiangxing_detail", "career_key": "shensha_jiangxing_career", "health_key": "shensha_jiangxing_health", "relationship_key": "shensha_jiangxing_relationship", "advice_key": "shensha_jiangxing_advice", "category": "shensha_cat_quanxing"},
    "shensha_huagai_name": {"title_key": "shensha_huagai_title", "category_key": "shensha_huagai_cat", "summary_key": "shensha_huagai_summary", "detail_key": "shensha_huagai_detail", "career_key": "shensha_huagai_career", "health_key": "shensha_huagai_health", "relationship_key": "shensha_huagai_relationship", "advice_key": "shensha_huagai_advice", "category": "shensha_cat_yixing"},
    "shensha_yangren_name": {"title_key": "shensha_yangren_title", "category_key": "shensha_yangren_cat", "summary_key": "shensha_yangren_summary", "detail_key": "shensha_yangren_detail", "career_key": "shensha_yangren_career", "health_key": "shensha_yangren_health", "relationship_key": "shensha_yangren_relationship", "advice_key": "shensha_yangren_advice", "category": "shensha_cat_xiongxing"},
    "shensha_lushen_name": {"title_key": "shensha_lushen_title", "category_key": "shensha_lushen_cat", "summary_key": "shensha_lushen_summary", "detail_key": "shensha_lushen_detail", "career_key": "shensha_lushen_career", "health_key": "shensha_lushen_health", "relationship_key": "shensha_lushen_relationship", "advice_key": "shensha_lushen_advice", "category": "shensha_cat_jixing"},
    "shensha_hongluan_name": {"title_key": "shensha_hongluan_title", "category_key": "shensha_hongluan_cat", "summary_key": "shensha_hongluan_summary", "detail_key": "shensha_hongluan_detail", "career_key": "shensha_hongluan_career", "health_key": "shensha_hongluan_health", "relationship_key": "shensha_hongluan_relationship", "advice_key": "shensha_hongluan_advice", "category": "shensha_cat_xixing"},
    "shensha_tianxi_name": {"title_key": "shensha_tianxi_title", "category_key": "shensha_tianxi_cat", "summary_key": "shensha_tianxi_summary", "detail_key": "shensha_tianxi_detail", "career_key": "shensha_tianxi_career", "health_key": "shensha_tianxi_health", "relationship_key": "shensha_tianxi_relationship", "advice_key": "shensha_tianxi_advice", "category": "shensha_cat_xixing"},
    "shensha_jinyu_name": {"title_key": "shensha_jinyu_title", "category_key": "shensha_jinyu_cat", "summary_key": "shensha_jinyu_summary", "detail_key": "shensha_jinyu_detail", "career_key": "shensha_jinyu_career", "health_key": "shensha_jinyu_health", "relationship_key": "shensha_jinyu_relationship", "advice_key": "shensha_jinyu_advice", "category": "shensha_cat_fuguixing"},
    "shensha_kuigang_name": {"title_key": "shensha_kuigang_title", "category_key": "shensha_kuigang_cat", "summary_key": "shensha_kuigang_summary", "detail_key": "shensha_kuigang_detail", "career_key": "shensha_kuigang_career", "health_key": "shensha_kuigang_health", "relationship_key": "shensha_kuigang_relationship", "advice_key": "shensha_kuigang_advice", "category": "shensha_cat_teshuxing"},
    "shensha_guchen_name": {"title_key": "shensha_guchen_title", "category_key": "shensha_guchen_cat", "summary_key": "shensha_guchen_summary", "detail_key": "shensha_guchen_detail", "career_key": "shensha_guchen_career", "health_key": "shensha_guchen_health", "relationship_key": "shensha_guchen_relationship", "advice_key": "shensha_guchen_advice", "category": "shensha_cat_guduxing"},
    "shensha_guasu_name": {"title_key": "shensha_guasu_title", "category_key": "shensha_guasu_cat", "summary_key": "shensha_guasu_summary", "detail_key": "shensha_guasu_detail", "career_key": "shensha_guasu_career", "health_key": "shensha_guasu_health", "relationship_key": "shensha_guasu_relationship", "advice_key": "shensha_guasu_advice", "category": "shensha_cat_guduxing"},
    "shensha_jiesha_name": {"title_key": "shensha_jiesha_title", "category_key": "shensha_jiesha_cat", "summary_key": "shensha_jiesha_summary", "detail_key": "shensha_jiesha_detail", "career_key": "shensha_jiesha_career", "health_key": "shensha_jiesha_health", "relationship_key": "shensha_jiesha_relationship", "advice_key": "shensha_jiesha_advice", "category": "shensha_cat_xiongxing"},
    "shensha_zaisha_name": {"title_key": "shensha_zaisha_title", "category_key": "shensha_zaisha_cat", "summary_key": "shensha_zaisha_summary", "detail_key": "shensha_zaisha_detail", "career_key": "shensha_zaisha_career", "health_key": "shensha_zaisha_health", "relationship_key": "shensha_zaisha_relationship", "advice_key": "shensha_zaisha_advice", "category": "shensha_cat_xiongxing"},
    "shensha_wangshen_name": {"title_key": "shensha_wangshen_title", "category_key": "shensha_wangshen_cat", "summary_key": "shensha_wangshen_summary", "detail_key": "shensha_wangshen_detail", "career_key": "shensha_wangshen_career", "health_key": "shensha_wangshen_health", "relationship_key": "shensha_wangshen_relationship", "advice_key": "shensha_wangshen_advice", "category": "shensha_cat_xiongxing"},
    "shensha_tiande_name": {"title_key": "shensha_tiande_title", "category_key": "shensha_tiande_cat", "summary_key": "shensha_tiande_summary", "detail_key": "shensha_tiande_detail", "career_key": "shensha_tiande_career", "health_key": "shensha_tiande_health", "relationship_key": "shensha_tiande_relationship", "advice_key": "shensha_tiande_advice", "category": "shensha_cat_jixing"},
    "shensha_yuede_name": {"title_key": "shensha_yuede_title", "category_key": "shensha_yuede_cat", "summary_key": "shensha_yuede_summary", "detail_key": "shensha_yuede_detail", "career_key": "shensha_yuede_career", "health_key": "shensha_yuede_health", "relationship_key": "shensha_yuede_relationship", "advice_key": "shensha_yuede_advice", "category": "shensha_cat_jixing"},
    "shensha_xuetang_name": {"title_key": "shensha_xuetang_title", "category_key": "shensha_xuetang_cat", "summary_key": "shensha_xuetang_summary", "detail_key": "shensha_xuetang_detail", "career_key": "shensha_xuetang_career", "health_key": "shensha_xuetang_health", "relationship_key": "shensha_xuetang_relationship", "advice_key": "shensha_xuetang_advice", "category": "shensha_cat_wenxing"},
    "shensha_taiji_name": {"title_key": "shensha_taiji_title", "category_key": "shensha_taiji_cat", "summary_key": "shensha_taiji_summary", "detail_key": "shensha_taiji_detail", "career_key": "shensha_taiji_career", "health_key": "shensha_taiji_health", "relationship_key": "shensha_taiji_relationship", "advice_key": "shensha_taiji_advice", "category": "shensha_cat_teshuxing"},
    "shensha_tianyimed_name": {"title_key": "shensha_tianyimed_title", "category_key": "shensha_tianyimed_cat", "summary_key": "shensha_tianyimed_summary", "detail_key": "shensha_tianyimed_detail", "career_key": "shensha_tianyimed_career", "health_key": "shensha_tianyimed_health", "relationship_key": "shensha_tianyimed_relationship", "advice_key": "shensha_tianyimed_advice", "category": "shensha_cat_teshuxing"},
}

# ========================
# 十神详细解释
# ========================
SHISHEN_EXPLANATIONS = {
    "比肩": {
        "title": "shishen_bijian_title",
        "category": "shishen_bijian_cat",
        "meaning": "shishen_bijian_meaning",
        "personality": "shishen_bijian_personality",
        "career": "shishen_bijian_career",
        "wealth": "shishen_bijian_wealth",
        "relationship": "shishen_bijian_relationship",
        "health": "shishen_bijian_health",
        "advice": "shishen_bijian_advice"
    },
    "劫财": {
        "title": "shishen_jiecai_title",
        "category": "shishen_jiecai_cat",
        "meaning": "shishen_jiecai_meaning",
        "personality": "shishen_jiecai_personality",
        "career": "shishen_jiecai_career",
        "wealth": "shishen_jiecai_wealth",
        "relationship": "shishen_jiecai_relationship",
        "health": "shishen_jiecai_health",
        "advice": "shishen_jiecai_advice"
    },
    "食神": {
        "title": "shishen_shishen_title",
        "category": "shishen_shishen_cat",
        "meaning": "shishen_shishen_meaning",
        "personality": "shishen_shishen_personality",
        "career": "shishen_shishen_career",
        "wealth": "shishen_shishen_wealth",
        "relationship": "shishen_shishen_relationship",
        "health": "shishen_shishen_health",
        "advice": "shishen_shishen_advice"
    },
    "伤官": {
        "title": "shishen_shangguan_title",
        "category": "shishen_shangguan_cat",
        "meaning": "shishen_shangguan_meaning",
        "personality": "shishen_shangguan_personality",
        "career": "shishen_shangguan_career",
        "wealth": "shishen_shangguan_wealth",
        "relationship": "shishen_shangguan_relationship",
        "health": "shishen_shangguan_health",
        "advice": "shishen_shangguan_advice"
    },
    "正财": {
        "title": "shishen_zhengcai_title",
        "category": "shishen_zhengcai_cat",
        "meaning": "shishen_zhengcai_meaning",
        "personality": "shishen_zhengcai_personality",
        "career": "shishen_zhengcai_career",
        "wealth": "shishen_zhengcai_wealth",
        "relationship": "shishen_zhengcai_relationship",
        "health": "shishen_zhengcai_health",
        "advice": "shishen_zhengcai_advice"
    },
    "偏财": {
        "title": "shishen_piancai_title",
        "category": "shishen_piancai_cat",
        "meaning": "shishen_piancai_meaning",
        "personality": "shishen_piancai_personality",
        "career": "shishen_piancai_career",
        "wealth": "shishen_piancai_wealth",
        "relationship": "shishen_piancai_relationship",
        "health": "shishen_piancai_health",
        "advice": "shishen_piancai_advice"
    },
    "正官": {
        "title": "shishen_zhengguan_title",
        "category": "shishen_zhengguan_cat",
        "meaning": "shishen_zhengguan_meaning",
        "personality": "shishen_zhengguan_personality",
        "career": "shishen_zhengguan_career",
        "wealth": "shishen_zhengguan_wealth",
        "relationship": "shishen_zhengguan_relationship",
        "health": "shishen_zhengguan_health",
        "advice": "shishen_zhengguan_advice"
    },
    "七杀": {
        "title": "shishen_qisha_title",
        "category": "shishen_qisha_cat",
        "meaning": "shishen_qisha_meaning",
        "personality": "shishen_qisha_personality",
        "career": "shishen_qisha_career",
        "wealth": "shishen_qisha_wealth",
        "relationship": "shishen_qisha_relationship",
        "health": "shishen_qisha_health",
        "advice": "shishen_qisha_advice"
    },
    "正印": {
        "title": "shishen_zhengyin_title",
        "category": "shishen_zhengyin_cat",
        "meaning": "shishen_zhengyin_meaning",
        "personality": "shishen_zhengyin_personality",
        "career": "shishen_zhengyin_career",
        "wealth": "shishen_zhengyin_wealth",
        "relationship": "shishen_zhengyin_relationship",
        "health": "shishen_zhengyin_health",
        "advice": "shishen_zhengyin_advice"
    },
    "偏印": {
        "title": "shishen_pianyin_title",
        "category": "shishen_pianyin_cat",
        "meaning": "shishen_pianyin_meaning",
        "personality": "shishen_pianyin_personality",
        "career": "shishen_pianyin_career",
        "wealth": "shishen_pianyin_wealth",
        "relationship": "shishen_pianyin_relationship",
        "health": "shishen_pianyin_health",
        "advice": "shishen_pianyin_advice"
    }
}

# ========================
# 五行详细解释
# ========================
WUXING_EXPLANATIONS = {
    "wood": {
        "title_key": "wuxing_wood",
        "nature_key": "wx_wood_nature", "season_key": "wx_wood_season",
        "color_key": "wx_wood_color", "organ_key": "wx_wood_organ",
        "personality_key": "wx_wood_personality", "career_key": "wx_wood_career",
        "health_key": "wx_wood_health", "advice_key": "wx_wood_advice"
    },
    "fire": {
        "title_key": "wuxing_fire",
        "nature_key": "wx_fire_nature", "season_key": "wx_fire_season",
        "color_key": "wx_fire_color", "organ_key": "wx_fire_organ",
        "personality_key": "wx_fire_personality", "career_key": "wx_fire_career",
        "health_key": "wx_fire_health", "advice_key": "wx_fire_advice"
    },
    "earth": {
        "title_key": "wuxing_earth",
        "nature_key": "wx_earth_nature", "season_key": "wx_earth_season",
        "color_key": "wx_earth_color", "organ_key": "wx_earth_organ",
        "personality_key": "wx_earth_personality", "career_key": "wx_earth_career",
        "health_key": "wx_earth_health", "advice_key": "wx_earth_advice"
    },
    "metal": {
        "title_key": "wuxing_metal",
        "nature_key": "wx_metal_nature", "season_key": "wx_metal_season",
        "color_key": "wx_metal_color", "organ_key": "wx_metal_organ",
        "personality_key": "wx_metal_personality", "career_key": "wx_metal_career",
        "health_key": "wx_metal_health", "advice_key": "wx_metal_advice"
    },
    "water": {
        "title_key": "wuxing_water",
        "nature_key": "wx_water_nature", "season_key": "wx_water_season",
        "color_key": "wx_water_color", "organ_key": "wx_water_organ",
        "personality_key": "wx_water_personality", "career_key": "wx_water_career",
        "health_key": "wx_water_health", "advice_key": "wx_water_advice"
    }
}


def build_comprehensive_interpretation(result):
    """
    基于八字结果生成综合解读，包括：
    1. 神煞详细解释
    2. 五行分析详解
    3. 十神分析详解
    4. 性格深度分析
    5. 人生综合建议
    """
    bazi_detail = result.get("bazi_detail", {})
    wuxing_strength = result.get("wuxing_strength", {})
    shensha_list = result.get("shensha", [])
    personality = result.get("personality", {})
    
    interpretation = {}
    
    # 1. 神煞详细解释
    interpretation["shensha_detail"] = _build_shensha_detail(shensha_list)
    
    # 2. 五行分析详解
    interpretation["wuxing_detail"] = _build_wuxing_detail(wuxing_strength, bazi_detail)
    
    # 3. 十神分析详解
    interpretation["shishen_detail"] = _build_shishen_detail(bazi_detail)
    
    # 4. 性格深度分析
    interpretation["personality_detail"] = _build_personality_detail(bazi_detail, personality, wuxing_strength)
    
    # 5. 人生综合建议
    interpretation["life_advice"] = _build_life_advice(bazi_detail, personality, wuxing_strength, shensha_list)
    
    return interpretation


SHISHEN_I18N = {
    "比肩": "Friend", "劫财": "Rob Wealth", "食神": "Eating God",
    "伤官": "Hurting Officer", "正财": "Direct Wealth", "偏财": "Indirect Wealth",
    "正官": "Direct Officer", "七杀": "Seven Killings", "正印": "Direct Resource", "偏印": "Indirect Resource"
}

SHISHEN_CHINESE_TO_KEY = {
    "比肩": "bijian", "劫财": "jiecai", "食神": "shishen",
    "伤官": "shangguan", "正财": "zhengcai", "偏财": "piancai",
    "正官": "zhengguan", "七杀": "qisha",     "正印": "zhengyin", "偏印": "pianyin"
}

SHENSHA_CAT_MAP = {
    "吉星": "shensha_cat_jixing", "动星": "shensha_cat_dongxing",
    "感情星": "shensha_cat_ganqingxing", "文星": "shensha_cat_wenxing",
    "权星": "shensha_cat_quanxing", "艺星": "shensha_cat_yixing",
    "凶星": "shensha_cat_xiongxing", "喜星": "shensha_cat_xixing",
    "富贵星": "shensha_cat_fuguixing", "特殊星": "shensha_cat_teshuxing",
    "孤独星": "shensha_cat_guduxing"
}

SHISHEN_I18N_FIELDS = {
    "title": "shishen_{pinyin}_title",
    "category": "shishen_{pinyin}_cat",
    "meaning": "shishen_{pinyin}_meaning",
    "personality": "shishen_{pinyin}_personality",
    "career": "shishen_{pinyin}_career",
    "wealth": "shishen_{pinyin}_wealth",
    "relationship": "shishen_{pinyin}_relationship",
    "health": "shishen_{pinyin}_health",
    "advice": "shishen_{pinyin}_advice"
}

def _build_shensha_detail(shensha_list):
    """构建神煞详细解释"""
    if not shensha_list:
        return {
            "has_shensha": False,
            "good_stars": [],
            "bad_stars": [],
            "neutral_stars": [],
            "summary_key": "shensha_no_shensha_summary"
        }
    
    good_stars = []
    bad_stars = []
    neutral_stars = []
    
    for s in shensha_list:
        name_key = s.get("name_key", "")
        explanation = SHENSHA_EXPLANATIONS.get(name_key)
        if explanation:
            star_info = {
                "name_key": explanation["title_key"],
                "category_key": explanation["category_key"],
                "detail_key": explanation["detail_key"],
                "pillar_key": "pillar_" + s.get("pillar_key", "").replace("pillar_", ""),
                "category": explanation["category"]
            }
            
            if explanation["category"] in ["shensha_cat_jixing", "shensha_cat_wenxing", "shensha_cat_quanxing", "shensha_cat_xixing", "shensha_cat_fuguixing"]:
                good_stars.append(star_info)
            elif explanation["category"] in ["shensha_cat_xiongxing", "shensha_cat_guduxing"]:
                bad_stars.append(star_info)
            else:
                neutral_stars.append(star_info)
    
    return {
        "has_shensha": True,
        "good_stars": good_stars,
        "bad_stars": bad_stars,
        "neutral_stars": neutral_stars,
        "summary_key": "shensha_has_summary"
    }


def _get_pillar_name(pillar_key):
    """获取柱位 i18n key"""
    mapping = {
        "pillar_year": "pillar_year",
        "pillar_month": "pillar_month",
        "pillar_day": "pillar_day",
        "pillar_hour": "pillar_hour"
    }
    return mapping.get(pillar_key, "pillar_year")


def _build_wuxing_detail(wuxing_strength, bazi_detail):
    """构建五行详细分析"""
    if not wuxing_strength:
        return {"analysis": "err_wuxing_analysis"}
    
    # 排序
    sorted_wx = sorted(wuxing_strength.items(), key=lambda x: x[1], reverse=True)
    strongest = sorted_wx[0]
    weakest = sorted_wx[-1]
    
    # 五行计数
    total = sum(wuxing_strength.values())
    
    # 分析
    wx_map = {"wood": "wuxing_wood", "fire": "wuxing_fire", "earth": "wuxing_earth", "metal": "wuxing_metal", "water": "wuxing_water"}
    
    # 生成详细分析
    analysis_parts = []
    
    # 最旺的五行
    strong_wx = strongest[0]
    strong_explain = WUXING_EXPLANATIONS.get(strong_wx, {})
    analysis_parts.append(f"wx_analysis_strong_{strong_wx}")
    
    # 最弱的五行
    weak_wx = weakest[0]
    weak_explain = WUXING_EXPLANATIONS.get(weak_wx, {})
    analysis_parts.append(f"wx_analysis_weak_{weak_wx}")
    
    # 五行平衡分析
    avg = total / 5
    balance_parts = []
    for wx, score in sorted_wx:
        diff = score - avg
        if diff > avg * 0.3:
            balance_parts.append(wx)
        elif diff < -avg * 0.3:
            balance_parts.append(wx)
    
    if balance_parts:
        analysis_parts.append("wx_analysis_imbalanced")
    else:
        analysis_parts.append("wx_analysis_balanced")
    
    # 生成建议
    advice_parts = []
    for wx, score in sorted_wx:
        explain = WUXING_EXPLANATIONS.get(wx, {})
        if score < avg * 0.5:
            advice_parts.append(f"wx_advice_supplement_{wx}")
        elif score > avg * 1.5:
            advice_parts.append(f"wx_advice_overstrong_{wx}")
    
    return {
        "scores": wuxing_strength,
        "strongest": {"element": wx_map[strongest[0]], "score": strongest[1]},
        "weakest": {"element": wx_map[weakest[0]], "score": weakest[1]},
        "analysis_parts": analysis_parts,
        "advice": advice_parts if advice_parts else ["wx_advice_balanced"],
        "elements_detail": {
            wx: {
                "name": wx_map[wx],
                "score": wuxing_strength[wx],
                "percentage": round(wuxing_strength[wx] / total * 100, 1) if total > 0 else 0,
                "nature_key": WUXING_EXPLANATIONS[wx]["nature_key"],
                "season_key": WUXING_EXPLANATIONS[wx]["season_key"],
                "color_key": WUXING_EXPLANATIONS[wx]["color_key"],
                "organ_key": WUXING_EXPLANATIONS[wx]["organ_key"],
                "personality_key": WUXING_EXPLANATIONS[wx]["personality_key"],
                "career_key": WUXING_EXPLANATIONS[wx]["career_key"],
                "health_key": WUXING_EXPLANATIONS[wx]["health_key"],
            } for wx in ["wood", "fire", "earth", "metal", "water"]
        }
    }


def _build_shishen_detail(bazi_detail):
    """构建十神详细分析"""
    # 获取日主
    day = bazi_detail.get("day", {})
    day_gan = day.get("gan", "")
    
    if not day_gan:
        return {"analysis": "err_shishen_analysis"}
    
    pillars_analysis = []
    
    for pillar_key, pillar_name in [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]:
        pillar = bazi_detail.get(pillar_key, {})
        gan = pillar.get("gan", "")
        
        if not gan or gan == "-":
            continue
        
        # 计算十神
        shishen = get_shishen(day_gan, gan)
        explanation = SHISHEN_EXPLANATIONS.get(shishen, {})
        
        # 获取藏干的十神
        hidden_stars = pillar.get("sub_stars", [])
        
        pillars_analysis.append({
            "pillar_name": pillar_key,
            "gan": gan,
            "shishen": shishen,
            "shishen_key": f"shishen_{SHISHEN_CHINESE_TO_KEY.get(shishen, shishen)}",
            "meaning_key": f"shishen_{SHISHEN_CHINESE_TO_KEY.get(shishen, shishen)}_meaning",
            "personality_key": f"shishen_{SHISHEN_CHINESE_TO_KEY.get(shishen, shishen)}_personality",
            "hidden_stars": [{"name": s.get("name", ""), "key": s.get("key", "")} for s in hidden_stars]
        })
    
    # 生成总结
    shishen_count = {}
    for pa in pillars_analysis:
        ss = pa["shishen"]
        shishen_count[ss] = shishen_count.get(ss, 0) + 1
    
    # 找出最多的十神
    if shishen_count:
        main_shishen = max(shishen_count, key=shishen_count.get)
        main_count = shishen_count[main_shishen]
        shishen_label = SHISHEN_I18N.get(main_shishen, main_shishen)
        summary_key = f"shishen_summary_{main_shishen}"
    else:
        summary_key = "shishen_summary_balanced"
    
    return {
        "pillars": pillars_analysis,
        "shishen_count": shishen_count,
        "summary_key": summary_key
    }


def _build_personality_detail(bazi_detail, personality, wuxing_strength):
    """构建性格深度分析"""
    day = bazi_detail.get("day", {})
    day_gan = day.get("gan", "")
    
    if not day_gan:
        return {"analysis": "err_personality_analysis"}
    
    from core.constants import STEM_ELEMENT
    
    # 日主五行
    dm_element = STEM_ELEMENT.get(day_gan, "")
    # 阴阳
    yang_stems = ["甲", "丙", "戊", "庚", "壬"]
    yin_yang = "阳" if day_gan in yang_stems else "阴"
    
    # 五行性格
    wx_map = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
    wx_explain = WUXING_EXPLANATIONS.get(personality.get("personality_key", "").split("_")[1] if "_" in personality.get("personality_key", "") else "", {})
    
    # 基本性格
    base_trait = personality.get("personality_key", "")
    strength = personality.get("strength_key", "")
    risk = personality.get("risk_key", "")
    
    # 身强身弱
    body_strength = personality.get("body_strength_key", "")
    body_desc = personality.get("body_strength_desc_key", "")
    
    # 综合分析
    if yin_yang == "阳":
        analysis_key = "personality_analysis_strong" if "strong" in body_strength else "personality_analysis_weak"
    else:
        analysis_key = "personality_analysis_yin_strong" if "strong" in body_strength else "personality_analysis_yin_weak"
    
    return {
        "analysis_key": analysis_key
    }



def _build_life_advice(bazi_detail, personality, wuxing_strength, shensha_list):
    """构建人生综合建议"""
    day = bazi_detail.get("day", {})
    day_gan = day.get("gan", "")
    
    if not day_gan:
        return {"advice": "err_life_advice"}
    
    from core.constants import STEM_ELEMENT
    
    dm_element = STEM_ELEMENT.get(day_gan, "")
    body_strength = personality.get("body_strength_key", "")
    
    # 综合建议
    advice = {
        "career": _get_career_advice(dm_element, body_strength, wuxing_strength),
        "wealth": _get_wealth_advice(dm_element, wuxing_strength),
        "relationship": _get_relationship_advice(dm_element, wuxing_strength),
        "health": _get_health_advice(dm_element, wuxing_strength),
        "study": _get_study_advice(dm_element, wuxing_strength),
        "social": _get_social_advice(dm_element, shensha_list),
        "overall": _get_overall_advice(dm_element, body_strength, wuxing_strength, shensha_list)
    }
    
    return advice


def _get_career_advice(element, body_strength, wuxing_strength):
    """事业建议"""
    career_map = {
        "木": "advice_career_wood",
        "火": "advice_career_fire",
        "土": "advice_career_earth",
        "金": "advice_career_metal",
        "水": "advice_career_water"
    }
    base_key = career_map.get(element, "advice_career_default")
    if "strong" in body_strength:
        return base_key + "_strong"
    else:
        return base_key + "_weak"


def _get_wealth_advice(element, wuxing_strength):
    """财运建议"""
    wealth_map = {
        "木": "advice_wealth_wood",
        "火": "advice_wealth_fire",
        "土": "advice_wealth_earth",
        "金": "advice_wealth_metal",
        "水": "advice_wealth_water"
    }
    return wealth_map.get(element, "advice_wealth_default")


def _get_relationship_advice(element, wuxing_strength):
    """感情建议"""
    relationship_map = {
        "木": "advice_love_wood",
        "火": "advice_love_fire",
        "土": "advice_love_earth",
        "金": "advice_love_metal",
        "水": "advice_love_water"
    }
    return relationship_map.get(element, "advice_love_default")


def _get_health_advice(element, wuxing_strength):
    """健康建议"""
    health_map = {
        "木": "advice_health_wood",
        "火": "advice_health_fire",
        "土": "advice_health_earth",
        "金": "advice_health_metal",
        "水": "advice_health_water"
    }
    return health_map.get(element, "advice_health_default")


def _get_study_advice(element, wuxing_strength):
    """学业建议"""
    study_map = {
        "木": "advice_study_wood",
        "火": "advice_study_fire",
        "土": "advice_study_earth",
        "金": "advice_study_metal",
        "水": "advice_study_water"
    }
    return study_map.get(element, "advice_study_default")


def _get_social_advice(element, shensha_list):
    """社交建议"""
    has_taohua = any(s.get("name_key") == "shensha_taohua_name" for s in shensha_list)
    has_tianyi = any(s.get("name_key") == "shensha_tianyi_name" for s in shensha_list)
    
    social_map = {
        "木": "advice_social_wood",
        "火": "advice_social_fire",
        "土": "advice_social_earth",
        "金": "advice_social_metal",
        "水": "advice_social_water"
    }
    key = social_map.get(element, "advice_social_default")
    
    suffix = ""
    if has_taohua:
        suffix = "_taohua"
    if has_tianyi:
        suffix = "_tianyi"
    
    return key + suffix


def _get_overall_advice(element, body_strength, wuxing_strength, shensha_list):
    """综合建议"""
    if "strong" in body_strength:
        base = "advice_overall_strong"
    else:
        base = "advice_overall_weak"
    
    has_good = any(s.get("name_key") in [
        "shensha_tianyi_name", "shensha_tiande_name", "shensha_yuede_name",
        "shensha_wenchang_name", "shensha_hongluan_name", "shensha_tianxi_name"
    ] for s in shensha_list)
    has_bad = any(s.get("name_key") in [
        "shensha_jiesha_name", "shensha_zaisha_name", "shensha_wangshen_name"
    ] for s in shensha_list)
    
    if has_good and has_bad:
        return base + "_stars_mixed"
    elif has_good:
        return base + "_stars_good"
    elif has_bad:
        return base + "_stars_bad"
    return base + "_default"
