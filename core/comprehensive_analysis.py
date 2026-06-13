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

# 各维度的详细分析模板
HEALTH_ANALYSIS = {
    "stress": {
        "summary": "健康压力较大，需特别注意身体信号",
        "details": [
            "身体容易出现疲劳、失眠、肠胃不适等症状",
            "长期压力可能导致免疫力下降，容易感冒或过敏",
            "建议定期体检，关注心脑血管和消化系统",
            "适合做一些温和的运动如瑜伽、散步来缓解压力"
        ],
        "advice": "注意休息，避免过度劳累，保持规律作息"
    },
    "drain": {
        "summary": "精力消耗较大，需要补充能量",
        "details": [
            "容易感到疲惫，做事缺乏持久力",
            "可能因为忙碌而忽视饮食和运动",
            "呼吸系统和皮肤需要特别关注",
            "适合通过冥想、深呼吸来恢复精力"
        ],
        "advice": "合理安排工作和休息，多补充营养"
    },
    "attack": {
        "summary": "身体有被消耗的倾向，注意保养",
        "details": [
            "容易出现意外伤害或手术情况",
            "肝胆系统需要特别关注",
            "运动时要注意安全，避免高风险活动",
            "适合定期做健康检查，早发现早治疗"
        ],
        "advice": "注意安全，定期体检，保持健康生活方式"
    },
    "help": {
        "summary": "健康状况整体良好，精力充沛",
        "details": [
            "身体抵抗力较强，恢复能力好",
            "精力充沛，适合保持运动习惯",
            "整体健康运势上升，适合开始新的健身计划",
            "保持乐观心态对健康有正面影响"
        ],
        "advice": "保持良好作息，适度运动，预防胜于治疗"
    },
    "self": {
        "summary": "健康状况平稳，但需注意情绪影响",
        "details": [
            "身体机能正常，但情绪波动可能影响健康",
            "容易因为压力大而出现头痛、失眠",
            "适合通过运动释放压力，保持心情愉悦",
            "注意不要因为忙碌而忽视身体信号"
        ],
        "advice": "关注情绪健康，适当放松，保持身心平衡"
    },
    "neutral": {
        "summary": "健康状况一般，需要注意保养",
        "details": [
            "整体健康无大碍，但需注意日常保养",
            "容易出现小毛病，如感冒、肠胃不适",
            "适合养成规律的运动和饮食习惯",
            "定期体检可以帮助及时发现问题"
        ],
        "advice": "保持健康生活方式，定期体检"
    }
}

LOVE_ANALYSIS = {
    "stress": {
        "summary": "感情运势有压力，需要用心经营",
        "details": [
            "容易遇到感情上的考验，可能有争吵或冷战",
            "单身者可能遇到不太合适的对象，需要谨慎选择",
            "已有伴侣的需要多沟通，避免误会积累",
            "适合在感情中保持理性，不要冲动做决定"
        ],
        "advice": "多沟通、多理解，感情需要双方共同维护"
    },
    "drain": {
        "summary": "感情运势一般，需要付出更多努力",
        "details": [
            "桃花运不算旺盛，需要主动出击",
            "已有伴侣的可能感到平淡，需要制造惊喜",
            "适合在感情中多付出，用行动证明心意",
            "不要因为忙碌而忽视另一半的感受"
        ],
        "advice": "主动表达爱意，用行动维护感情"
    },
    "attack": {
        "summary": "感情运势起伏较大，需要谨慎处理",
        "details": [
            "容易遇到感情上的竞争或第三者问题",
            "单身者可能遇到烂桃花，需要擦亮眼睛",
            "已有伴侣的需要处理好与其他异性的关系",
            "适合在感情中保持清醒，不要被表象迷惑"
        ],
        "advice": "保持忠诚，处理好边界问题"
    },
    "help": {
        "summary": "感情运势很好，桃花运旺盛",
        "details": [
            "单身者容易遇到心仪的对象，脱单机会大",
            "已有伴侣的感情会更加甜蜜，适合考虑进一步发展",
            "社交场合容易遇到有缘人，多参加活动",
            "适合表达心意，主动追求幸福"
        ],
        "advice": "珍惜缘分，勇敢追求爱情"
    },
    "self": {
        "summary": "感情运势平稳，适合按自己节奏发展",
        "details": [
            "桃花运一般，但质量不错",
            "适合在感情中保持自我，不要为了迎合而改变",
            "单身者可以通过兴趣爱好认识志同道合的人",
            "已有伴侣的适合一起做喜欢的事情"
        ],
        "advice": "保持自我，顺其自然"
    },
    "neutral": {
        "summary": "感情运势一般，需要耐心等待",
        "details": [
            "桃花运不强不弱，需要主动创造机会",
            "已有伴侣的感情需要维护，不能掉以轻心",
            "适合在感情中多观察，不要急于确定关系",
            "保持开放心态，缘分到了自然会有结果"
        ],
        "advice": "耐心等待，用心经营"
    }
}

WEALTH_ANALYSIS = {
    "stress": {
        "summary": "财运有压力，需要谨慎理财",
        "details": [
            "容易遇到财务上的困难或意外支出",
            "投资需要特别谨慎，避免高风险项目",
            "适合保守理财，不要冲动消费",
            "可能因为健康或家庭问题导致财务压力"
        ],
        "advice": "控制支出，避免冲动消费，谨慎投资"
    },
    "drain": {
        "summary": "财运一般，收入稳定但增长有限",
        "details": [
            "收入来源稳定，但难有大的突破",
            "适合通过学习新技能来增加收入渠道",
            "不要寄希望于一夜暴富，稳扎稳打更实际",
            "适合做长期投资规划，不要频繁操作"
        ],
        "advice": "开源节流，提升技能，做好长期规划"
    },
    "attack": {
        "summary": "财运有风险，需要谨慎决策",
        "details": [
            "容易遇到财务上的竞争或损失",
            "投资需要特别小心，避免跟风",
            "适合保守理财，不要借贷投资",
            "可能因为人际纠纷导致财务问题"
        ],
        "advice": "保持理性，避免冲动决策，做好风险管理"
    },
    "help": {
        "summary": "财运很好，有意外之财的机会",
        "details": [
            "容易获得意外收入或投资收益",
            "适合抓住机会，但不要过于贪心",
            "可能会有人提供好的投资机会或合作",
            "适合做一些稳健的投资，把握时机"
        ],
        "advice": "抓住机会，但保持理性，不要贪心"
    },
    "self": {
        "summary": "财运平稳，适合按部就班",
        "details": [
            "收入稳定，不会有大的波动",
            "适合做好财务规划，量入为出",
            "可以通过兼职或副业增加收入",
            "不要进行高风险投资"
        ],
        "advice": "做好财务规划，稳步积累"
    },
    "neutral": {
        "summary": "财运一般，需要努力创造",
        "details": [
            "不会有大的财务突破，但也不会有大的损失",
            "适合通过努力工作来增加收入",
            "可以尝试新的理财方式，但要谨慎",
            "保持良好的消费习惯很重要"
        ],
        "advice": "努力工作，合理理财"
    }
}

CAREER_ANALYSIS = {
    "stress": {
        "summary": "事业压力较大，需要调整心态",
        "details": [
            "容易遇到工作上的困难或挑战",
            "可能面临失业、降薪或工作变动",
            "适合在逆境中锻炼能力，不要轻言放弃",
            "可能需要学习新技能来适应变化"
        ],
        "advice": "保持积极心态，在困难中成长"
    },
    "drain": {
        "summary": "事业运势一般，需要默默耕耘",
        "details": [
            "付出很多但回报可能不明显",
            "适合学习新技能，为未来发展打基础",
            "不要期望一步登天，稳扎稳打更实际",
            "适合在现有岗位上深耕，积累经验"
        ],
        "advice": "耐心积累，厚积薄发"
    },
    "attack": {
        "summary": "事业有竞争，需要提升实力",
        "details": [
            "容易遇到职场竞争或人际关系问题",
            "可能面临升职加薪的机会，但需要争取",
            "适合提升专业能力，增强竞争力",
            "处理好与同事和上司的关系很重要"
        ],
        "advice": "提升实力，处理好人际关系"
    },
    "help": {
        "summary": "事业运势很好，有贵人相助",
        "details": [
            "容易得到上司或同事的帮助和赏识",
            "适合主动争取机会，展示自己的能力",
            "可能会有升职加薪或跳槽的好机会",
            "适合拓展人脉，寻找新的发展方向"
        ],
        "advice": "抓住机会，主动出击"
    },
    "self": {
        "summary": "事业运势平稳，适合按自己节奏发展",
        "details": [
            "工作稳定，不会有大的变动",
            "适合在现有领域深耕，成为专家",
            "可以通过学习提升自己的价值",
            "不要为了追求速度而忽视质量"
        ],
        "advice": "专注深耕，提升专业能力"
    },
    "neutral": {
        "summary": "事业运势一般，需要主动创造机会",
        "details": [
            "工作不会有大的突破，但也不会有大的问题",
            "适合在稳定中寻求发展机会",
            "可以尝试新的工作方式或领域",
            "保持学习的心态很重要"
        ],
        "advice": "保持学习，寻找机会"
    }
}

EXAM_ANALYSIS = {
    "stress": {
        "summary": "考试运势有压力，需要更加努力",
        "details": [
            "学习状态可能不稳定，容易分心",
            "考试时可能紧张，影响发挥",
            "适合制定详细的学习计划，按部就班",
            "多做模拟练习，增强信心"
        ],
        "advice": "制定计划，多练习，保持良好心态"
    },
    "drain": {
        "summary": "考试运势一般，需要付出更多努力",
        "details": [
            "学习效率可能不高，需要调整方法",
            "容易感到疲惫，影响学习状态",
            "适合找到适合自己的学习方法",
            "不要急于求成，稳扎稳打"
        ],
        "advice": "找到适合的学习方法，保持耐心"
    },
    "attack": {
        "summary": "考试有竞争，需要提升实力",
        "details": [
            "竞争对手较多，需要更加努力",
            "可能遇到难题或意外情况",
            "适合多做练习，提升应试能力",
            "保持冷静，不要被压力影响"
        ],
        "advice": "提升实力，保持冷静"
    },
    "help": {
        "summary": "考试运势很好，容易取得好成绩",
        "details": [
            "学习状态好，理解能力强",
            "考试时容易超常发挥",
            "适合参加重要的考试或比赛",
            "保持自信，正常发挥就好"
        ],
        "advice": "保持状态，自信应考"
    },
    "self": {
        "summary": "考试运势平稳，适合按自己节奏学习",
        "details": [
            "学习状态一般，需要保持专注",
            "适合制定计划，按部就班地学习",
            "不要给自己太大压力",
            "保持良好的学习习惯"
        ],
        "advice": "保持专注，按计划学习"
    },
    "neutral": {
        "summary": "考试运势一般，需要努力创造条件",
        "details": [
            "学习效率一般，需要找到方法",
            "适合多做练习，积累经验",
            "不要寄希望于运气，实力才是关键",
            "保持良好的学习状态"
        ],
        "advice": "努力学习，提升实力"
    }
}

FRIENDSHIP_ANALYSIS = {
    "stress": {
        "summary": "人际关系有压力，需要注意处理",
        "details": [
            "容易与朋友产生误会或矛盾",
            "可能因为利益问题影响友谊",
            "适合多沟通，化解误会",
            "不要因为小事而伤害友谊"
        ],
        "advice": "多沟通，珍惜友谊"
    },
    "drain": {
        "summary": "人际关系一般，需要主动维护",
        "details": [
            "朋友可能不太主动联系，需要你主动",
            "容易因为忙碌而忽视朋友",
            "适合定期与朋友聚会，保持联系",
            "不要因为忙碌而失去朋友"
        ],
        "advice": "主动联系，维护友谊"
    },
    "attack": {
        "summary": "人际关系有竞争，需要谨慎处理",
        "details": [
            "容易遇到朋友间的竞争或嫉妒",
            "可能因为利益问题影响关系",
            "适合保持距离，不要过度投入",
            "处理好边界问题很重要"
        ],
        "advice": "保持理性，处理好边界"
    },
    "help": {
        "summary": "人际关系很好，朋友运旺盛",
        "details": [
            "容易结交新朋友，友谊运上升",
            "朋友会给你带来帮助和支持",
            "适合多参加社交活动，拓展人脉",
            "珍惜现有的友谊，感恩朋友"
        ],
        "advice": "珍惜友谊，感恩朋友"
    },
    "self": {
        "summary": "人际关系平稳，适合按自己节奏发展",
        "details": [
            "朋友圈稳定，不会有大的变动",
            "适合维护现有友谊，不需要刻意拓展",
            "可以通过共同爱好加深友谊",
            "保持真诚，友谊自然会持久"
        ],
        "advice": "保持真诚，维护友谊"
    },
    "neutral": {
        "summary": "人际关系一般，需要主动创造机会",
        "details": [
            "朋友联系可能不多，需要主动",
            "适合通过活动认识新朋友",
            "保持开放心态，接纳不同类型的人",
            "真诚对待每一个朋友"
        ],
        "advice": "主动社交，真诚待人"
    }
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
