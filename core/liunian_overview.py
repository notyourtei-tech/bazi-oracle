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
    根据事件结果，评估风险等级
    """

    risk = 0
    reasons = []

    # 事业压力
    if "压力" in event_result["career"] or "冲突" in event_result["career"]:
        risk += 1
        reasons.append("事业压力明显")

    # 财务风险
    if "风险" in event_result["wealth"] or "破财" in event_result["wealth"]:
        risk += 1
        reasons.append("财务波动风险")

    # 感情冲突
    if "争执" in event_result["relationship"]:
        risk += 1
        reasons.append("人际关系紧张")

    # 健康问题
    if "注意" in event_result["health"] or "失衡" in event_result["health"]:
        risk += 1
        reasons.append("健康需留意")

    # 用神是否受损（简化版）
    if not any(wx in yongshen_info.get("yongshen", []) for wx in ["water", "metal", "wood", "fire", "earth"]):
        risk += 1
        reasons.append("用神未得到有效助力")

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
