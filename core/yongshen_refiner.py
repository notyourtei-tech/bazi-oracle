# core/yongshen_refiner.py
# A1+ 用神修正建议引擎（不会直接改原用神）
from core.constants import GAN_WUXING, SHENG, KE


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
            "message": "yongshen_msg_insufficient_data",
            "suggestion": None
        }

    # === 统计高应期 ===
    high_hit_years = [
        h for h in history_results if h.get("match_score", 0) >= 70
    ]

    if len(high_hit_years) < 2:
        return {
            "status": "not_needed",
            "message": "yongshen_msg_not_needed",
            "suggestion": None
        }

    # === 统计问题来源 ===
    issue_counter = {}
    for h in high_hit_years:
        tags = h.get("liunian_event", {}).get("risk_tags", {})
        for k in ["career", "wealth", "relationship", "health"]:
            if tags.get(k):
                issue_counter[k] = issue_counter.get(k, 0) + 1

    # === 判断是否集中在某一类问题 ===
    major_issue = max(issue_counter, key=issue_counter.get)

    # === 修正策略 ===
    suggestion = None
    reason = ""

    if major_issue in ["health", "relationship"]:
        if xishen:
            suggestion = xishen[0]
            reason = "yongshen_reason_consumption"

    elif major_issue == "career":
        if jishen and jishen[0] in KE:
            suggestion = KE[jishen[0]]
            reason = "yongshen_reason_career_blocked"

    else:
        return {
            "status": "no_clear_pattern",
            "message": "yongshen_msg_no_pattern",
            "suggestion": None
        }

    if not suggestion or suggestion in original:
        return {
            "status": "no_change",
            "message": "yongshen_msg_no_change",
            "suggestion": None
        }

    return {
        "status": "suggest_revision",
        "original_yongshen": original,
        "suggested_yongshen": suggestion,
        "reason": reason,
        "note": "yongshen_note"
    }
