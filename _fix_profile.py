with open(r'C:\Users\t\Desktop\bazi_app\core\analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def analyze_profile(ec):
    """
    \u7efc\u5408\u5206\u6790\uff1a\u6027\u683c\u3001\u4e8b\u4e1a\u65b9\u5411\u3001\u611f\u60c5\u98ce\u683c\u3001\u5065\u5eb7\u63d0\u9192\u3001\u795e\u715e\u63d0\u793a
    """
    dm_gan = ec.getDayGan()
    dm_zhi = ec.getDayZhi()
    elem = stem_to_element(dm_gan)

    # \u9634\u9633
    yang_stems = ["\u7532", "\u4e19", "\u620a", "\u5e9a", "\u58ec"]
    yin_yang = "\u9633" if dm_gan in yang_stems else "\u9634"

    # \u6027\u683c\u57fa\u8c03
    if elem == "\u6728":
        base_personality = "\u5185\u5728\u5e26\u7740\u6210\u957f\u6b32\u671b\u548c\u7406\u60f3\u611f\uff0c\u91cd\u89c6\u539f\u5219\uff0c\u6709\u65f6\u6bd4\u8f83\u76f4\u6765\u76f4\u53bb\u3002"
    elif elem == "\u706b":
        base_personality = "\u6027\u683c\u504f\u70ed\u60c5\u76f4\u63a5\uff0c\u60c5\u7eea\u53cd\u5e94\u5feb\uff0c\u8bb2\u611f\u89c9\uff0c\u8ba8\u538c\u62d6\u6ce5\u5e26\u6c34\u3002"
    elif elem == "\u571f":
        base_personality = "\u504f\u7a33\u91cd\u73b0\u5b9e\u578b\uff0c\u91cd\u89c6\u5b89\u5168\u611f\u4e0e\u8d23\u4efb\u611f\uff0c\u6bd4\u8f83\u80fd\u6297\u4e8b\u3002"
    elif elem == "\u91d1":
        base_personality = "\u601d\u8def\u504f\u7406\u6027\u3001\u91cd\u89c4\u5219\uff0c\u5224\u65ad\u529b\u5f3a\uff0c\u559c\u6b22\u6e05\u6670\u4e0e\u6548\u7387\u3002"
    elif elem == "\u6c34":
        base_personality = "\u611f\u53d7\u7ec6\u817b\u3001\u89c2\u5bdf\u529b\u5f3a\uff0c\u60f3\u6cd5\u591a\uff0c\u9002\u5408\u52a8\u8111\u800c\u4e0d\u662f\u786c\u6297\u3002"
    else:
        base_personality = "\u6027\u683c\u6bd4\u8f83\u7efc\u5408\uff0c\u4e0d\u4f1a\u7279\u522b\u504f\u5411\u67d0\u4e00\u7c7b\u3002"

    if yin_yang == "\u9633":
        ext = "\u6574\u4f53\u504f\u5916\u5411\u3001\u4e3b\u52a8\uff0c\u9047\u4e8b\u4e60\u60ef\u5148\u51fa\u624b\u518d\u6162\u6162\u8c03\u6574\u3002"
    else:
        ext = "\u6574\u4f53\u504f\u542b\u84c4\u3001\u89c2\u5bdf\u578b\uff0c\u4e60\u60ef\u5148\u770b\u6e05\u5c40\u52bf\u518d\u51fa\u624b\u3002"

    personality = f"\u65e5\u4e3b\u4e3a{yin_yang}{elem}\uff0c{base_personality}{ext}"

    # \u4e8b\u4e1a\u65b9\u5411
    if elem == "\u6728":
        career = "\u9002\u5408\u6559\u80b2\u3001\u987e\u95ee\u3001\u8bbe\u8ba1\u3001\u6587\u5b57\u3001\u6587\u5316\u3001\u5fc3\u7406\u3001\u54a8\u8be2\u7b49\u4e0e\u6210\u957f\u76f8\u5173\u7684\u884c\u4e1a\uff0c\u4e5f\u9002\u5408\u548c\u4eba\u6253\u4ea4\u9053\u7684\u5de5\u4f5c\u3002"
    elif elem == "\u706b":
        career = "\u9002\u5408\u9700\u8981\u8868\u73b0\u529b\u548c\u70ed\u60c5\u7684\u5de5\u4f5c\uff1a\u9500\u552e\u3001\u516c\u5173\u3001\u76f4\u64ad\u3001\u81ea\u5a92\u4f53\u3001\u5a31\u4e50\u3001\u9910\u996e\u3001\u6d3b\u52a8\u7b56\u5212\u7b49\u3002"
    elif elem == "\u571f":
        career = "\u9002\u5408\u7a33\u5b9a\u3001\u9700\u8981\u8010\u5fc3\u4e0e\u8d23\u4efb\u611f\u7684\u5c97\u4f4d\uff1a\u884c\u653f\u3001\u8d22\u52a1\u3001\u4eba\u4e8b\u3001\u4e0d\u52a8\u4ea7\u3001\u571f\u6728\u3001\u4f9b\u5e94\u94fe\u3001\u540e\u53f0\u8fd0\u8425\u7b49\u3002"
    elif elem == "\u91d1":
        career = "\u9002\u5408\u6cd5\u5f8b\u3001\u91d1\u878d\u3001\u5ba1\u8ba1\u3001IT \u5f00\u53d1\u3001\u6570\u636e\u5206\u6790\u3001\u98ce\u63a7\u3001\u7ba1\u7406\u5c97\u4f4d\u7b49\u9700\u8981\u5224\u65ad\u548c\u51b3\u7b56\u7684\u5de5\u4f5c\u3002"
    elif elem == "\u6c34":
        career = "\u9002\u5408\u8d44\u8baf\u3001\u4f20\u5a92\u3001\u54a8\u8be2\u3001\u5fc3\u7406\u3001\u5916\u8bed\u3001\u8de8\u56fd\u4e1a\u52a1\u3001\u6d41\u901a\u8d38\u6613\u7b49\u9700\u8981\u7075\u6d3b\u6c9f\u901a\u7684\u9886\u57df\u3002"
    else:
        career = "\u6574\u4f53\u884c\u4e1a\u9650\u5236\u4e0d\u5927\uff0c\u91cd\u70b9\u662f\u627e\u80fd\u6301\u7eed\u5b66\u4e60\u3001\u53c8\u4e0d\u4f1a\u88ab\u5b8c\u5168\u7ed1\u6b7b\u7684\u65b9\u5411\u3002"

    # \u611f\u60c5
    if elem in ["\u6728", "\u706b"]:
        love = "\u611f\u60c5\u4e0a\u6bd4\u8f83\u4e3b\u52a8\uff0c\u6709\u611f\u89c9\u5c31\u5f88\u96be\u88c5\u4f5c\u6ca1\u4e8b\uff0c\u4f46\u4e5f\u5bb9\u6613\u56e0\u4e3a\u51b2\u52a8\u6216\u70ed\u5ea6\u53d8\u5316\u5feb\u800c\u8d77\u4f0f\u8f83\u5927\u3002"
    elif elem in ["\u91d1", "\u6c34"]:
        love = "\u611f\u60c5\u91cc\u6bd4\u8f83\u91cd\u7406\u6027\u4e0e\u4e92\u52a8\u8d28\u91cf\uff0c\u4e0d\u592a\u559c\u6b22\u9ecf\u817b\uff0c\u4f46\u5e0c\u671b\u5bf9\u65b9\u80fd\u7406\u89e3\u81ea\u5df1\u7684\u8282\u594f\u4e0e\u8fb9\u754c\u3002"
    else:
        love = "\u611f\u60c5\u89c2\u504f\u52a1\u5b9e\uff0c\u6bd4\u8f83\u770b\u91cd\u7a33\u5b9a\u4e0e\u957f\u671f\u6253\u7b97\uff0c\u6709\u65f6\u8868\u8fbe\u4e0d\u591f\u6d6a\u6f2b\uff0c\u4f46\u5fc3\u91cc\u662f\u8bb0\u5f97\u5bf9\u65b9\u597d\u7684\u3002"

    # \u5065\u5eb7\uff08\u5927\u65b9\u5411\uff09
    if elem == "\u706b":
        health = "\u6ce8\u610f\u5fc3\u8840\u7ba1\u3001\u8840\u538b\u4e0e\u71ac\u591c\u95ee\u9898\uff0c\u4fdd\u6301\u89c4\u5f8b\u4f5c\u606f\u5f88\u91cd\u8981\u3002"
    elif elem == "\u6c34":
        health = "\u6ce8\u610f\u80be\u810f\u3001\u6ccc\u5c3f\u4e0e\u7761\u7720\u8d28\u91cf\uff0c\u907f\u514d\u957f\u671f\u538b\u529b\u5bfc\u81f4\u5931\u7720\u3002"
    elif elem == "\u6728":
        health = "\u6ce8\u610f\u809d\u80c6\u4e0e\u773c\u775b\uff0c\u7528\u7535\u8111\u65f6\u95f4\u957f\u8bb0\u5f97\u4f11\u606f\u4e0e\u8fd0\u52a8\u3002"
    elif elem == "\u91d1":
        health = "\u6ce8\u610f\u547c\u5438\u9053\u3001\u76ae\u80a4\u4e0e\u7b4b\u9aa8\uff0c\u4e45\u5750\u8981\u65f6\u5e38\u6d3b\u52a8\u3002"
    else:
        health = "\u6ce8\u610f\u813e\u80c3\u3001\u6d88\u5316\u7cfb\u7edf\u4e0e\u4f53\u91cd\u7ba1\u7406\uff0c\u996e\u98df\u5c3d\u91cf\u89c4\u5f8b\u3002"

    # \u795e\u715e\u63d0\u793a\uff08\u7b80\u6613\u7248\uff09
    shensha_list = simple_shensha(dm_zhi)
    if shensha_list:
        shensha_text = "\u3001".join(shensha_list)
    else:
        shensha_text = "\u547d\u76d8\u795e\u715e\u5206\u5e03\u6bd4\u8f83\u5e73\u5747\uff0c\u6ca1\u6709\u7279\u522b\u6781\u7aef\u7684\u52a0\u5206\u6216\u51cf\u5206\u70b9\uff0c\u66f4\u770b\u91cd\u81ea\u5df1\u540e\u5929\u7684\u9009\u62e9\u3002"

    return {
        "personality": personality,
        "career": career,
        "love": love,
        "health": health,
        "shensha": shensha_text,
    }'''

new = '''def analyze_profile(ec):
    """
    \u7efc\u5408\u5206\u6790\uff1a\u6027\u683c\u3001\u4e8b\u4e1a\u65b9\u5411\u3001\u611f\u60c5\u98ce\u683c\u3001\u5065\u5eb7\u63d0\u9192\u3001\u795e\u715e\u63d0\u793a
    """
    dm_gan = ec.getDayGan()
    dm_zhi = ec.getDayZhi()
    elem = stem_to_element(dm_gan)

    # \u9634\u9633
    yang_stems = ["\u7532", "\u4e19", "\u620a", "\u5e9a", "\u58ec"]
    yin_yang = "yang_label" if dm_gan in yang_stems else "yin_label"

    # \u6027\u683c\u57fa\u8c03
    if elem == "\u6728":
        base_personality = "profile_personality_wood_base"
    elif elem == "\u706b":
        base_personality = "profile_personality_fire_base"
    elif elem == "\u571f":
        base_personality = "profile_personality_earth_base"
    elif elem == "\u91d1":
        base_personality = "profile_personality_metal_base"
    elif elem == "\u6c34":
        base_personality = "profile_personality_water_base"
    else:
        base_personality = "profile_personality_default_base"

    if yin_yang == "yang_label":
        ext = "profile_personality_yang_ext"
    else:
        ext = "profile_personality_yin_ext"

    personality = f"profile_dm_prefix{yin_yang}{elem}\uff0c{base_personality}{ext}"

    # \u4e8b\u4e1a\u65b9\u5411
    if elem == "\u6728":
        career = "profile_career_wood"
    elif elem == "\u706b":
        career = "profile_career_fire"
    elif elem == "\u571f":
        career = "profile_career_earth"
    elif elem == "\u91d1":
        career = "profile_career_metal"
    elif elem == "\u6c34":
        career = "profile_career_water"
    else:
        career = "profile_career_default"

    # \u611f\u60c5
    if elem in ["\u6728", "\u706b"]:
        love = "profile_love_wood_fire"
    elif elem in ["\u91d1", "\u6c34"]:
        love = "profile_love_metal_water"
    else:
        love = "profile_love_earth"

    # \u5065\u5eb7\uff08\u5927\u65b9\u5411\uff09
    if elem == "\u706b":
        health = "profile_health_fire"
    elif elem == "\u6c34":
        health = "profile_health_water"
    elif elem == "\u6728":
        health = "profile_health_wood"
    elif elem == "\u91d1":
        health = "profile_health_metal"
    else:
        health = "profile_health_earth"

    # \u795e\u715e\u63d0\u793a\uff08\u7b80\u6613\u7248\uff09
    shensha_list = simple_shensha(dm_zhi)
    if shensha_list:
        shensha_text = "\u3001".join(shensha_list)
    else:
        shensha_text = "shensha_text_none"

    return {
        "personality": personality,
        "career": career,
        "love": love,
        "health": health,
        "shensha": shensha_text,
    }'''

content = content.replace(old, new)

with open(r'C:\Users\t\Desktop\bazi_app\core\analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done - replaced analyze_profile')
