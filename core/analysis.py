# core/analysis.py
# 用五行关系 + 年龄阶段，生成更细致的大运 / 流年分析 + 命格总评
from core.constants import TIANGAN as STEMS, ZHI as BRANCHES, STEM_ELEMENT, GENERATE_CN as GENERATE, OVERCOME_CN as OVERCOME, GENERATED_BY_CN as GENERATED_BY, OVERCOME_BY_CN as OVERCOME_BY


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
    if OVERCOME.get(dm_elem) == other_elem:
        return "attack"    # 我克
    if OVERCOME.get(other_elem) == dm_elem:
        return "stress"    # 克我
    if dm_elem == other_elem:
        return "self"      # 同类
    return "neutral"


def life_stage(age_start: int) -> str:
    """根据年龄段给一个"人生阶段"的标签"""
    if age_start < 12:
        return "analysis_stage_childhood"
    if age_start < 22:
        return "analysis_stage_student"
    if age_start < 32:
        return "analysis_stage_early_career"
    if age_start < 42:
        return "analysis_stage_career_dev"
    if age_start < 52:
        return "analysis_stage_midlife"
    if age_start < 62:
        return "analysis_stage_mature"
    if age_start < 72:
        return "analysis_stage_later_years"
    return "analysis_stage_retirement"


# =======================
# 大运文案模板（更丰富）
# =======================

DAYUN_TPL = {
    "help": [
        "dayun_tpl_help_0",
        "dayun_tpl_help_1",
        "dayun_tpl_help_2",
    ],
    "self": [
        "dayun_tpl_self_0",
        "dayun_tpl_self_1",
        "dayun_tpl_self_2",
    ],
    "attack": [
        "dayun_tpl_attack_0",
        "dayun_tpl_attack_1",
        "dayun_tpl_attack_2",
    ],
    "drain": [
        "dayun_tpl_drain_0",
        "dayun_tpl_drain_1",
        "dayun_tpl_drain_2",
    ],
    "stress": [
        "dayun_tpl_stress_0",
        "dayun_tpl_stress_1",
        "dayun_tpl_stress_2",
    ],
    "neutral": [
        "dayun_tpl_neutral_0",
        "dayun_tpl_neutral_1",
        "dayun_tpl_neutral_2",
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

    # 根据年龄阶段加一点"当时会发生什么类型事件"的提示
    if age_start < 12:
        extra = "dayun_event_hint_childhood"
    elif age_start < 22:
        extra = "dayun_event_hint_student"
    elif age_start < 32:
        extra = "dayun_event_hint_early_career"
    elif age_start < 42:
        extra = "dayun_event_hint_career_dev"
    elif age_start < 52:
        extra = "dayun_event_hint_midlife"
    else:
        extra = "dayun_event_hint_mature"

    return head + tpl + "（阶段关键词：" + stage + "）" + extra


# =======================
# 流年文案模板（更细）
# =======================

LIUNIAN_TPL = {
    "help": [
        "liunian_tpl_help_0",
        "liunian_tpl_help_1",
        "liunian_tpl_help_2",
    ],
    "self": [
        "liunian_tpl_self_0",
        "liunian_tpl_self_1",
        "liunian_tpl_self_2",
    ],
    "attack": [
        "liunian_tpl_attack_0",
        "liunian_tpl_attack_1",
        "liunian_tpl_attack_2",
    ],
    "drain": [
        "liunian_tpl_drain_0",
        "liunian_tpl_drain_1",
        "liunian_tpl_drain_2",
    ],
    "stress": [
        "liunian_tpl_stress_0",
        "liunian_tpl_stress_1",
        "liunian_tpl_stress_2",
    ],
    "neutral": [
        "liunian_tpl_neutral_0",
        "liunian_tpl_neutral_1",
        "liunian_tpl_neutral_2",
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
        extra = "liunian_event_hint_child"
    elif age < 28:
        extra = "liunian_event_hint_youth"
    elif age < 38:
        extra = "liunian_event_hint_adult"
    elif age < 48:
        extra = "liunian_event_hint_middle"
    elif age < 60:
        extra = "liunian_event_hint_senior"
    else:
        extra = "liunian_event_hint_elderly"

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
    非传统严谨版，只是给用户一点"神煞味道"的说明。
    """
    stars = []

    # 桃花：感情、人缘比较活跃
    if day_zhi in ["子", "午", "卯", "酉"]:
        stars.append("shensha_text_taohua")

    # 文昌：学习、写作、考试
    if day_zhi in ["寅", "卯", "辰", "巳"]:
        stars.append("shensha_text_wenchang")

    # 驿马：动荡、奔波
    if day_zhi in ["申", "子", "辰"]:
        stars.append("shensha_text_yima")

    # 华盖：思考多，比较独立
    if day_zhi in ["戌", "丑", "辰", "未"]:
        stars.append("shensha_text_huagai")

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
