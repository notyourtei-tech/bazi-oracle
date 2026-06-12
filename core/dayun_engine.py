def build_dayun_story(dayun_list, base_info):
    """
    dayun_list: [{start_year,end_year,gan_zhi,element},...]
    base_info:  payload["bazi"]["wuxing_strength"] 等
    """
    out = []
    wux = base_info.get("wuxing_strength", {})
    strong = sorted(wux.items(), key=lambda x: x[1], reverse=True)
    weak = sorted(wux.items(), key=lambda x: x[1])
    strong_el = strong[0][0] if strong else "未知"
    weak_el = weak[0][0] if weak else "未知"

    for idx, d in enumerate(dayun_list):
        start_y = d["start_year"]
        end_y = d["end_year"]
        gz = d["gan_zhi"]
        el = d.get("element", "未知")

        # “真人口吻”模板：每段都不一样（用 idx 做微扰）
        if idx % 3 == 0:
            tone = "这十年像换挡：外部节奏会变快，你会被推着做决定。"
        elif idx % 3 == 1:
            tone = "这十年像打磨：不一定轰轰烈烈，但会把你的底盘练硬。"
        else:
            tone = "这十年像收成：前面种下的东西，会在这段时间显现结果。"

        # 五行主题落地
        if el == weak_el:
            theme = f"这步运补你最弱的「{weak_el}」，通常意味着：你开始学会用新的方式解决老问题。"
        elif el == strong_el:
            theme = f"这步运放大你最强的「{strong_el}」，机会更集中，但也更容易“过度用力”。"
        else:
            theme = f"这步运带来「{el}」的气场，会让你在某些领域更顺手。"

        # 关键词：更像命师的提点
        keywords = []
        if idx < 2:
            keywords += ["基础重建", "环境变化", "学习/迁移"]
        elif idx < 5:
            keywords += ["事业成型", "资源整合", "人脉筛选"]
        else:
            keywords += ["位置与权责", "长期资产", "生活方式定型"]

        # 每段给“可回忆”的钩子
        hook = (
            "你可以回想：这一段里是否出现过——"
            "工作内容明显变化、重要合作关系更替、搬家/转学/转岗、或家庭责任突然加重。"
        )

        story = (
            f"{tone}\n"
            f"{theme}\n"
            f"建议走法：把“大目标”拆成三件能落地的小事（技能、关系、现金流）。\n"
            f"{hook}"
        )

        out.append({
            "start_year": start_y,
            "end_year": end_y,
            "gan_zhi": gz,
            "element_theme": el,
            "keywords": keywords,
            "story": story,
        })

    return out
