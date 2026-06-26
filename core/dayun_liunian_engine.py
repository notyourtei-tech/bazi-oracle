
# core/dayun_liunian_engine.py
from core.bazi_utils import GAN_WUXING, ZHI_WUXING, get_shishen, get_wuxing

# 十神 Key 映射
SHISHEN_KEY_MAP = {
    "比肩": "bijian",
    "劫财": "jiecai",
    "食神": "shishen",
    "伤官": "shangguan",
    "正财": "zhengcai",
    "偏财": "piancai",
    "正官": "zhengguan",
    "七杀": "qisha",
    "正印": "zhengyin",
    "偏印": "pianyin"
}

def analyze_dayun(index, gz, start_year, end_year, day_master_wx, yongshen=None, day_master_gan=None):
    """
    分析大运
    """
    gan = gz[0]
    zhi = gz[1]
    
    # 优先使用天干计算十神来定大运基调
    dayun_shishen = "unknown"
    key_suffix = "unknown"
    if day_master_gan:
        dayun_shishen = get_shishen(day_master_gan, gan)
        key_suffix = SHISHEN_KEY_MAP.get(dayun_shishen, "unknown")
    
    return {
        "index": index,
        "gz": gz,
        "start_year": start_year,
        "end_year": end_year,
        "shishen": dayun_shishen,
        "theme_key": f"dayun_{key_suffix}_theme",
        "desc_key": f"dayun_{key_suffix}_desc",
        "advice_key": f"dayun_{key_suffix}_advice"
    }

def analyze_liunian(year: int, gz: str, day_master_gan: str, dayun_shishen: str = None):
    """
    分析流年
    """
    gan = gz[0]
    
    liunian_shishen = get_shishen(day_master_gan, gan)
    key_suffix = SHISHEN_KEY_MAP.get(liunian_shishen, "unknown")
    
    return {
        "year": year,
        "gz": gz,
        "shishen": liunian_shishen,
        "theme_key": f"liunian_{key_suffix}_theme",
        "desc_key": f"liunian_{key_suffix}_desc",
        "event_hint_key": f"liunian_{key_suffix}_event"
    }

def analyze_dayun_liunian_overlap(dayun, liunian):
    """
    大运流年叠加简单分析
    """
    return "dayun_liunian_overlap_key"

def build_yearly_focus(year, dayun, liunian, overlap):
    """
    年度重点
    """
    return "dayun_yearly_focus_key"
