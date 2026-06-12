# core/history_engine.py
# 历史事件验证引擎（V1）

from core.event_engine import map_liunian_event


def verify_history_event(
    bazi: dict,
    history_event: dict,
    strength_info: dict,
    yongshen_info: dict,
    liunian_data: dict
) -> dict:
    """
    history_event 示例：
    {
        "year": 2021,
        "type": "job_change",   # job_change / breakup / illness / study
        "description": "换工作"
    }

    liunian_data 示例：
    {
        "year": 2021,
        "gan": "辛",
        "zhi": "丑"
    }
    """

    event_result = map_liunian_event(
        bazi=bazi,
        liunian=liunian_data,
        strength_info=strength_info,
        yongshen_info=yongshen_info
    )

    match_score = 0
    reason = []

    event_type = history_event.get("type")

    # === 事件类型匹配 ===
    if event_type == "job_change":
        if "事业" in event_result["career"] or "压力" in event_result["career"]:
            match_score += 40
            reason.append("该年事业宫有明显变动信号")

    elif event_type == "breakup":
        if "争执" in event_result["relationship"] or "距离" in event_result["relationship"]:
            match_score += 40
            reason.append("该年人际/感情出现冲突信息")

    elif event_type == "illness":
        if "注意" in event_result["health"]:
            match_score += 40
            reason.append("该年健康五行失衡明显")

    elif event_type == "study":
        if "考试" in event_result["career"] or "学习" in event_result["career"]:
            match_score += 40
            reason.append("该年有学习与积累倾向")

    # === 用神是否被冲 ===
    if liunian_data["gan"] not in yongshen_info.get("yongshen", []):
        match_score += 20
        reason.append("流年未助用神，容易出事应变")

    # === 身强身弱逻辑 ===
    if strength_info["strength"] == "weak":
        match_score += 10
        reason.append("日主偏弱，遇变动年份更易应事")

    return {
        "year": history_event["year"],
        "event_type": history_event["type"],
        "match_score": min(match_score, 100),
        "analysis": reason,
        "liunian_event": event_result
    }
