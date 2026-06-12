# core/yongshen_comparator.py
# A1++ 用神对比解释力引擎

from core.history_engine import verify_history_event


def evaluate_explain_power(
    bazi: dict,
    history_events: list,
    strength_info: dict,
    yongshen_info: dict,
    liunian_provider
) -> dict:
    """
    liunian_provider(year) -> {"year": y, "gan": "...", "zhi": "..."}
    """

    hit = 0
    total_score = 0
    details = []

    for h in history_events:
        liunian = liunian_provider(h["year"])

        result = verify_history_event(
            bazi=bazi,
            history_event=h,
            strength_info=strength_info,
            yongshen_info=yongshen_info,
            liunian_data=liunian
        )

        total_score += result["match_score"]

        if result["match_score"] >= 70:
            hit += 1
            details.append(f'{h["year"]} 年：高应期命中')
        else:
            details.append(f'{h["year"]} 年：解释力不足')

    return {
        "hit_rate": round(hit / len(history_events), 2) if history_events else 0,
        "avg_match_score": round(total_score / len(history_events), 1) if history_events else 0,
        "details": details
    }
