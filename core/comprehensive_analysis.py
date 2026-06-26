"""
Comprehensive Multi-Dimension Analysis Engine
Provides detailed analysis for health, love, wealth, career, exams, friendship, etc.
"""
from core.constants import TIANGAN as STEMS, ZHI as BRANCHES, STEM_ELEMENT, GENERATE_CN as GENERATE, OVERCOME_CN as CONTROL

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
        return "comp_stage_childhood"
    if age < 22:
        return "comp_stage_youth"
    if age < 32:
        return "comp_stage_social"
    if age < 42:
        return "comp_stage_career"
    if age < 52:
        return "comp_stage_midlife"
    if age < 62:
        return "comp_stage_mature"
    if age < 72:
        return "comp_stage_later"
    return "comp_stage_retirement"


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
            "comp_events_help_0",
            "comp_events_help_1",
            "comp_events_help_2"
        ],
        "self": [
            "comp_events_self_0",
            "comp_events_self_1",
            "comp_events_self_2"
        ],
        "drain": [
            "comp_events_drain_0",
            "comp_events_drain_1",
            "comp_events_drain_2"
        ],
        "attack": [
            "comp_events_attack_0",
            "comp_events_attack_1",
            "comp_events_attack_2"
        ],
        "stress": [
            "comp_events_stress_0",
            "comp_events_stress_1",
            "comp_events_stress_2"
        ],
        "neutral": [
            "comp_events_neutral_0",
            "comp_events_neutral_1",
            "comp_events_neutral_2"
        ]
    }
    return events.get(rel, events["neutral"])


def _get_watch_out(rel, age):
    """Get things to watch out for."""
    watch = {
        "help": [
            "comp_watch_help_0",
            "comp_watch_help_1",
            "comp_watch_help_2"
        ],
        "self": [
            "comp_watch_self_0",
            "comp_watch_self_1",
            "comp_watch_self_2"
        ],
        "drain": [
            "comp_watch_drain_0",
            "comp_watch_drain_1",
            "comp_watch_drain_2"
        ],
        "attack": [
            "comp_watch_attack_0",
            "comp_watch_attack_1",
            "comp_watch_attack_2"
        ],
        "stress": [
            "comp_watch_stress_0",
            "comp_watch_stress_1",
            "comp_watch_stress_2"
        ],
        "neutral": [
            "comp_watch_neutral_0",
            "comp_watch_neutral_1",
            "comp_watch_neutral_2"
        ]
    }
    return watch.get(rel, watch["neutral"])


def _get_what_to_do(rel, age, stage):
    """Get recommended actions."""
    do = {
        "help": [
            "comp_do_help_0",
            "comp_do_help_1",
            "comp_do_help_2"
        ],
        "self": [
            "comp_do_self_0",
            "comp_do_self_1",
            "comp_do_self_2"
        ],
        "drain": [
            "comp_do_drain_0",
            "comp_do_drain_1",
            "comp_do_drain_2"
        ],
        "attack": [
            "comp_do_attack_0",
            "comp_do_attack_1",
            "comp_do_attack_2"
        ],
        "stress": [
            "comp_do_stress_0",
            "comp_do_stress_1",
            "comp_do_stress_2"
        ],
        "neutral": [
            "comp_do_neutral_0",
            "comp_do_neutral_1",
            "comp_do_neutral_2"
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
