# core/analysis.py
# 用五行关系 + 年龄阶段，生成更细致的大运 / 流年分析 + 命格总评

STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

STEM_ELEMENT = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

GENERATE = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木",
}

CONTROL = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}


def year_ganzhi(year: int) -> str:
    """用 1984 甲子年为基准算某年的干支"""
    base = 1984
    offset = (year - base) % 60
    stem = STEMS[offset % 10]
    branch = BRANCHES[offset % 12]
    return stem + branch


def stem_to_element(stem: str) -> str:
    return STEM_ELEMENT.get(stem, "")


def relation_between(dm_elem: str, other_elem: str) -> str:
    """
    五行关系：
      help   生我
      drain  我生
      attack 我克
      stress 克我
      self   同元素
    """
    if not dm_elem or not other_elem:
        return "neutral"

    if GENERATE.get(other_elem) == dm_elem:
        return "help"      # 生我
    if GENERATE.get(dm_elem) == other_elem:
        return "drain"     # 我生
    if CONTROL.get(dm_elem) == other_elem:
        return "attack"    # 我克
    if CONTROL.get(other_elem) == dm_elem:
        return "stress"    # 克我
    if dm_elem == other_elem:
        return "self"      # 同类
    return "neutral"


def life_stage(age_start: int) -> str:
    """根据年龄段给一个“人生阶段”的标签"""
    if age_start < 12:
        return "童年 / 基础打底期"
    if age_start < 22:
        return "学生 / 青春探索期"
    if age_start < 32:
        return "初入社会 / 打怪升级期"
    if age_start < 42:
        return "事业发展 / 定位期"
    if age_start < 52:
        return "中年调整 / 结构升级期"
    if age_start < 62:
        return "成熟收成 / 布局期"
    if age_start < 72:
        return "晚年享受 / 传承期"
    return "养生慢活 / 回顾期"


# =======================
# 大运文案模板（更丰富）
# =======================

DAYUN_TPL = {
    "help": [
        "这一运贵人明显，适合主动出击，多去结识新圈子、上新项目。只要你肯迈开步，机会就会自己浮上来。",
        "整体顺势而上，资源、人脉都更愿意靠近你。适合换赛道、升学深造、跳槽到更大的平台。",
        "适合把之前积累的东西拿出来用，用好贵人和平台，多去争取头衔、证书、职级上的抬升。",
    ],
    "self": [
        "这一运自我意识变强，会更想按自己的想法活。适合确立个人风格、IP 或职业方向，但不要把所有桥都烧掉。",
        "会有『我就想试一次』的冲动，适合创业、副业、转专业，但务必保留一点安全垫。",
        "容易形成自己的一套价值观，与家庭或环境有些观念拉扯，要学会在坚持和妥协之间找平衡。",
    ],
    "attack": [
        "这是竞争味道很重的一运，容易面对考试、升职、业绩指标或职场斗争。适合冲刺，但要学会用策略而不是硬刚。",
        "外部环境会逼你成长，可能出现换工作、换城市、换圈子等关键节点，趁机修炼谈判力与边界感。",
        "适合主动争取位置，尤其是想走管理、业务一线、业绩导向岗位的，会有比较多打仗的机会。",
    ],
    "drain": [
        "这一运更像『蓄力期』，付出会多于及时回报。适合学习、修行、建作品集，把时间花在能沉淀的东西上。",
        "生活节奏可能有点忙乱，容易一心多用。要学会取舍，不要什么都想兼顾，否则身心容易透支。",
        "适合默默打基础：读书、考证、练技能、调整体质。短期看不出效果，但会在下一两运慢慢体现出来。",
    ],
    "stress": [
        "责任感会被强行拉满，可能要照顾家人、扛家庭经济、面对长期的工作压力。宜稳守，不宜乱赌一把。",
        "这一运容易被现实拽着走，内心压力大时，记得定期运动、倾诉，避免情绪积压变成身体问题。",
        "规则和制度感会变强，适合学会在系统里玩游戏——懂流程、懂汇报、懂如何保护自己。",
    ],
    "neutral": [
        "整体比较平稳，不会特别大起大落。适合慢慢整理人生结构：钱、人、时间、健康都做一些微调。",
        "这一运可以把节奏放得相对舒服，留一点空间给兴趣爱好，顺便看看有没有新的可能性冒出来。",
        "适合做长期但不那么急的事：学一门新的语言、技术、乐器，或者养成真正对你有好处的习惯。",
    ]
}


def build_dayun_text(age_start: int, gz: str, dm_elem: str, yun_elem: str, index: int) -> str:
    """十年一个阶段的大运文字说明（根据五行关系 + 年龄阶段 + 模板轮换）"""
    age_end = age_start + 9
    stage = life_stage(age_start)
    head = f"{age_start}～{age_end}岁（{gz}）阶段："

    rel = relation_between(dm_elem, yun_elem)
    tpl_list = DAYUN_TPL.get(rel, DAYUN_TPL["neutral"])
    tpl = tpl_list[index % len(tpl_list)]

    extra = ""

    # 根据年龄阶段加一点“当时会发生什么类型事件”的提示
    if age_start < 12:
        extra = " 多对应家庭环境、父母工作变动、搬家、升学等，对你的成长气氛影响大。"
    elif age_start < 22:
        extra = " 主要反映在学业、同学圈、人际关系以及早期恋爱体验上。"
    elif age_start < 32:
        extra = " 多与找工作、实习、踏入社会、第一次换工作或独立生活有关。"
    elif age_start < 42:
        extra = " 容易出现事业方向调整、收入结构变化、成家立业等关键选择。"
    elif age_start < 52:
        extra = " 常见主题是家庭责任、房产、子女教育、事业定位再升级。"
    else:
        extra = " 更多体现在健康、生活质量、家庭氛围与内心状态的调整上。"

    return head + tpl + "（阶段关键词：" + stage + "）" + extra


# =======================
# 流年文案模板（更细）
# =======================

LIUNIAN_TPL = {
    "help": [
        "人际助力明显，贵人、老师、上司或客户比较给力，适合主动提出自己的想法。",
        "适合开启新计划：换专业、换组、换工作、搬家、留学等，都容易遇到愿意帮助你的人。",
        "整体氛围偏顺，一些之前卡住的事情容易突然有突破口，可以多试几次。",
    ],
    "self": [
        "自我意愿很强的一年，会特别在意『我真正想要什么』，适合做一些人生方向的决定。",
        "更想按照自己节奏来，不太想被安排。注意和家人、同事在沟通方式上多一点温柔。",
        "容易爆发个人表达欲：想做内容、想发声、想改变形象，是适合重塑自我标签的一年。",
    ],
    "attack": [
        "竞争与对抗感偏重，可能遇到考试、升职、业绩压力，或者感情关系里的硬碰硬。",
        "需要多用策略而不是情绪，适合提升谈判、表达和边界感，学会说“不”。",
        "这一年适合去争，也适合认清哪些东西不值得你继续耗下去，做减法很重要。",
    ],
    "drain": [
        "忙碌奔波，事情很多，容易觉得时间不够用。适合把精力集中在最重要的两三件事上。",
        "学习、考证、做项目、照顾家人等消耗型事务会比较多，别把自己排得太满。",
        "适合静下心来打磨技能或作品，短期虽然累，但对后面一两年很关键。",
    ],
    "stress": [
        "责任和压力感偏重，容易被现实课题推着走：钱、健康、家人、合同等都要上心。",
        "如果身体开始发出信号（失眠、焦虑、暴饮暴食），要认真对待，必要时求助专业资源。",
        "外部要求高的一年，适合把基础打牢、把风险控制好，不太适合做大赌博式的决定。",
    ],
    "neutral": [
        "整体起伏不大，生活比较按部就班。适合修复关系、整理房间和心情，给自己一点喘息空间。",
        "可以用来尝试新兴趣、发展副业雏形，没那么多硬性考核，反而容易实验出新方向。",
        "适合做年度复盘：看看哪些习惯值得保留，哪些人和事可以慢慢放下。",
    ]
}


def build_liunian_text(year: int, gz: str, dm_elem: str, year_elem: str, age: int, index: int) -> str:
    """单年运势说明：根据五行关系 + 年龄段 + 模板轮换"""
    head = f"{year}年（{gz}），大约{age}岁："
    rel = relation_between(dm_elem, year_elem)
    tpl_list = LIUNIAN_TPL.get(rel, LIUNIAN_TPL["neutral"])
    tpl = tpl_list[index % len(tpl_list)]

    # 补一点“事件类型”
    if age < 18:
        extra = " 主题多和读书、考试、同学、人际圈、兴趣班、搬家或父母工作变动有关。"
    elif age < 28:
        extra = " 多和升学、求职、实习、初入社会、人际扩张、早期感情体验相关。"
    elif age < 38:
        extra = " 容易遇到换工作、加薪、转方向、同居或结婚等关键现实选择。"
    elif age < 48:
        extra = " 常见议题是事业稳定度、家庭结构、子女、房产和中期规划。"
    elif age < 60:
        extra = " 多和资产配置、健康管理、子女发展、父母照护相关。"
    else:
        extra = " 更看重生活质量、身体状态与精神愉悦，适合把节奏放慢一点。"

    return head + tpl + extra


# =======================
# 生成大运 / 流年列表
# =======================

def analyze_dayun(ec, birth_year: int):
    """
    按十年一段生成大运解读列表
    起运年龄近似按 6 岁起运来算：
      第一个阶段：6～15 岁
      第二个阶段：16～25 岁
      ...
    """
    dm_gan = ec.getDayGan()
    dm_elem = stem_to_element(dm_gan)

    res = []
    # NOTE: qiyun_age=6 is an approximation. The actual qiyun age should be
    # calculated from the birth date's gender, day stem, and month stem using
    # the proper 起运 formula. Pass calculated qiyun_age when available.
    qiyun_age = 6  # 近似起运年龄

    for i in range(0, 9):
        age_start = qiyun_age + i * 10
        mid_age = age_start + 5
        yun_year = birth_year + mid_age
        gz = year_ganzhi(yun_year)
        yun_elem = stem_to_element(gz[0])
        analysis = build_dayun_text(age_start, gz, dm_elem, yun_elem, i)
        res.append({
            "age_start": age_start,
            "gz": gz,
            "analysis": analysis,
        })
    return res


def analyze_liunian(ec, birth_year: int):
    """
    从起运年份开始，到大约 86 岁左右的年度运势。
    """
    dm_gan = ec.getDayGan()
    dm_elem = stem_to_element(dm_gan)

    res = []
    # NOTE: qiyun_age=6 is an approximation. See analyze_dayun() for details.
    qiyun_age = 6
    start_year = birth_year + qiyun_age
    end_year = birth_year + 86

    idx = 0
    for y in range(start_year, end_year + 1):
        gz = year_ganzhi(y)
        year_elem = stem_to_element(gz[0])
        age = y - birth_year
        analysis = build_liunian_text(y, gz, dm_elem, year_elem, age, idx)
        res.append({
            "year": y,
            "gz": gz,
            "analysis": analysis,
        })
        idx += 1
    return res


# -----------------------------------------
# 神煞 + 性格 / 事业 / 感情 综合分析
# -----------------------------------------

def simple_shensha(day_zhi: str):
    """
    非传统严谨版，只是给用户一点“神煞味道”的说明。
    """
    stars = []

    # 桃花：感情、人缘比较活跃
    if day_zhi in ["子", "午", "卯", "酉"]:
        stars.append("桃花：异性缘、人际魅力比较强，容易被注意到。")

    # 文昌：学习、写作、考试
    if day_zhi in ["寅", "卯", "辰", "巳"]:
        stars.append("文昌：头脑灵活，适合学习、写作、设计相关工作。")

    # 驿马：动荡、奔波
    if day_zhi in ["申", "子", "辰"]:
        stars.append("驿马：一生不太安分，容易搬家、换环境、出差或留学。")

    # 华盖：思考多，比较独立
    if day_zhi in ["戌", "丑", "辰", "未"]:
        stars.append("华盖：思考多，比较有主见，也有点孤高感，需要自己的空间。")

    return stars


def analyze_profile(ec):
    """
    综合分析：性格、事业方向、感情风格、健康提醒、神煞提示
    """
    dm_gan = ec.getDayGan()
    dm_zhi = ec.getDayZhi()
    elem = stem_to_element(dm_gan)

    # 阴阳
    yang_stems = ["甲", "丙", "戊", "庚", "壬"]
    yin_yang = "阳" if dm_gan in yang_stems else "阴"

    # 性格基调
    if elem == "木":
        base_personality = "内在带着成长欲望和理想感，重视原则，有时比较直来直去。"
    elif elem == "火":
        base_personality = "性格偏热情直接，情绪反应快，讲感觉，讨厌拖泥带水。"
    elif elem == "土":
        base_personality = "偏稳重现实型，重视安全感与责任感，比较能扛事。"
    elif elem == "金":
        base_personality = "思路偏理性、重规则，判断力强，喜欢清晰与效率。"
    elif elem == "水":
        base_personality = "感受细腻、观察力强，想法多，适合动脑而不是硬扛。"
    else:
        base_personality = "性格比较综合，不会特别偏向某一类。"

    if yin_yang == "阳":
        ext = "整体偏外向、主动，遇事习惯先出手再慢慢调整。"
    else:
        ext = "整体偏含蓄、观察型，习惯先看清局势再出手。"

    personality = f"日主为{yin_yang}{elem}，{base_personality}{ext}"

    # 事业方向
    if elem == "木":
        career = "适合教育、顾问、设计、文字、文化、心理、咨询等与成长相关的行业，也适合和人打交道的工作。"
    elif elem == "火":
        career = "适合需要表现力和热情的工作：销售、公关、直播、自媒体、娱乐、餐饮、活动策划等。"
    elif elem == "土":
        career = "适合稳定、需要耐心与责任感的岗位：行政、财务、人事、不动产、土木、供应链、后台运营等。"
    elif elem == "金":
        career = "适合法律、金融、审计、IT 开发、数据分析、风控、管理岗位等需要判断和决策的工作。"
    elif elem == "水":
        career = "适合资讯、传媒、咨询、心理、外语、跨国业务、流通贸易等需要灵活沟通的领域。"
    else:
        career = "整体行业限制不大，重点是找能持续学习、又不会被完全绑死的方向。"

    # 感情
    if elem in ["木", "火"]:
        love = "感情上比较主动，有感觉就很难装作没事，但也容易因为冲动或热度变化快而起伏较大。"
    elif elem in ["金", "水"]:
        love = "感情里比较重理性与互动质量，不太喜欢黏腻，但希望对方能理解自己的节奏与边界。"
    else:
        love = "感情观偏务实，比较看重稳定与长期打算，有时表达不够浪漫，但心里是记得对方好的。"

    # 健康（大方向）
    if elem == "火":
        health = "注意心血管、血压与熬夜问题，保持规律作息很重要。"
    elif elem == "水":
        health = "注意肾脏、泌尿与睡眠质量，避免长期压力导致失眠。"
    elif elem == "木":
        health = "注意肝胆与眼睛，用电脑时间长记得休息与运动。"
    elif elem == "金":
        health = "注意呼吸道、皮肤与筋骨，久坐要时常活动。"
    else:
        health = "注意脾胃、消化系统与体重管理，饮食尽量规律。"

    # 神煞提示（简易版）
    shensha_list = simple_shensha(dm_zhi)
    if shensha_list:
        shensha_text = "、".join(shensha_list)
    else:
        shensha_text = "命盘神煞分布比较平均，没有特别极端的加分或减分点，更看重自己后天的选择。"

    return {
        "personality": personality,
        "career": career,
        "love": love,
        "health": health,
        "shensha": shensha_text,
    }
