# core/fortune_engine.py

from core.dayun_liunian_engine import (
    analyze_liunian,
    analyze_dayun,
    analyze_dayun_liunian_overlap,
    build_yearly_focus
)

# ===== 示例：你已有的基础函数 =====
# build_bazi(...)
# get_day_master(...)
# get_yongshen(...)
# get_dayun_list(...)

def full_analysis_from_birth(
    bazi: dict,
    day_master_wx: str,
    yongshen: str | None,
    dayun_list: list
):
    """
    核心总入口：整合 大运 / 流年 / 叠加 / 年度重点
    """

    result = {
        "bazi": bazi,
        "day_master": day_master_wx,
        "yongshen": yongshen,
        "dayun": [],
        "liunian": []
    }

    # ===== 遍历每一个大运 =====
    for idx, du in enumerate(dayun_list):
        dayun_info = analyze_dayun(
            index=idx + 1,
            gz=du["gz"],
            start_year=du["start_year"],
            end_year=du["end_year"],
            day_master_wx=day_master_wx,
            yongshen=yongshen
        )

        result["dayun"].append(dayun_info)

        # ===== 在这个大运下，生成每一年的流年 =====
        for year in range(du["start_year"], du["end_year"] + 1):
            liunian_gz = du["liunian_map"].get(year)
            if not liunian_gz:
                continue

            liunian_info = analyze_liunian(
                year=year,
                gz=liunian_gz,
                day_master_gan=bazi["day"][0],
                dayun_shishen=yongshen
            )

            overlap = analyze_dayun_liunian_overlap(
                dayun=dayun_info,
                liunian=liunian_info
            )

            focus = build_yearly_focus(
                year=year,
                dayun=dayun_info,
                liunian=liunian_info,
                overlap=overlap
            )

            liunian_info["dayun_index"] = idx + 1
            liunian_info["overlap"] = overlap
            liunian_info["focus"] = focus

            result["liunian"].append(liunian_info)

    return result
