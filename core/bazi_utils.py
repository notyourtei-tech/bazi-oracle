
# core/bazi_utils.py

GAN_WUXING = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water"
}

ZHI_WUXING = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water"
}

ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

ZHI_HIDDEN_GAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "戊", "庚"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

NAYIN_MAP = {
    "甲子": "nayin_gold_sea", "乙丑": "nayin_gold_sea",
    "丙寅": "nayin_fire_furnace", "丁卯": "nayin_fire_furnace",
    "戊辰": "nayin_wood_forest", "己巳": "nayin_wood_forest",
    "庚午": "nayin_earth_road", "辛未": "nayin_earth_road",
    "壬申": "nayin_metal_sword", "癸酉": "nayin_metal_sword",
    "甲戌": "nayin_fire_mountain", "乙亥": "nayin_fire_mountain",
    "丙子": "nayin_water_stream", "丁丑": "nayin_water_stream",
    "戊寅": "nayin_earth_wall", "己卯": "nayin_earth_wall",
    "庚辰": "nayin_metal_wax", "辛巳": "nayin_metal_wax",
    "壬午": "nayin_wood_poplar", "癸未": "nayin_wood_poplar",
    "甲申": "nayin_water_well", "乙酉": "nayin_water_well",
    "丙戌": "nayin_earth_roof", "丁亥": "nayin_earth_roof",
    "戊子": "nayin_fire_thunder", "己丑": "nayin_fire_thunder",
    "庚寅": "nayin_wood_pine", "辛卯": "nayin_wood_pine",
    "壬辰": "nayin_water_river", "癸巳": "nayin_water_river",
    "甲午": "nayin_gold_sand", "乙未": "nayin_gold_sand",
    "丙申": "nayin_fire_mountain_foot", "丁酉": "nayin_fire_mountain_foot",
    "戊戌": "nayin_wood_plain", "己亥": "nayin_wood_plain",
    "庚子": "nayin_earth_wall_on", "辛丑": "nayin_earth_wall_on",
    "壬寅": "nayin_metal_foil", "癸卯": "nayin_metal_foil",
    "甲辰": "nayin_fire_lamp", "乙巳": "nayin_fire_lamp",
    "丙午": "nayin_water_sky", "丁未": "nayin_water_sky",
    "戊申": "nayin_earth_land", "己酉": "nayin_earth_land",
    "庚戌": "nayin_gold_hairpin", "辛亥": "nayin_gold_hairpin",
    "壬子": "nayin_wood_mulberry", "癸丑": "nayin_wood_mulberry",
    "甲寅": "nayin_water_stream_great", "乙卯": "nayin_water_stream_great",
    "丙辰": "nayin_earth_sand", "丁巳": "nayin_earth_sand",
    "戊午": "nayin_fire_sun", "己未": "nayin_fire_sun",
    "庚申": "nayin_wood_pomegranate", "辛酉": "nayin_wood_pomegranate",
    "壬戌": "nayin_water_ocean", "癸亥": "nayin_water_ocean"
}

# 十神映射 (基于日主与他干的关系)
# Key: (Day Master Wuxing, Other Wuxing) -> Base Relation
# Then check Yin/Yang for specific Ten God
# simplified for now:
# 1. Determine relationship (Same, Generated, Controlled, Controls Me, Generates Me)
# 2. Determine Yin/Yang (Same polarity = Bi/Shi/Pian, Diff polarity = Jie/Shang/Zheng)

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
YIN_YANG = {
    "甲": "yang", "乙": "yin",
    "丙": "yang", "丁": "yin",
    "戊": "yang", "己": "yin",
    "庚": "yang", "辛": "yin",
    "壬": "yang", "癸": "yin"
}

SHISHEN_MAP = {
    "same": {"same": "比肩", "diff": "劫财"},
    "generated": {"same": "食神", "diff": "伤官"},
    "controlled": {"same": "偏财", "diff": "正财"},
    "controls_me": {"same": "七杀", "diff": "正官"},
    "generates_me": {"same": "偏印", "diff": "正印"}
}

def get_wuxing(stem_or_branch):
    return GAN_WUXING.get(stem_or_branch) or ZHI_WUXING.get(stem_or_branch)

def get_shishen(day_master_gan, other_gan):
    """
    计算十神
    day_master_gan: 日主天干
    other_gan: 其他天干
    """
    dm_wx = GAN_WUXING[day_master_gan]
    other_wx = GAN_WUXING[other_gan]
    
    dm_yy = YIN_YANG[day_master_gan]
    other_yy = YIN_YANG[other_gan]
    
    is_same_yy = "same" if dm_yy == other_yy else "diff"
    
    relation = ""
    
    # 五行生克关系
    if dm_wx == other_wx:
        relation = "same"
    # 生我
    elif (dm_wx == "wood" and other_wx == "water") or \
         (dm_wx == "fire" and other_wx == "wood") or \
         (dm_wx == "earth" and other_wx == "fire") or \
         (dm_wx == "metal" and other_wx == "earth") or \
         (dm_wx == "water" and other_wx == "metal"):
        relation = "generates_me"
    # 我生
    elif (dm_wx == "wood" and other_wx == "fire") or \
         (dm_wx == "fire" and other_wx == "earth") or \
         (dm_wx == "earth" and other_wx == "metal") or \
         (dm_wx == "metal" and other_wx == "water") or \
         (dm_wx == "water" and other_wx == "wood"):
        relation = "generated"
    # 克我
    elif (dm_wx == "wood" and other_wx == "metal") or \
         (dm_wx == "fire" and other_wx == "water") or \
         (dm_wx == "earth" and other_wx == "wood") or \
         (dm_wx == "metal" and other_wx == "fire") or \
         (dm_wx == "water" and other_wx == "earth"):
        relation = "controls_me"
    # 我克
    elif (dm_wx == "wood" and other_wx == "earth") or \
         (dm_wx == "fire" and other_wx == "metal") or \
         (dm_wx == "earth" and other_wx == "water") or \
         (dm_wx == "metal" and other_wx == "wood") or \
         (dm_wx == "water" and other_wx == "fire"):
        relation = "controlled"
        
    return SHISHEN_MAP[relation][is_same_yy]

def get_nayin(ganzhi):
    return NAYIN_MAP.get(ganzhi, "")

def get_kongwang(gan, zhi):
    g_idx = TIANGAN.index(gan)
    z_idx = ZHI.index(zhi)
    dist = 9 - g_idx
    z_gui = (z_idx + dist) % 12
    kw1 = ZHI[(z_gui + 1) % 12]
    kw2 = ZHI[(z_gui + 2) % 12]
    return [kw1, kw2]

def get_hidden_stems(zhi):
    return ZHI_HIDDEN_GAN.get(zhi, [])
