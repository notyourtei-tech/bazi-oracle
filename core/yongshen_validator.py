# core/yongshen_validator.py
# 用神准确度自校验引擎（A1）


def evaluate_yongshen_accuracy(
    yongshen_info: dict,
    history_results: list
) -> dict:
    """
    history_results:
    [
      {
        "year": 2021,
        "match_score": 80,
        "liunian_event": {...}
      }
    ]
    """

    yongshen = yongshen_info.get("yongshen", [])
    hit = 0
    total = len(history_results)

    reasons = []

    for h in history_results:
        if h["match_score"] >= 70:
            hit += 1
            reasons.append(
                f"{h['year']} 年为高应期，用神体系可解释"
            )

    accuracy = round(hit / total, 2) if total > 0 else 0

    verdict = (
        "用神判断可靠"
        if accuracy >= 0.6
        else "用神需调整（可能从喜神中取用）"
    )

    return {
        "accuracy": accuracy,
        "verdict": verdict,
        "explain": reasons
    }
