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
    tags = event_result.get("risk_tags", {})

    # === 事件类型匹配 ===
    if event_type == "job_change":
        if tags.get("career"):
            match_score += 40
            reason.append("history_reason_career_change")

    elif event_type == "breakup":
        if tags.get("relationship"):
            match_score += 40
            reason.append("history_reason_relationship_conflict")

    elif event_type == "illness":
        if tags.get("health"):
            match_score += 40
            reason.append("history_reason_health_imbalance")

    elif event_type == "study":
        if tags.get("career"):
            match_score += 40
            reason.append("history_reason_study_tendency")

    # === 用神是否被冲 ===
    if liunian_data["gan"] not in yongshen_info.get("yongshen", []):
        match_score += 20
        reason.append("history_reason_yongshen_unsupported")

    # === 身强身弱逻辑 ===
    if strength_info["strength"] == "weak":
        match_score += 10
        reason.append("history_reason_body_weak")

    return {
        "year": history_event["year"],
        "event_type": history_event["type"],
        "match_score": min(match_score, 100),
        "analysis": reason,
        "liunian_event": event_result
    }
