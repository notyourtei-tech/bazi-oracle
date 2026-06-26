with open(r'C:\Users\t\Desktop\bazi_app\core\comprehensive_analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace get_life_stage
content = content.replace(
    '        return "\u7ae5\u5e74\u57fa\u7840\u671f"',
    '        return "comp_stage_childhood"'
)
content = content.replace(
    '        return "\u9752\u6625\u63a2\u7d22\u671f"',
    '        return "comp_stage_youth"'
)
content = content.replace(
    '        return "\u793e\u4f1a\u6253\u602a\u671f"',
    '        return "comp_stage_social"'
)
content = content.replace(
    '        return "\u4e8b\u4e1a\u53d1\u5c55\u671f"',
    '        return "comp_stage_career"'
)
content = content.replace(
    '        return "\u4e2d\u5e74\u8c03\u6574\u671f"',
    '        return "comp_stage_midlife"'
)
content = content.replace(
    '        return "\u6210\u719f\u6536\u6210\u671f"',
    '        return "comp_stage_mature"'
)
content = content.replace(
    '        return "\u665a\u5e74\u4eab\u53d7\u671f"',
    '        return "comp_stage_later"'
)
content = content.replace(
    '    return "\u517b\u751f\u6162\u6d3b\u671f"',
    '    return "comp_stage_retirement"'
)

# 2. Replace _get_likely_events
content = content.replace(
    '            "\u53ef\u80fd\u9047\u5230\u8d35\u4eba\u76f8\u52a9\uff0c\u83b7\u5f97\u597d\u7684\u673a\u4f1a"',
    '            "comp_events_help_0"'
)
content = content.replace(
    '            "\u9002\u5408\u5f00\u542f\u65b0\u9879\u76ee\u6216\u5c1d\u8bd5\u65b0\u4e8b\u7269"',
    '            "comp_events_help_1"'
)
content = content.replace(
    '            "\u4eba\u9645\u5173\u7cfb\u987a\u5229\uff0c\u5bb9\u6613\u5f97\u5230\u652f\u6301"',
    '            "comp_events_help_2"'
)
content = content.replace(
    '            "\u53ef\u80fd\u4f1a\u6709\u4e2a\u4eba\u6210\u957f\u7684\u91cd\u8981\u65f6\u523b"',
    '            "comp_events_self_0"'
)
content = content.replace(
    '            "\u9002\u5408\u786e\u7acb\u81ea\u5df1\u7684\u76ee\u6807\u548c\u65b9\u5411"',
    '            "comp_events_self_1"'
)
content = content.replace(
    '            "\u53ef\u80fd\u4f1a\u9047\u5230\u4e00\u4e9b\u6311\u6218\u4f46\u80fd\u514b\u670d"',
    '            "comp_events_self_2"'
)
content = content.replace(
    '            "\u53ef\u80fd\u4f1a\u611f\u5230\u5fd9\u788c\uff0c\u4e8b\u60c5\u8f83\u591a"',
    '            "comp_events_drain_0"'
)
content = content.replace(
    '            "\u9002\u5408\u5b66\u4e60\u65b0\u6280\u80fd\uff0c\u4e3a\u672a\u6765\u505a\u51c6\u5907"',
    '            "comp_events_drain_1"'
)
content = content.replace(
    '            "\u9700\u8981\u8010\u5fc3\uff0c\u6210\u679c\u4f1a\u6162\u6162\u663e\u73b0"',
    '            "comp_events_drain_2"'
)
content = content.replace(
    '            "\u53ef\u80fd\u4f1a\u9047\u5230\u7ade\u4e89\u6216\u6311\u6218"',
    '            "comp_events_attack_0"'
)
content = content.replace(
    '            "\u9002\u5408\u63d0\u5347\u81ea\u5df1\u7684\u5b9e\u529b"',
    '            "comp_events_attack_1"'
)
content = content.replace(
    '            "\u9700\u8981\u5904\u7406\u597d\u4eba\u9645\u5173\u7cfb"',
    '            "comp_events_attack_2"'
)
content = content.replace(
    '            "\u53ef\u80fd\u4f1a\u9047\u5230\u4e00\u4e9b\u538b\u529b\u6216\u56f0\u96be"',
    '            "comp_events_stress_0"'
)
content = content.replace(
    '            "\u9700\u8981\u4fdd\u6301\u79ef\u6781\u5fc3\u6001"',
    '            "comp_events_stress_1"'
)
content = content.replace(
    '            "\u9002\u5408\u7a33\u624e\u7a33\u6253\uff0c\u4e0d\u8981\u51b2\u52a8"',
    '            "comp_events_stress_2"'
)
content = content.replace(
    '            "\u751f\u6d3b\u6309\u90e8\u5c31\u73ed\uff0c\u4e0d\u4f1a\u6709\u5927\u7684\u6ce2\u52a8"',
    '            "comp_events_neutral_0"'
)
content = content.replace(
    '            "\u9002\u5408\u505a\u4e00\u4e9b\u65e5\u5e38\u7684\u4e8b\u60c5"',
    '            "comp_events_neutral_1"'
)
content = content.replace(
    '            "\u4fdd\u6301\u5e38\u5e73\u5fc3\u5c31\u597d"',
    '            "comp_events_neutral_2"'
)

# 3. Replace _get_watch_out
content = content.replace(
    '            "\u867d\u7136\u8fd0\u52bf\u597d\uff0c\u4f46\u4e0d\u8981\u8fc7\u4e8e\u81ea\u4fe1"',
    '            "comp_watch_help_0"'
)
content = content.replace(
    '            "\u73cd\u60dc\u5e2e\u52a9\u4f60\u7684\u4eba\uff0c\u4e0d\u8981\u8fc7\u6cb3\u62c6\u6865"',
    '            "comp_watch_help_1"'
)
content = content.replace(
    '            "\u597d\u8fd0\u65f6\u4e5f\u8981\u4fdd\u6301\u8c26\u865a"',
    '            "comp_watch_help_2"'
)
content = content.replace(
    '            "\u4e0d\u8981\u8fc7\u4e8e\u56fa\u6267\uff0c\u8981\u5b66\u4f1a\u503e\u542c\u4ed6\u4eba"',
    '            "comp_watch_self_0"'
)
content = content.replace(
    '            "\u4fdd\u6301\u5f00\u653e\u5fc3\u6001\uff0c\u63a5\u53d7\u4e0d\u540c\u610f\u89c1"',
    '            "comp_watch_self_1"'
)
content = content.replace(
    '            "\u6ce8\u610f\u4e0e\u5bb6\u4eba\u670b\u53cb\u7684\u6c9f\u901a"',
    '            "comp_watch_self_2"'
)
content = content.replace(
    '            "\u4e0d\u8981\u56e0\u4e3a\u5fd9\u788c\u800c\u5ffd\u89c6\u5065\u5eb7"',
    '            "comp_watch_drain_0"'
)
content = content.replace(
    '            "\u5b66\u4f1a\u53d6\u820d\uff0c\u4e0d\u8981\u4ec0\u4e48\u90fd\u60f3\u505a"',
    '            "comp_watch_drain_1"'
)
content = content.replace(
    '            "\u4fdd\u6301\u8010\u5fc3\uff0c\u4e0d\u8981\u6025\u4e8e\u6c42\u6210"',
    '            "comp_watch_drain_2"'
)
content = content.replace(
    '            "\u6ce8\u610f\u5904\u7406\u597d\u4eba\u9645\u5173\u7cfb"',
    '            "comp_watch_attack_0"'
)
content = content.replace(
    '            "\u4e0d\u8981\u51b2\u52a8\u505a\u51b3\u5b9a"',
    '            "comp_watch_attack_1"'
)
content = content.replace(
    '            "\u4fdd\u6301\u51b7\u9759\uff0c\u7406\u6027\u5206\u6790"',
    '            "comp_watch_attack_2"'
)
content = content.replace(
    '            "\u6ce8\u610f\u8eab\u4f53\u5065\u5eb7\uff0c\u5b9a\u671f\u4f53\u68c0"',
    '            "comp_watch_stress_0"'
)
content = content.replace(
    '            "\u4e0d\u8981\u7ed9\u81ea\u5df1\u592a\u5927\u538b\u529b"',
    '            "comp_watch_stress_1"'
)
content = content.replace(
    '            "\u5b66\u4f1a\u91ca\u653e\u538b\u529b\uff0c\u4fdd\u6301\u5fc3\u60c5\u6109\u60a6"',
    '            "comp_watch_stress_2"'
)
content = content.replace(
    '            "\u4fdd\u6301\u826f\u597d\u7684\u751f\u6d3b\u4e60\u60ef"',
    '            "comp_watch_neutral_0"'
)
content = content.replace(
    '            "\u4e0d\u8981\u56e0\u4e3a\u5e73\u6de1\u800c\u61c8\u6020"',
    '            "comp_watch_neutral_1"'
)
content = content.replace(
    '            "\u6301\u7eed\u5b66\u4e60\uff0c\u63d0\u5347\u81ea\u5df1"',
    '            "comp_watch_neutral_2"'
)

# 4. Replace _get_what_to_do
content = content.replace(
    '            "\u4e3b\u52a8\u51fa\u51fb\uff0c\u6293\u4f4f\u673a\u4f1a"',
    '            "comp_do_help_0"'
)
content = content.replace(
    '            "\u62d3\u5c55\u4eba\u8109\uff0c\u7ed3\u4ea4\u65b0\u670b\u53cb"',
    '            "comp_do_help_1"'
)
content = content.replace(
    '            "\u5c1d\u8bd5\u65b0\u4e8b\u7269\uff0c\u6311\u6218\u81ea\u5df1"',
    '            "comp_do_help_2"'
)
content = content.replace(
    '            "\u786e\u7acb\u81ea\u5df1\u7684\u76ee\u6807\u548c\u65b9\u5411"',
    '            "comp_do_self_0"'
)
content = content.replace(
    '            "\u4fdd\u6301\u81ea\u6211\uff0c\u4e0d\u8981\u968f\u6ce2\u901a\u6d41"',
    '            "comp_do_self_1"'
)
content = content.replace(
    '            "\u63d0\u5347\u81ea\u5df1\u7684\u4e13\u4e1a\u80fd\u529b"',
    '            "comp_do_self_2"'
)
# drain is same as events_drain_1
content = content.replace(
    '            "\u4fdd\u6301\u8010\u5fc3\uff0c\u7a33\u624e\u7a33\u6253"',
    '            "comp_do_drain_1"'
)
content = content.replace(
    '            "\u505a\u597d\u65f6\u95f4\u7ba1\u7406\uff0c\u63d0\u9ad8\u6548\u7387"',
    '            "comp_do_drain_2"'
)
content = content.replace(
    '            "\u63d0\u5347\u81ea\u5df1\u7684\u5b9e\u529b"',
    '            "comp_do_attack_0"'
)
content = content.replace(
    '            "\u5904\u7406\u597d\u4eba\u9645\u5173\u7cfb"',
    '            "comp_do_attack_1"'
)
content = content.replace(
    '            "\u4fdd\u6301\u51b7\u9759\uff0c\u7406\u6027\u51b3\u7b56"',
    '            "comp_do_attack_2"'
)
content = content.replace(
    '            "\u4fdd\u6301\u79ef\u6781\u5fc3\u6001"',
    '            "comp_do_stress_0"'
)
content = content.replace(
    '            "\u6ce8\u610f\u8eab\u4f53\u5065\u5eb7"',
    '            "comp_do_stress_1"'
)
content = content.replace(
    '            "\u7a33\u624e\u7a33\u6253\uff0c\u4e0d\u8981\u51b2\u52a8"',
    '            "comp_do_stress_2"'
)
# neutral watch is same as neutral do
content = content.replace(
    '            "\u6301\u7eed\u5b66\u4e60\uff0c\u63d0\u5347\u81ea\u5df1"',
    '            "comp_do_neutral_1"',
    1  # only first occurrence (watch_out already replaced the first)
)
content = content.replace(
    '            "\u73cd\u60dc\u8eab\u8fb9\u7684\u4eba"',
    '            "comp_do_neutral_2"'
)

# Also need to handle the remaining events_drain entries that overlap with do_drain
# events_drain_0 already handled, events_drain_1 and events_drain_2 overlap with do_drain
# Let me handle the remaining do entries
content = content.replace(
    '            "comp_events_drain_1"',
    '"comp_events_drain_1"',  # This was already replaced above, no-op
)

with open(r'C:\Users\t\Desktop\bazi_app\core\comprehensive_analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done - replaced comprehensive_analysis.py')
