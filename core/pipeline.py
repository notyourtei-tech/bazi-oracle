
from datetime import datetime

from core.geo_time_engine import build_time_bundle
from core.calendar_engine import compute_bazi_from_solar_time
from core.personality_engine import build_personality_yongshen_analysis
from core.qiyun_engine import calc_qiyun_and_dayun
from core.shensha_engine import compute_shensha
from core.dayun_liunian_engine import analyze_dayun, analyze_liunian
from core.bazi_utils import GAN_WUXING, ZHI_WUXING, get_nayin, get_hidden_stems, get_shishen, get_kongwang
from core.wuxing_engine import calc_wuxing
from core.interpretation_engine import build_comprehensive_interpretation

def _parse_local_datetime(date_str: str, time_str: str | None) -> datetime:
    y, m, d = [int(x) for x in date_str.split("-")]
    if time_str:
        hh, mm = [int(x) for x in time_str.split(":")]
    else:
        hh, mm = 12, 0
    return datetime(y, m, d, hh, mm)

def get_ganzhi_for_year(year: int):
    GAN = list("甲乙丙丁戊己庚辛壬癸")
    ZHI = list("子丑寅卯辰巳午未申酉戌亥")
    offset = (year - 4) % 60
    return GAN[offset % 10] + ZHI[offset % 12]

def run_full_analysis_from_birth(
    *,
    birth_country: str,
    birth_date: str,
    birth_time: str | None,
    gender: str,
    city: str | None = None
):
    local_naive = _parse_local_datetime(birth_date, birth_time)
    tb = build_time_bundle(birth_country, local_naive, city_key=city)

    cal = compute_bazi_from_solar_time(tb["solar_time"])
    
    # 构造八字结构供神煞使用
    bazi_pillars_struct = {
        "year": (cal.pillars.year[0], cal.pillars.year[1]),
        "month": (cal.pillars.month[0], cal.pillars.month[1]),
        "day": (cal.pillars.day[0], cal.pillars.day[1]),
        "hour": (cal.pillars.hour[0], cal.pillars.hour[1]) if birth_time else None
    }
    
    # 计算五行强弱
    wuxing_strength = calc_wuxing(bazi_pillars_struct)
    
    # 计算神煞
    shensha = compute_shensha(bazi_pillars_struct)
    
    day_master = cal.pillars.day[0]
    day_master_wx = GAN_WUXING.get(day_master)
    month_zhi = cal.pillars.month[1]
    month_zhi_wx = ZHI_WUXING.get(month_zhi)
    
    # 性格与强弱
    personality = build_personality_yongshen_analysis(day_master_wx, month_zhi_wx, None, wuxing_strength)
    
    # 起运与大运
    year_gz = "".join(cal.pillars.year)
    month_gz = "".join(cal.pillars.month)
    qiyun_info, raw_dayun_list = calc_qiyun_and_dayun(
        birth_solar_dt=tb["solar_time"],
        year_gz=year_gz,
        month_gz=month_gz,
        gender=gender,
        tz_offset_hours=tb["tz_offset_hours"]
    )
    
    # 处理大运及其内部流年
    processed_dayun = []
    for idx, d in enumerate(raw_dayun_list):
        # 1. 大运本身分析
        dy_analysis = analyze_dayun(
            index=idx, 
            gz=d["gz"], 
            start_year=d["start_year"], 
            end_year=d["end_year"], 
            day_master_wx=day_master_wx,
            day_master_gan=day_master
        )
        
        # 2. 该大运区间内的流年分析
        liunian_list = []
        for y in range(d["start_year"], d["end_year"] + 1):
            ygz = get_ganzhi_for_year(y)
            ln_analysis = analyze_liunian(
                year=y,
                gz=ygz,
                day_master_gan=day_master,
                dayun_shishen=dy_analysis["shishen"]
            )
            liunian_list.append(ln_analysis)
            
        dy_analysis["liunian_list"] = liunian_list
        processed_dayun.append(dy_analysis)

    # 计算空亡 (基于日柱)
    kw_branches = get_kongwang(cal.pillars.day[0], cal.pillars.day[1])

    # 颜色与详情结构
    def pillar_detail(pair, pillar_key):
        if not pair: return {
            "gan": "-", "zhi": "-", "gan_wx": "", "zhi_wx": "", 
            "nayin": "", "nayin_key": "",
            "hidden_stems": [], "hidden_stems_wx": [], "sub_stars": [],
            "is_kw": False,
            "shensha": []
        }
        
        gan, zhi = pair
        gz = gan + zhi
        
        # 纳音
        ny_key = get_nayin(gz)
        
        # 藏干
        hidden = get_hidden_stems(zhi)
        hidden_wx = [GAN_WUXING.get(h, "") for h in hidden]
        
        # 副星 (十神)
        sub_stars = []
        for h in hidden:
            ss_name = get_shishen(day_master, h)
            from core.dayun_liunian_engine import SHISHEN_KEY_MAP
            key_suffix = SHISHEN_KEY_MAP.get(ss_name, "unknown")
            sub_stars.append({"name": ss_name, "key": f"shishen_{key_suffix}"})
            
        # 空亡
        is_kw = (zhi in kw_branches)
        
        # 该柱神煞
        my_shensha = [s for s in shensha if s["pillar_key"] == pillar_key]
        
        return {
            "gan": gan, 
            "zhi": zhi, 
            "gan_wx": GAN_WUXING.get(gan), 
            "zhi_wx": ZHI_WUXING.get(zhi),
            "nayin_key": ny_key,
            "hidden_stems": hidden,
            "hidden_stems_wx": hidden_wx,
            "sub_stars": sub_stars,
            "is_kw": is_kw,
            "shensha": my_shensha
        }

    bazi_detail = {
        "year": pillar_detail(cal.pillars.year, "pillar_year"),
        "month": pillar_detail(cal.pillars.month, "pillar_month"),
        "day": pillar_detail(cal.pillars.day, "pillar_day"),
        "hour": pillar_detail(cal.pillars.hour if birth_time else None, "pillar_hour")
    }
    
    result = {
        "meta": {
            "country": birth_country,
            "solar_time": tb["solar_time"].strftime("%Y-%m-%d %H:%M"),
            "note": "True Solar Time Used"
        },
        "bazi": {
            "year": year_gz, "month": month_gz, "day": "".join(cal.pillars.day), 
            "hour": "".join(cal.pillars.hour) if birth_time else "-"
        },
        "bazi_detail": bazi_detail,
        "personality": personality, 
        "shensha": shensha,
        "wuxing_strength": wuxing_strength,
        "qiyun": qiyun_info,
        "dayun": processed_dayun # 包含 liunian_list
    }
    
    # 生成综合解读
    try:
        result["interpretation"] = build_comprehensive_interpretation(result)
    except Exception as e:
        result["interpretation"] = {}
    
    return result
