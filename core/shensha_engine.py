
# core/shensha_engine.py
from core.bazi_utils import GAN_WUXING, ZHI_WUXING

# 天乙贵人
TIANYI = {
    "甲": ["丑", "未"], "戊": ["丑", "未"],
    "乙": ["子", "申"], "己": ["子", "申"],
    "丙": ["亥", "酉"], "丁": ["亥", "酉"],
    "壬": ["卯", "巳"], "癸": ["卯", "巳"],
    "庚": ["午", "寅"], "辛": ["午", "寅"]
}

# 驿马
YIMA = {
    "申": "寅", "子": "寅", "辰": "寅",
    "寅": "申", "午": "申", "戌": "申",
    "巳": "亥", "酉": "亥", "丑": "亥",
    "亥": "巳", "卯": "巳", "未": "巳"
}

# 桃花
TAOHUA = {
    "申": "酉", "子": "酉", "辰": "酉",
    "寅": "卯", "午": "卯", "戌": "卯",
    "巳": "午", "酉": "午", "丑": "午",
    "亥": "子", "卯": "子", "未": "子"
}

# 天德 (Based on Month Zhi)
TIANDE = {
    "子": "巳", "丑": "庚", "寅": "丁", "卯": "申",
    "辰": "壬", "巳": "辛", "午": "亥", "未": "甲",
    "申": "癸", "酉": "寅", "戌": "丙", "亥": "乙"
}

# 月德 (Based on Month Zhi)
YUEDE = {
    "寅": "丙", "午": "丙", "戌": "丙",
    "申": "壬", "子": "壬", "辰": "壬",
    "亥": "甲", "卯": "甲", "未": "甲",
    "巳": "庚", "酉": "庚", "丑": "庚"
}

# 文昌 (Based on Day Gan)
WENCHANG = {
    "甲": "巳", "乙": "午", "丙": "申", "丁": "酉",
    "戊": "申", "己": "酉", "庚": "亥", "辛": "子",
    "壬": "寅", "癸": "卯"
}

# 将星 (Based on Year/Day Zhi)
JIANGXING = {
    "申": "子", "子": "子", "辰": "子",
    "寅": "午", "午": "午", "戌": "午",
    "巳": "酉", "酉": "酉", "丑": "酉",
    "亥": "卯", "卯": "卯", "未": "卯"
}

# 华盖 (Based on Year/Day Zhi)
HUAGAI = {
    "申": "辰", "子": "辰", "辰": "辰",
    "寅": "戌", "午": "戌", "戌": "戌",
    "巳": "丑", "酉": "丑", "丑": "丑",
    "亥": "未", "卯": "未", "未": "未"
}

# 羊刃 (Based on Day Gan)
YANGREN = {
    "甲": "卯", "乙": "辰", "丙": "午", "丁": "未",
    "戊": "午", "己": "未", "庚": "酉", "辛": "戌",
    "壬": "子", "癸": "丑"
}

# 禄神 (Based on Day Gan)
LUSHEN = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
    "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
    "壬": "亥", "癸": "子"
}

# 红鸾 (Based on Year Zhi)
HONGLUAN = {
    "子": "卯", "丑": "寅", "寅": "丑", "卯": "子",
    "辰": "亥", "巳": "戌", "午": "酉", "未": "申",
    "申": "未", "酉": "午", "戌": "巳", "亥": "辰"
}

# 天喜 (Opposite of Hong Luan)
TIANXI = {
    "子": "酉", "丑": "申", "寅": "未", "卯": "午",
    "辰": "巳", "巳": "辰", "午": "卯", "未": "寅",
    "申": "丑", "酉": "子", "戌": "亥", "亥": "戌"
}

# 金舆 (Based on Day Gan)
JINYU = {
    "甲": "辰", "乙": "巳", "丙": "未", "丁": "申",
    "戊": "未", "己": "申", "庚": "戌", "辛": "亥",
    "壬": "丑", "癸": "寅"
}

# 孤辰 (Based on Year Zhi)
GUCHEN = {
    "亥": "寅", "子": "寅", "丑": "寅",
    "寅": "巳", "卯": "巳", "辰": "巳",
    "巳": "申", "午": "申", "未": "申",
    "申": "亥", "酉": "亥", "戌": "亥"
}

# 寡宿 (Based on Year Zhi)
GUASU = {
    "亥": "戌", "子": "戌", "丑": "戌",
    "寅": "丑", "卯": "丑", "辰": "丑",
    "巳": "辰", "午": "辰", "未": "辰",
    "申": "未", "酉": "未", "戌": "未"
}

# 劫煞 (Based on Year/Day Zhi)
JIESHA = {
    "申": "巳", "子": "巳", "辰": "巳",
    "寅": "亥", "午": "亥", "戌": "亥",
    "巳": "寅", "酉": "寅", "丑": "寅",
    "亥": "申", "卯": "申", "未": "申"
}

# 灾煞 (Based on Year/Day Zhi)
ZAISHA = {
    "申": "午", "子": "午", "辰": "午",
    "寅": "子", "午": "子", "戌": "子",
    "巳": "卯", "酉": "卯", "丑": "卯",
    "亥": "酉", "卯": "酉", "未": "酉"
}

# 亡神 (Based on Year/Day Zhi)
WANGSHEN = {
    "申": "亥", "子": "亥", "辰": "亥",
    "寅": "巳", "午": "巳", "戌": "巳",
    "巳": "申", "酉": "申", "丑": "申",
    "亥": "寅", "卯": "寅", "未": "寅"
}

# 元辰 (Based on Year Zhi)
# Yang Nan Yin Nu: Chong + 1 (Forward/Backward?)
# Simplified rule: 
# Yang Nan / Yin Nu: Zi->Wei, Chou->Wu, Yin->Si, Mao->Chen, Chen->Mao, Si->Yin, Wu->Chou, Wei->Zi, Shen->Hai, You->Xu, Xu->You, Hai->Shen
# Yin Nan / Yang Nu: Zi->Si, Chou->Chen, Yin->Mao, Mao->Yin, Chen->Chou, Si->Zi, Wu->Hai, Wei->Xu, Shen->You, You->Shen, Xu->Wei, Hai->Wu
# Since we don't have gender/yin-yang info passed easily here without looking up Year Gan Yin/Yang + Gender, 
# I will skip Yuan Chen for now to avoid complexity or assume simplified version if any.
# Let's add Tai Ji (Noble) instead, based on Day Gan.
TAIJI = {
    "甲": ["子", "午"], "乙": ["子", "午"],
    "丙": ["卯", "酉"], "丁": ["卯", "酉"],
    "戊": ["辰", "戌", "丑", "未"], "己": ["辰", "戌", "丑", "未"],
    "庚": ["寅", "亥"], "辛": ["寅", "亥"],
    "壬": ["巳", "申"], "癸": ["巳", "申"]
}

# 天医 (Based on Month Zhi)
# Previous month's Zhi? No, specific mapping.
# Jan(Yin)->Chou, Feb(Mao)->Yin... 
# Offset -1 roughly.
TIANYI_MED = {
    "寅": "丑", "卯": "寅", "辰": "卯",
    "巳": "辰", "午": "巳", "未": "午",
    "申": "未", "酉": "申", "戌": "酉",
    "亥": "戌", "子": "亥", "丑": "子"
}

# 学堂 (Based on Day Gan, Long Sheng position roughly)
XUETANG = {
    "甲": "亥", "乙": "午", "丙": "寅", "丁": "酉",
    "戊": "寅", "己": "酉", "庚": "巳", "辛": "子",
    "壬": "申", "癸": "卯"
}

def compute_shensha(bazi_pillars):
    """
    计算神煞
    """
    day_gan = bazi_pillars["day"][0]
    year_zhi = bazi_pillars["year"][1]
    month_zhi = bazi_pillars["month"][1]
    day_zhi = bazi_pillars["day"][1]
    day_gz = bazi_pillars["day"][0] + bazi_pillars["day"][1]
    
    shensha_list = []
    
    # 魁罡 (Check Day Pillar only)
    if day_gz in ["戊戌", "庚辰", "庚戌", "壬辰"]:
        shensha_list.append({"pillar_key": "pillar_day", "name_key": "shensha_kuigang_name", "desc_key": "shensha_kuigang_desc"})

    # Iterate all pillars (Year, Month, Day, Hour)
    # Check Gan and Zhi for each pillar
    
    pillars = [
        ("pillar_year", bazi_pillars["year"]),
        ("pillar_month", bazi_pillars["month"]),
        ("pillar_day", bazi_pillars["day"]),
        ("pillar_hour", bazi_pillars["hour"] if bazi_pillars["hour"] else (None, None))
    ]
    
    for pillar_key, (p_gan, p_zhi) in pillars:
        if not p_zhi: continue
        
        # --- Based on Day Gan ---
        
        # Tian Yi
        if p_zhi in TIANYI.get(day_gan, []):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_tianyi_name", "desc_key": "shensha_tianyi_desc"})
            
        # Wen Chang
        if p_zhi == WENCHANG.get(day_gan):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_wenchang_name", "desc_key": "shensha_wenchang_desc"})
            
        # Xue Tang
        if p_zhi == XUETANG.get(day_gan):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_xuetang_name", "desc_key": "shensha_xuetang_desc"})

        # Tai Ji
        if p_zhi in TAIJI.get(day_gan, []):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_taiji_name", "desc_key": "shensha_taiji_desc"})

        # Yang Ren
        if p_zhi == YANGREN.get(day_gan):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_yangren_name", "desc_key": "shensha_yangren_desc"})
            
        # Lu Shen
        if p_zhi == LUSHEN.get(day_gan):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_lushen_name", "desc_key": "shensha_lushen_desc"})
            
        # Jin Yu
        if p_zhi == JINYU.get(day_gan):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_jinyu_name", "desc_key": "shensha_jinyu_desc"})
            
        # --- Based on Year/Day Zhi ---
        
        # Yi Ma
        if p_zhi == YIMA.get(year_zhi) or p_zhi == YIMA.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_yima_name", "desc_key": "shensha_yima_desc"})
            
        # Tao Hua
        if p_zhi == TAOHUA.get(year_zhi) or p_zhi == TAOHUA.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_taohua_name", "desc_key": "shensha_taohua_desc"})
            
        # Jiang Xing
        if p_zhi == JIANGXING.get(year_zhi) or p_zhi == JIANGXING.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_jiangxing_name", "desc_key": "shensha_jiangxing_desc"})
            
        # Hua Gai
        if p_zhi == HUAGAI.get(year_zhi) or p_zhi == HUAGAI.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_huagai_name", "desc_key": "shensha_huagai_desc"})
            
        # Jie Sha
        if p_zhi == JIESHA.get(year_zhi) or p_zhi == JIESHA.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_jiesha_name", "desc_key": "shensha_jiesha_desc"})
            
        # Zai Sha
        if p_zhi == ZAISHA.get(year_zhi) or p_zhi == ZAISHA.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_zaisha_name", "desc_key": "shensha_zaisha_desc"})
            
        # Wang Shen
        if p_zhi == WANGSHEN.get(year_zhi) or p_zhi == WANGSHEN.get(day_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_wangshen_name", "desc_key": "shensha_wangshen_desc"})

        # --- Based on Month Zhi ---
        
        # Tian De (Check Gan or Zhi)
        target = TIANDE.get(month_zhi)
        if target:
            if p_gan == target or p_zhi == target: # Tian De can be Gan or Zhi
                shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_tiande_name", "desc_key": "shensha_tiande_desc"})
        
        # Yue De (Check Gan)
        if p_gan and p_gan == YUEDE.get(month_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_yuede_name", "desc_key": "shensha_yuede_desc"})
            
        # Tian Yi Med (Tian Yi Star for Medicine)
        if p_zhi == TIANYI_MED.get(month_zhi):
             shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_tianyimed_name", "desc_key": "shensha_tianyimed_desc"})

        # --- Based on Year Zhi ---
        
        # Hong Luan
        if p_zhi == HONGLUAN.get(year_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_hongluan_name", "desc_key": "shensha_hongluan_desc"})
            
        # Tian Xi
        if p_zhi == TIANXI.get(year_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_tianxi_name", "desc_key": "shensha_tianxi_desc"})

        # Gu Chen
        if p_zhi == GUCHEN.get(year_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_guchen_name", "desc_key": "shensha_guchen_desc"})

        # Gua Su
        if p_zhi == GUASU.get(year_zhi):
            shensha_list.append({"pillar_key": pillar_key, "name_key": "shensha_guasu_name", "desc_key": "shensha_guasu_desc"})


    # Deduplicate
    unique_shensha = []
    seen = set()
    for s in shensha_list:
        key = f"{s['name_key']}-{s['pillar_key']}"
        if key not in seen:
            unique_shensha.append(s)
            seen.add(key)
            
    return unique_shensha
