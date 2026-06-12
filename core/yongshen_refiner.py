# core/yongshen_refiner.py
# A1+ 用神修正建议引擎（不会直接改原用神）

GAN_WUXING = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water"
}

SHENG = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood"
}

KE = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood"
}


def refine_yongshen(
    bazi: dict,
    yongshen_info: dict,
    history_results: list
) -> dict:
    """
    history_results:
    [
      {
        "year": 2021,
        "match_score": 85,
        "liunian_event": {...}
      }
    ]
    """

    original = yongshen_info.get("yongshen", [])
    xishen = yongshen_info.get("xishen", [])
    jishen = yongshen_info.get("jishen", [])

    if not history_results:
        return {
            "status": "insufficient_data",
            "message": "历史事件不足，无法修正用神",
            "suggestion": None
        }

    # === 统计高应期 ===
    high_hit_years = [
        h for h in history_results if h.get("match_score", 0) >= 70
    ]

    if len(high_hit_years) < 2:
        return {
            "status": "not_needed",
            "message": "当前用神解释力尚可，无需修正",
            "suggestion": None
        }

    # === 统计问题来源 ===
    issue_counter = {}
    for h in high_hit_years:
        event = h.get("liunian_event", {})
        for k in ["career", "wealth", "relationship", "health"]:
            text = event.get(k, "")
            if "冲" in text or "失衡" in text or "压力" in text:
                issue_counter[k] = issue_counter.get(k, 0) + 1

    # === 判断是否集中在某一类问题 ===
    major_issue = max(issue_counter, key=issue_counter.get)

    # === 修正策略 ===
    suggestion = None
    reason = ""

    if major_issue in ["health", "relationship"]:
        # 身体 / 人际反复出问题 → 优先考虑「生我之神」
        if xishen:
            suggestion = xishen[0]
            reason = "历史高应期多集中在消耗层面，建议从喜神中取生扶之神为新用神候选"

    elif major_issue == "career":
        # 事业反复受阻 → 考虑制约过旺之气
        if jishen:
            suggestion = KE[jishen[0]]
            reason = "事业反复受阻，推测过旺之气未受制，建议取其克神为候选用神"

    else:
        return {
            "status": "no_clear_pattern",
            "message": "事件类型分散，暂不建议修正",
            "suggestion": None
        }

    if not suggestion or suggestion in original:
        return {
            "status": "no_change",
            "message": "修正建议与原用神一致，无需调整",
            "suggestion": None
        }

    return {
        "status": "suggest_revision",
        "original_yongshen": original,
        "suggested_yongshen": suggestion,
        "reason": reason,
        "note": "该结果为系统建议，需结合人工判断确认"
    }
