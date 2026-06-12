def empty_analysis():
    # 统一 schema：result.html 只读这些字段，不允许它“推理”
    return {
        "meta": {
            "lang": "zh",
            "name": "",
            "note": "",
        },
        "sections": {
            "overview": {"title": "", "bullets": []},          # 总览
            "personality": {"title": "", "text": ""},          # 性格
            "career": {"title": "", "text": "", "tags": []},   # 事业
            "love": {"title": "", "text": ""},                 # 情感
            "health": {"title": "", "text": ""},               # 身心
        },
        "tabs": {
            "dayun": [],   # [{start_year,end_year,gan_zhi,element_theme,story,keywords:[]}, ...]
            "liunian": [], # [{year,gan_zhi,theme,story,focus:[]}, ...]
            "shensha": [], # [{name,level,story,advice}, ...]
        },
    }
