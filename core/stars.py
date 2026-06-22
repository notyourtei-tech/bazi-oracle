# core/stars.py
# 神煞计算模块（接口统一）

def get_stars(bazi):
    """
    bazi: dict，由 bazi_calc 生成的完整八字信息
    return: dict，神煞名称 -> 解释

    TODO: This function returns hardcoded placeholder data.
    Real star/shensha calculation based on the bazi input is not yet implemented.
    """
    # WARNING: Returning hardcoded data. This does not reflect actual bazi analysis.
    return {
        "天乙贵人": {
            "level": "吉",
            "desc": "一生多遇贵人相助，关键时刻有人拉你一把。",
            "hint": "遇事不必单打独斗，向外求助反而更顺。"
        },
        "文昌": {
            "level": "吉",
            "desc": "学习力强，理解力好，适合深度思考型工作。",
            "hint": "读书、考试、研究、写作都对你有利。"
        }
    }
