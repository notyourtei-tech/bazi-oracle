# core/liunian_overview.py
# 流年概览 & 风险评估

from core.event_engine import map_liunian_event

GAN_WUXING = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water"
}


def assess_risk(event_result: dict, yongshen_info: dict) -> dict:
    """
    根据事件结果的 risk_tags，评估风险等级
    """
    risk = 0
    reasons = []
    tags = event_result.get("risk_tags", {})

    if tags.get("career"):
        risk += 1
        reasons.append("risk_reason_career_stress")

    if tags.get("wealth"):
        risk += 1
        reasons.append("risk_reason_wealth_risk")

    if tags.get("relationship"):
        risk += 1
        reasons.append("risk_reason_relationship_tension")

    if tags.get("health"):
        risk += 1
        reasons.append("risk_reason_health_attention")

    if tags.get("yongshen"):
        risk += 1
        reasons.append("risk_reason_yongshen_weak")

    # 风险等级
    if risk >= 3:
        level = "high"
    elif risk == 2:
        level = "medium"
    else:
        level = "low"

    return {
        "level": level,
        "score": risk,
        "reasons": reasons
    }


def build_liunian_overview(
    bazi: dict,
    years: list,
    strength_info: dict,
    yongshen_info: dict,
    liunian_provider
) -> list:
    """
    返回：
    [
      {
        "year": 2026,
        "event": {...},
        "risk": {...}
      }
    ]
    """

    overview = []

    for y in years:
        liunian = liunian_provider(y)

        event = map_liunian_event(
            bazi=bazi,
            liunian=liunian,
            strength_info=strength_info,
            yongshen_info=yongshen_info
        )

        risk = assess_risk(event, yongshen_info)

        overview.append({
            "year": y,
            "event": event,
            "risk": risk
        })

    return overview
