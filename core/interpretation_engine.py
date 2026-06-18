
# core/interpretation_engine.py
# 综合解读引擎：神煞解释、五行分析、十神分析、性格分析、人生建议

from core.bazi_utils import GAN_WUXING, ZHI_WUXING, get_shishen, YIN_YANG, TIANGAN
from core.wuxing_engine import calc_wuxing, ZHI_CANG
from core.shensha_engine import compute_shensha

# ========================
# 神煞名称与详细解释
# ========================
SHENSHA_EXPLANATIONS = {
    "shensha_tianyi_name": {"title_key": "shensha_tianyi_title", "category_key": "shensha_tianyi_cat", "summary_key": "shensha_tianyi_summary", "detail_key": "shensha_tianyi_detail", "career_key": "shensha_tianyi_career", "health_key": "shensha_tianyi_health", "relationship_key": "shensha_tianyi_relationship", "advice_key": "shensha_tianyi_advice", "category": "吉星"},
    "shensha_yima_name": {"title_key": "shensha_yima_title", "category_key": "shensha_yima_cat", "summary_key": "shensha_yima_summary", "detail_key": "shensha_yima_detail", "career_key": "shensha_yima_career", "health_key": "shensha_yima_health", "relationship_key": "shensha_yima_relationship", "advice_key": "shensha_yima_advice", "category": "动星"},
    "shensha_taohua_name": {"title_key": "shensha_taohua_title", "category_key": "shensha_taohua_cat", "summary_key": "shensha_taohua_summary", "detail_key": "shensha_taohua_detail", "career_key": "shensha_taohua_career", "health_key": "shensha_taohua_health", "relationship_key": "shensha_taohua_relationship", "advice_key": "shensha_taohua_advice", "category": "感情星"},
    "shensha_wenchang_name": {"title_key": "shensha_wenchang_title", "category_key": "shensha_wenchang_cat", "summary_key": "shensha_wenchang_summary", "detail_key": "shensha_wenchang_detail", "career_key": "shensha_wenchang_career", "health_key": "shensha_wenchang_health", "relationship_key": "shensha_wenchang_relationship", "advice_key": "shensha_wenchang_advice", "category": "文星"},
    "shensha_jiangxing_name": {"title_key": "shensha_jiangxing_title", "category_key": "shensha_jiangxing_cat", "summary_key": "shensha_jiangxing_summary", "detail_key": "shensha_jiangxing_detail", "career_key": "shensha_jiangxing_career", "health_key": "shensha_jiangxing_health", "relationship_key": "shensha_jiangxing_relationship", "advice_key": "shensha_jiangxing_advice", "category": "权星"},
    "shensha_huagai_name": {"title_key": "shensha_huagai_title", "category_key": "shensha_huagai_cat", "summary_key": "shensha_huagai_summary", "detail_key": "shensha_huagai_detail", "career_key": "shensha_huagai_career", "health_key": "shensha_huagai_health", "relationship_key": "shensha_huagai_relationship", "advice_key": "shensha_huagai_advice", "category": "艺星"},
    "shensha_yangren_name": {"title_key": "shensha_yangren_title", "category_key": "shensha_yangren_cat", "summary_key": "shensha_yangren_summary", "detail_key": "shensha_yangren_detail", "career_key": "shensha_yangren_career", "health_key": "shensha_yangren_health", "relationship_key": "shensha_yangren_relationship", "advice_key": "shensha_yangren_advice", "category": "凶星"},
    "shensha_lushen_name": {"title_key": "shensha_lushen_title", "category_key": "shensha_lushen_cat", "summary_key": "shensha_lushen_summary", "detail_key": "shensha_lushen_detail", "career_key": "shensha_lushen_career", "health_key": "shensha_lushen_health", "relationship_key": "shensha_lushen_relationship", "advice_key": "shensha_lushen_advice", "category": "吉星"},
    "shensha_hongluan_name": {"title_key": "shensha_hongluan_title", "category_key": "shensha_hongluan_cat", "summary_key": "shensha_hongluan_summary", "detail_key": "shensha_hongluan_detail", "career_key": "shensha_hongluan_career", "health_key": "shensha_hongluan_health", "relationship_key": "shensha_hongluan_relationship", "advice_key": "shensha_hongluan_advice", "category": "喜星"},
    "shensha_tianxi_name": {"title_key": "shensha_tianxi_title", "category_key": "shensha_tianxi_cat", "summary_key": "shensha_tianxi_summary", "detail_key": "shensha_tianxi_detail", "career_key": "shensha_tianxi_career", "health_key": "shensha_tianxi_health", "relationship_key": "shensha_tianxi_relationship", "advice_key": "shensha_tianxi_advice", "category": "喜星"},
    "shensha_jinyu_name": {"title_key": "shensha_jinyu_title", "category_key": "shensha_jinyu_cat", "summary_key": "shensha_jinyu_summary", "detail_key": "shensha_jinyu_detail", "career_key": "shensha_jinyu_career", "health_key": "shensha_jinyu_health", "relationship_key": "shensha_jinyu_relationship", "advice_key": "shensha_jinyu_advice", "category": "富贵星"},
    "shensha_kuigang_name": {"title_key": "shensha_kuigang_title", "category_key": "shensha_kuigang_cat", "summary_key": "shensha_kuigang_summary", "detail_key": "shensha_kuigang_detail", "career_key": "shensha_kuigang_career", "health_key": "shensha_kuigang_health", "relationship_key": "shensha_kuigang_relationship", "advice_key": "shensha_kuigang_advice", "category": "特殊星"},
    "shensha_guchen_name": {"title_key": "shensha_guchen_title", "category_key": "shensha_guchen_cat", "summary_key": "shensha_guchen_summary", "detail_key": "shensha_guchen_detail", "career_key": "shensha_guchen_career", "health_key": "shensha_guchen_health", "relationship_key": "shensha_guchen_relationship", "advice_key": "shensha_guchen_advice", "category": "孤独星"},
    "shensha_guasu_name": {"title_key": "shensha_guasu_title", "category_key": "shensha_guasu_cat", "summary_key": "shensha_guasu_summary", "detail_key": "shensha_guasu_detail", "career_key": "shensha_guasu_career", "health_key": "shensha_guasu_health", "relationship_key": "shensha_guasu_relationship", "advice_key": "shensha_guasu_advice", "category": "孤独星"},
    "shensha_jiesha_name": {"title_key": "shensha_jiesha_title", "category_key": "shensha_jiesha_cat", "summary_key": "shensha_jiesha_summary", "detail_key": "shensha_jiesha_detail", "career_key": "shensha_jiesha_career", "health_key": "shensha_jiesha_health", "relationship_key": "shensha_jiesha_relationship", "advice_key": "shensha_jiesha_advice", "category": "凶星"},
    "shensha_zaisha_name": {"title_key": "shensha_zaisha_title", "category_key": "shensha_zaisha_cat", "summary_key": "shensha_zaisha_summary", "detail_key": "shensha_zaisha_detail", "career_key": "shensha_zaisha_career", "health_key": "shensha_zaisha_health", "relationship_key": "shensha_zaisha_relationship", "advice_key": "shensha_zaisha_advice", "category": "凶星"},
    "shensha_wangshen_name": {"title_key": "shensha_wangshen_title", "category_key": "shensha_wangshen_cat", "summary_key": "shensha_wangshen_summary", "detail_key": "shensha_wangshen_detail", "career_key": "shensha_wangshen_career", "health_key": "shensha_wangshen_health", "relationship_key": "shensha_wangshen_relationship", "advice_key": "shensha_wangshen_advice", "category": "凶星"},
    "shensha_tiande_name": {"title_key": "shensha_tiande_title", "category_key": "shensha_tiande_cat", "summary_key": "shensha_tiande_summary", "detail_key": "shensha_tiande_detail", "career_key": "shensha_tiande_career", "health_key": "shensha_tiande_health", "relationship_key": "shensha_tiande_relationship", "advice_key": "shensha_tiande_advice", "category": "吉星"},
    "shensha_yuede_name": {"title_key": "shensha_yuede_title", "category_key": "shensha_yuede_cat", "summary_key": "shensha_yuede_summary", "detail_key": "shensha_yuede_detail", "career_key": "shensha_yuede_career", "health_key": "shensha_yuede_health", "relationship_key": "shensha_yuede_relationship", "advice_key": "shensha_yuede_advice", "category": "吉星"},
    "shensha_xuetang_name": {"title_key": "shensha_xuetang_title", "category_key": "shensha_xuetang_cat", "summary_key": "shensha_xuetang_summary", "detail_key": "shensha_xuetang_detail", "career_key": "shensha_xuetang_career", "health_key": "shensha_xuetang_health", "relationship_key": "shensha_xuetang_relationship", "advice_key": "shensha_xuetang_advice", "category": "文星"},
    "shensha_taiji_name": {"title_key": "shensha_taiji_title", "category_key": "shensha_taiji_cat", "summary_key": "shensha_taiji_summary", "detail_key": "shensha_taiji_detail", "career_key": "shensha_taiji_career", "health_key": "shensha_taiji_health", "relationship_key": "shensha_taiji_relationship", "advice_key": "shensha_taiji_advice", "category": "特殊星"},
    "shensha_tianyimed_name": {"title_key": "shensha_tianyimed_title", "category_key": "shensha_tianyimed_cat", "summary_key": "shensha_tianyimed_summary", "detail_key": "shensha_tianyimed_detail", "career_key": "shensha_tianyimed_career", "health_key": "shensha_tianyimed_health", "relationship_key": "shensha_tianyimed_relationship", "advice_key": "shensha_tianyimed_advice", "category": "特殊星"},
}

# ========================
# 十神详细解释
# ========================
SHISHEN_EXPLANATIONS = {
    "比肩": {
        "title": "比肩",
        "category": "同类",
        "meaning": "与日主相同五行和阴阳的天干，代表自我、独立、竞争。",
        "personality": "比肩旺者性格独立、自信、有主见，喜欢自己做决定。为人正直、重义气，但有时过于固执、不听劝告。竞争意识强，不甘人后。",
        "career": "适合独立创业、自主经营、自由职业等需要独立性的工作。也适合与人合伙，但要注意权益分配。",
        "wealth": "比肩旺则财运起伏较大，容易有朋友借钱或合伙破财的情况。需要学会理财和拒绝。",
        "relationship": "在感情中比较独立，不太依赖伴侣。婚姻中要注意给对方空间，避免太过自我。",
        "health": "比肩旺者一般身体素质好，但要注意不要过度劳累。",
        "advice": "学会合作与分享，不要什么事都自己扛。适当借助他人的力量。"
    },
    "劫财": {
        "title": "劫财",
        "category": "同类",
        "meaning": "与日主相同五行但阴阳相反的天干，代表竞争、破耗、冲动。",
        "personality": "劫财旺者性格豪爽、大方、敢于冒险，社交能力强。但容易冲动消费、被人利用。有赌性，做事有时不够谨慎。",
        "career": "适合销售、公关、娱乐、餐饮等需要社交和冒险精神的行业。",
        "wealth": "劫财主破耗，花钱大手大脚，容易被人骗财。需要加强理财意识。",
        "relationship": "感情上比较主动，但也容易因为朋友而忽略伴侣。要注意平衡社交和家庭。",
        "health": "劫财主消耗，要注意不要过度透支身体。",
        "advice": "控制消费冲动，谨慎交友，不要轻信他人的投资建议。"
    },
    "食神": {
        "title": "食神",
        "category": "我生",
        "meaning": "日主所生且与日主同阴阳的天干，代表才华、享受、口福。",
        "personality": "食神旺者性格温和、乐观、有才华，善于表达和创作。喜欢美食和享受生活，有时有些懒散。为人善良、有口福。",
        "career": "适合餐饮、美食、演艺、创作、教育等需要才华和表现力的行业。",
        "wealth": "食神主口福和享受，财运一般稳定，适合靠才华赚钱。",
        "relationship": "食神旺者感情丰富，善于表达爱意，婚姻生活甜蜜。",
        "health": "食神主享受，要注意不要过度美食而导致肥胖。",
        "advice": "发挥才华，享受生活，但不要过于安逸。"
    },
    "伤官": {
        "title": "伤官",
        "category": "我生",
        "meaning": "日主所生但与日主阴阳相反的天干，代表叛逆、创新、口才。",
        "personality": "伤官旺者思维敏捷、叛逆心强、口才好、有创造力。但容易骄傲自大、得罪人。不喜欢被约束，追求自由。",
        "career": "适合创意、设计、演艺、写作、咨询等需要创新和口才的行业。",
        "wealth": "伤官生财能力强，但花钱也大，需要学会开源节流。",
        "relationship": "伤官旺者在感情中比较挑剔，容易与伴侣发生口角。",
        "health": "伤官主消耗，要注意不要过度用脑和说话。",
        "advice": "把创新和口才用在正途上，不要过于锋芒毕露。"
    },
    "正财": {
        "title": "正财",
        "category": "我克",
        "meaning": "日主所克且与日主阴阳相反的天干，代表稳定收入、妻子（男命）、务实。",
        "personality": "正财旺者性格务实、勤恳、注重实际利益。做事踏实、不投机取巧，为人诚实可靠。但有时过于保守，缺乏冒险精神。",
        "career": "适合会计、银行、行政、财务等稳定务实的行业。",
        "wealth": "正财主稳定收入，财运稳定但不会暴富。适合长期投资和储蓄。",
        "relationship": "正财代表正缘，感情稳定，婚姻幸福。男命以正财为妻星。",
        "health": "正财旺者生活规律，一般健康较好。",
        "advice": "保持勤恳务实的态度，稳定积累财富。"
    },
    "偏财": {
        "title": "偏财",
        "category": "我克",
        "meaning": "日主所克且与日主同阴阳的天干，代表意外之财、父亲、交际。",
        "personality": "偏财旺者性格开朗、大方、善于交际，有投资眼光。但容易贪图享受、花钱如流水。人缘好，异性缘也不错。",
        "career": "适合投资、贸易、销售、公关、娱乐等需要交际和眼光的行业。",
        "wealth": "偏财主意外之财，财运起伏较大。适合投资和投机，但要注意风险。",
        "relationship": "偏财旺者异性缘好，但感情上容易花心。要注意专一。",
        "health": "偏财主享受，要注意不要过度纵欲。",
        "advice": "善用投资眼光，但要控制风险。感情上要专一。"
    },
    "正官": {
        "title": "正官",
        "category": "克我",
        "meaning": "克日主且与日主阴阳相反的天干，代表权力、地位、丈夫（女命）。",
        "personality": "正官旺者性格正直、有责任感、守规矩、有领导才能。为人正派、有权威感。但有时过于保守、拘泥于形式。",
        "career": "适合公务员、管理层、法律、教育等需要权威和责任的行业。",
        "wealth": "正官主地位和权力，财运一般稳定，靠正当收入赚钱。",
        "relationship": "正官代表正缘，感情稳定。女命以正官为夫星。",
        "health": "正官旺者生活规律，但要注意不要过于操劳。",
        "advice": "发挥领导才能，但要灵活变通，不要过于死板。"
    },
    "七杀": {
        "title": "七杀",
        "category": "克我",
        "meaning": "克日主且与日主同阴阳的天干，代表压力、挑战、权力。",
        "personality": "七杀旺者性格刚强、有魄力、敢于冒险。有领导才能和决断力，但脾气大、容易冲动。压力大但抗压能力强。",
        "career": "适合军警、法律、竞技、管理等需要魄力和决断力的行业。",
        "wealth": "七杀主竞争和压力，财运起伏较大。需要努力拼搏才能获得财富。",
        "relationship": "七杀旺者在感情中比较强势，容易与伴侣发生冲突。",
        "health": "七杀主压力和意外，要注意安全和心理健康。",
        "advice": "把压力转化为动力，但要注意控制脾气和安全。"
    },
    "正印": {
        "title": "正印",
        "category": "生我",
        "meaning": "生助日主且与日主阴阳相反的天干，代表母亲、贵人、学历。",
        "personality": "正印旺者性格温和、善良、有包容心。重视学习和修养，有宗教或哲学倾向。为人慈祥、有爱心。但有时过于理想化。",
        "career": "适合教育、文化、宗教、慈善、心理咨询等需要爱心和修养的行业。",
        "wealth": "正印主贵人和学历，财运一般稳定，靠知识和贵人赚钱。",
        "relationship": "正印旺者感情温和，婚姻稳定。对伴侣有包容心。",
        "health": "正印旺者心态平和，一般健康较好。",
        "advice": "多学习提升自己，善用贵人运，发挥爱心和包容力。"
    },
    "偏印": {
        "title": "偏印",
        "category": "生我",
        "meaning": "生助日主且与日主同阴阳的天干，代表偏门学问、继母、孤独。",
        "personality": "偏印旺者思维独特、直觉敏锐、有创造力。喜欢研究偏门学问，对神秘文化有兴趣。但容易孤独、不合群。有时过于多疑。",
        "career": "适合研究、占卜、中医、心理咨询、艺术创作等需要独特思维的行业。",
        "wealth": "偏印主偏门收入，财运不稳定。适合靠独特技能赚钱。",
        "relationship": "偏印旺者在感情中比较被动，容易孤独。",
        "health": "偏印主孤独，要注意心理健康，多与人交流。",
        "advice": "发挥独特思维的优势，但要注意融入社会，不要过于封闭。"
    }
}

# ========================
# 五行详细解释
# ========================
WUXING_EXPLANATIONS = {
    "wood": {
        "title": "木",
        "nature_key": "wx_wood_nature", "season_key": "wx_wood_season",
        "color_key": "wx_wood_color", "organ_key": "wx_wood_organ",
        "personality_key": "wx_wood_personality", "career_key": "wx_wood_career",
        "health_key": "wx_wood_health", "advice_key": "wx_wood_advice"
    },
    "fire": {
        "title": "火",
        "nature_key": "wx_fire_nature", "season_key": "wx_fire_season",
        "color_key": "wx_fire_color", "organ_key": "wx_fire_organ",
        "personality_key": "wx_fire_personality", "career_key": "wx_fire_career",
        "health_key": "wx_fire_health", "advice_key": "wx_fire_advice"
    },
    "earth": {
        "title": "土",
        "nature_key": "wx_earth_nature", "season_key": "wx_earth_season",
        "color_key": "wx_earth_color", "organ_key": "wx_earth_organ",
        "personality_key": "wx_earth_personality", "career_key": "wx_earth_career",
        "health_key": "wx_earth_health", "advice_key": "wx_earth_advice"
    },
    "metal": {
        "title": "金",
        "nature_key": "wx_metal_nature", "season_key": "wx_metal_season",
        "color_key": "wx_metal_color", "organ_key": "wx_metal_organ",
        "personality_key": "wx_metal_personality", "career_key": "wx_metal_career",
        "health_key": "wx_metal_health", "advice_key": "wx_metal_advice"
    },
    "water": {
        "title": "水",
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
            
            if explanation["category"] in ["吉星", "文星", "权星", "喜星", "富贵星"]:
                good_stars.append(star_info)
            elif explanation["category"] in ["凶星", "孤独星"]:
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
        return {"analysis": "无法进行五行分析。"}
    
    # 排序
    sorted_wx = sorted(wuxing_strength.items(), key=lambda x: x[1], reverse=True)
    strongest = sorted_wx[0]
    weakest = sorted_wx[-1]
    
    # 五行计数
    total = sum(wuxing_strength.values())
    
    # 分析
    wx_map = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
    
    # 生成详细分析
    analysis_parts = []
    
    # 最旺的五行
    strong_wx = strongest[0]
    strong_explain = WUXING_EXPLANATIONS.get(strong_wx, {})
    analysis_parts.append(f"命盘中{wx_map[strong_wx]}行最旺（{strongest[1]:.1f}分），{strong_explain.get('personality', '')}")
    
    # 最弱的五行
    weak_wx = weakest[0]
    weak_explain = WUXING_EXPLANATIONS.get(weak_wx, {})
    analysis_parts.append(f"{wx_map[weak_wx]}行最弱（{weakest[1]:.1f}分），{weak_explain.get('personality', '')}")
    
    # 五行平衡分析
    avg = total / 5
    balance_parts = []
    for wx, score in sorted_wx:
        diff = score - avg
        if diff > avg * 0.3:
            balance_parts.append(f"{wx_map[wx]}偏旺")
        elif diff < -avg * 0.3:
            balance_parts.append(f"{wx_map[wx]}偏弱")
    
    if balance_parts:
        analysis_parts.append(f"五行{'、'.join(balance_parts)}")
    else:
        analysis_parts.append("五行相对平衡")
    
    # 生成建议
    advice_parts = []
    for wx, score in sorted_wx:
        explain = WUXING_EXPLANATIONS.get(wx, {})
        if score < avg * 0.5:
            advice_parts.append(f"建议补充{wx_map[wx]}：{explain.get('advice', '')}")
        elif score > avg * 1.5:
            advice_parts.append(f"{wx_map[wx]}过旺，{explain.get('advice', '')}")
    
    return {
        "scores": wuxing_strength,
        "strongest": {"element": wx_map[strongest[0]], "score": strongest[1]},
        "weakest": {"element": wx_map[weakest[0]], "score": weakest[1]},
        "analysis_key": "wx_analysis_strong_" + strong_wx + "_weak_" + weak_wx if balance_parts else "wx_analysis_balanced",
        "advice": advice_parts if advice_parts else ["五行相对平衡，保持即可。"],
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
        return {"analysis": "无法进行十神分析。"}
    
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
            "shishen_key": f"shishen_{shishen}",
            "meaning_key": f"shishen_{shishen}_meaning",
            "personality_key": f"shishen_{shishen}_personality",
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
        return {"analysis": "无法进行性格分析。"}
    
    from core.analysis import STEM_ELEMENT
    
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
        return {"advice": "无法生成人生建议。"}
    
    from core.analysis import STEM_ELEMENT
    
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
        "wood": "advice_career_wood",
        "fire": "advice_career_fire",
        "earth": "advice_career_earth",
        "metal": "advice_career_metal",
        "water": "advice_career_water"
    }
    base_key = career_map.get(element, "advice_career_default")
    if "strong" in body_strength:
        return base_key + "_strong"
    else:
        return base_key + "_weak"


def _get_wealth_advice(element, wuxing_strength):
    """财运建议"""
    wealth_map = {
        "wood": "advice_wealth_wood",
        "fire": "advice_wealth_fire",
        "earth": "advice_wealth_earth",
        "metal": "advice_wealth_metal",
        "water": "advice_wealth_water"
    }
    return wealth_map.get(element, "advice_wealth_default")


def _get_relationship_advice(element, wuxing_strength):
    """感情建议"""
    relationship_map = {
        "wood": "advice_love_wood",
        "fire": "advice_love_fire",
        "earth": "advice_love_earth",
        "metal": "advice_love_metal",
        "water": "advice_love_water"
    }
    return relationship_map.get(element, "advice_love_default")


def _get_health_advice(element, wuxing_strength):
    """健康建议"""
    health_map = {
        "wood": "advice_health_wood",
        "fire": "advice_health_fire",
        "earth": "advice_health_earth",
        "metal": "advice_health_metal",
        "water": "advice_health_water"
    }
    return health_map.get(element, "advice_health_default")


def _get_study_advice(element, wuxing_strength):
    """学业建议"""
    study_map = {
        "wood": "advice_study_wood",
        "fire": "advice_study_fire",
        "earth": "advice_study_earth",
        "metal": "advice_study_metal",
        "water": "advice_study_water"
    }
    return study_map.get(element, "advice_study_default")


def _get_social_advice(element, shensha_list):
    """社交建议"""
    has_taohua = any(s.get("name_key") == "shensha_taohua_name" for s in shensha_list)
    has_tianyi = any(s.get("name_key") == "shensha_tianyi_name" for s in shensha_list)
    
    social_map = {
        "wood": "advice_social_wood",
        "fire": "advice_social_fire",
        "earth": "advice_social_earth",
        "metal": "advice_social_metal",
        "water": "advice_social_water"
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
