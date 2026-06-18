"""
Comprehensive Multi-Dimension Analysis Engine
Provides detailed analysis for health, love, wealth, career, exams, friendship, etc.
"""

STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

STEM_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}

GENERATE = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROL = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# 各维度的详细分析模板 - 使用 i18n key
HEALTH_ANALYSIS = {
    "stress": {"summary_key": "comp_health_stress", "advice_key": "comp_health_stress_advice"},
    "drain": {"summary_key": "comp_health_drain", "advice_key": "comp_health_drain_advice"},
    "attack": {"summary_key": "comp_health_attack", "advice_key": "comp_health_attack_advice"},
    "help": {"summary_key": "comp_health_help", "advice_key": "comp_health_help_advice"},
    "self": {"summary_key": "comp_health_self", "advice_key": "comp_health_self_advice"},
    "neutral": {"summary_key": "comp_health_neutral", "advice_key": "comp_health_neutral_advice"},
}

LOVE_ANALYSIS = {
    "stress": {"summary_key": "comp_love_stress", "advice_key": "comp_love_stress_advice"},
    "drain": {"summary_key": "comp_love_drain", "advice_key": "comp_love_drain_advice"},
    "attack": {"summary_key": "comp_love_attack", "advice_key": "comp_love_attack_advice"},
    "help": {"summary_key": "comp_love_help", "advice_key": "comp_love_help_advice"},
    "self": {"summary_key": "comp_love_self", "advice_key": "comp_love_self_advice"},
    "neutral": {"summary_key": "comp_love_neutral", "advice_key": "comp_love_neutral_advice"},
}

WEALTH_ANALYSIS = {
    "stress": {"summary_key": "comp_wealth_stress", "advice_key": "comp_wealth_stress_advice"},
    "drain": {"summary_key": "comp_wealth_drain", "advice_key": "comp_wealth_drain_advice"},
    "attack": {"summary_key": "comp_wealth_attack", "advice_key": "comp_wealth_attack_advice"},
    "help": {"summary_key": "comp_wealth_help", "advice_key": "comp_wealth_help_advice"},
    "self": {"summary_key": "comp_wealth_self", "advice_key": "comp_wealth_self_advice"},
    "neutral": {"summary_key": "comp_wealth_neutral", "advice_key": "comp_wealth_neutral_advice"},
}

CAREER_ANALYSIS = {
    "stress": {"summary_key": "comp_career_stress", "advice_key": "comp_career_stress_advice"},
    "drain": {"summary_key": "comp_career_drain", "advice_key": "comp_career_drain_advice"},
    "attack": {"summary_key": "comp_career_attack", "advice_key": "comp_career_attack_advice"},
    "help": {"summary_key": "comp_career_help", "advice_key": "comp_career_help_advice"},
    "self": {"summary_key": "comp_career_self", "advice_key": "comp_career_self_advice"},
    "neutral": {"summary_key": "comp_career_neutral", "advice_key": "comp_career_neutral_advice"},
}

EXAM_ANALYSIS = {
    "stress": {"summary_key": "comp_exam_stress", "advice_key": "comp_exam_stress_advice"},
    "drain": {"summary_key": "comp_exam_drain", "advice_key": "comp_exam_drain_advice"},
    "attack": {"summary_key": "comp_exam_attack", "advice_key": "comp_exam_attack_advice"},
    "help": {"summary_key": "comp_exam_help", "advice_key": "comp_exam_help_advice"},
    "self": {"summary_key": "comp_exam_self", "advice_key": "comp_exam_self_advice"},
    "neutral": {"summary_key": "comp_exam_neutral", "advice_key": "comp_exam_neutral_advice"},
}

FRIENDSHIP_ANALYSIS = {
    "stress": {"summary_key": "comp_friend_stress", "advice_key": "comp_friend_stress_advice"},
    "drain": {"summary_key": "comp_friend_drain", "advice_key": "comp_friend_drain_advice"},
    "attack": {"summary_key": "comp_friend_attack", "advice_key": "comp_friend_attack_advice"},
    "help": {"summary_key": "comp_friend_help", "advice_key": "comp_friend_help_advice"},
    "self": {"summary_key": "comp_friend_self", "advice_key": "comp_friend_self_advice"},
    "neutral": {"summary_key": "comp_friend_neutral", "advice_key": "comp_friend_neutral_advice"},
}


def get_relation(dm_elem, other_elem):
    """Get the wuxing relationship between two elements."""
    if not dm_elem or not other_elem:
        return "neutral"
    if GENERATE.get(other_elem) == dm_elem:
        return "help"
    if GENERATE.get(dm_elem) == other_elem:
        return "drain"
    if CONTROL.get(dm_elem) == other_elem:
        return "attack"
    if CONTROL.get(other_elem) == dm_elem:
        return "stress"
    if dm_elem == other_elem:
        return "self"
    return "neutral"


def get_life_stage(age):
    """Get life stage label based on age."""
    if age < 12:
        return "童年基础期"
    if age < 22:
        return "青春探索期"
    if age < 32:
        return "社会打怪期"
    if age < 42:
        return "事业发展期"
    if age < 52:
        return "中年调整期"
    if age < 62:
        return "成熟收成期"
    if age < 72:
        return "晚年享受期"
    return "养生慢活期"


def analyze_dayun_comprehensive(dayun_data, birth_year, dm_elem):
    """
    Generate comprehensive dayun analysis with multiple dimensions.
    
    Args:
        dayun_data: List of dayun dicts from pipeline
        birth_year: Birth year
        dm_elem: Day master element
    
    Returns:
        List of comprehensive dayun analysis dicts
    """
    results = []
    
    for i, d in enumerate(dayun_data):
        start_year = d.get("start_year", birth_year + 6 + i * 10)
        end_year = d.get("end_year", start_year + 9)
        gz = d.get("gz", "")
        
        # Get the dayun stem element
        dayun_stem = gz[0] if gz else "甲"
        dayun_elem = STEM_ELEMENT.get(dayun_stem, "木")
        
        # Calculate age range
        age_start = start_year - birth_year
        age_end = end_year - birth_year
        life_stage = get_life_stage(age_start)
        
        # Get relationship
        rel = get_relation(dm_elem, dayun_elem)
        
        # Build comprehensive analysis
        health = HEALTH_ANALYSIS.get(rel, HEALTH_ANALYSIS["neutral"])
        love = LOVE_ANALYSIS.get(rel, LOVE_ANALYSIS["neutral"])
        wealth = WEALTH_ANALYSIS.get(rel, WEALTH_ANALYSIS["neutral"])
        career = CAREER_ANALYSIS.get(rel, CAREER_ANALYSIS["neutral"])
        exam = EXAM_ANALYSIS.get(rel, EXAM_ANALYSIS["neutral"])
        friendship = FRIENDSHIP_ANALYSIS.get(rel, FRIENDSHIP_ANALYSIS["neutral"])
        
        # Overall summary
        overall_score = {
            "help": 85, "self": 70, "drain": 55, 
            "attack": 45, "stress": 40, "neutral": 60
        }.get(rel, 60)
        
        # Likely events
        likely_events = _get_likely_events(rel, age_start, life_stage)
        
        # What to watch out for
        watch_out = _get_watch_out(rel, age_start)
        
        # What to do
        what_to_do = _get_what_to_do(rel, age_start, life_stage)
        
        results.append({
            "start_year": start_year,
            "end_year": end_year,
            "gz": gz,
            "theme_key": d.get("theme_key", ""),
            "desc_key": d.get("desc_key", ""),
            "advice_key": d.get("advice_key", ""),
            "liunian_list": d.get("liunian_list", []),
            # Comprehensive analysis
            "age_range": f"{age_start}-{age_end}岁",
            "life_stage": life_stage,
            "overall_score": overall_score,
            "health": health,
            "love": love,
            "wealth": wealth,
            "career": career,
            "exam": exam,
            "friendship": friendship,
            "likely_events": likely_events,
            "watch_out": watch_out,
            "what_to_do": what_to_do,
        })
    
    return results


def _get_likely_events(rel, age, stage):
    """Get likely events based on relationship and age."""
    events = {
        "help": [
            "可能遇到贵人相助，获得好的机会",
            "适合开启新项目或尝试新事物",
            "人际关系顺利，容易得到支持"
        ],
        "self": [
            "可能会有个人成长的重要时刻",
            "适合确立自己的目标和方向",
            "可能会遇到一些挑战但能克服"
        ],
        "drain": [
            "可能会感到忙碌，事情较多",
            "适合学习新技能，为未来做准备",
            "需要耐心，成果会慢慢显现"
        ],
        "attack": [
            "可能会遇到竞争或挑战",
            "适合提升自己的实力",
            "需要处理好人际关系"
        ],
        "stress": [
            "可能会遇到一些压力或困难",
            "需要保持积极心态",
            "适合稳扎稳打，不要冲动"
        ],
        "neutral": [
            "生活按部就班，不会有大的波动",
            "适合做一些日常的事情",
            "保持平常心就好"
        ]
    }
    return events.get(rel, events["neutral"])


def _get_watch_out(rel, age):
    """Get things to watch out for."""
    watch = {
        "help": [
            "虽然运势好，但不要过于自信",
            "珍惜帮助你的人，不要过河拆桥",
            "好运时也要保持谦虚"
        ],
        "self": [
            "不要过于固执，要学会倾听他人",
            "保持开放心态，接受不同意见",
            "注意与家人朋友的沟通"
        ],
        "drain": [
            "不要因为忙碌而忽视健康",
            "学会取舍，不要什么都想做",
            "保持耐心，不要急于求成"
        ],
        "attack": [
            "注意处理好人际关系",
            "不要冲动做决定",
            "保持冷静，理性分析"
        ],
        "stress": [
            "注意身体健康，定期体检",
            "不要给自己太大压力",
            "学会释放压力，保持心情愉悦"
        ],
        "neutral": [
            "保持良好的生活习惯",
            "不要因为平淡而懈怠",
            "持续学习，提升自己"
        ]
    }
    return watch.get(rel, watch["neutral"])


def _get_what_to_do(rel, age, stage):
    """Get recommended actions."""
    do = {
        "help": [
            "主动出击，抓住机会",
            "拓展人脉，结交新朋友",
            "尝试新事物，挑战自己"
        ],
        "self": [
            "确立自己的目标和方向",
            "保持自我，不要随波逐流",
            "提升自己的专业能力"
        ],
        "drain": [
            "学习新技能，为未来做准备",
            "保持耐心，稳扎稳打",
            "做好时间管理，提高效率"
        ],
        "attack": [
            "提升自己的实力",
            "处理好人际关系",
            "保持冷静，理性决策"
        ],
        "stress": [
            "保持积极心态",
            "注意身体健康",
            "稳扎稳打，不要冲动"
        ],
        "neutral": [
            "保持良好的生活习惯",
            "持续学习，提升自己",
            "珍惜身边的人"
        ]
    }
    return do.get(rel, do["neutral"])


def analyze_liunian_comprehensive(liunian_list, birth_year, dm_elem):
    """
    Generate comprehensive liunian analysis with multiple dimensions.
    
    Args:
        liunian_list: List of liunian dicts
        birth_year: Birth year
        dm_elem: Day master element
    
    Returns:
        List of comprehensive liunian analysis dicts
    """
    results = []
    
    for ln in liunian_list:
        year = ln.get("year", 0)
        gz = ln.get("gz", "")
        age = year - birth_year
        
        # Get the year stem element
        year_stem = gz[0] if gz else "甲"
        year_elem = STEM_ELEMENT.get(year_stem, "木")
        
        # Get relationship
        rel = get_relation(dm_elem, year_elem)
        
        # Build comprehensive analysis
        health = HEALTH_ANALYSIS.get(rel, HEALTH_ANALYSIS["neutral"])
        love = LOVE_ANALYSIS.get(rel, LOVE_ANALYSIS["neutral"])
        wealth = WEALTH_ANALYSIS.get(rel, WEALTH_ANALYSIS["neutral"])
        career = CAREER_ANALYSIS.get(rel, CAREER_ANALYSIS["neutral"])
        exam = EXAM_ANALYSIS.get(rel, EXAM_ANALYSIS["neutral"])
        friendship = FRIENDSHIP_ANALYSIS.get(rel, FRIENDSHIP_ANALYSIS["neutral"])
        
        # Overall score
        overall_score = {
            "help": 85, "self": 70, "drain": 55, 
            "attack": 45, "stress": 40, "neutral": 60
        }.get(rel, 60)
        
        # Likely events
        likely_events = _get_likely_events(rel, age, get_life_stage(age))
        
        # What to watch out for
        watch_out = _get_watch_out(rel, age)
        
        # What to do
        what_to_do = _get_what_to_do(rel, age, get_life_stage(age))
        
        results.append({
            "year": year,
            "gz": gz,
            "theme_key": ln.get("theme_key", ""),
            "desc_key": ln.get("desc_key", ""),
            "event_hint_key": ln.get("event_hint_key", ""),
            # Comprehensive analysis
            "age": age,
            "life_stage": get_life_stage(age),
            "overall_score": overall_score,
            "health": health,
            "love": love,
            "wealth": wealth,
            "career": career,
            "exam": exam,
            "friendship": friendship,
            "likely_events": likely_events,
            "watch_out": watch_out,
            "what_to_do": what_to_do,
        })
    
    return results
