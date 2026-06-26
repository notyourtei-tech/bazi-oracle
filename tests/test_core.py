"""Core engine unit tests"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.bazi_utils import (
    GAN_WUXING, ZHI_WUXING, get_shishen, get_nayin, get_kongwang,
    get_hidden_stems, TIANGAN, ZHI, NAYIN_MAP
)
from core.wuxing_engine import calc_wuxing, ZHI_CANG
from core.comprehensive_analysis import (
    get_relation, get_life_stage, STEM_ELEMENT,
    analyze_dayun_comprehensive, analyze_liunian_comprehensive
)
from core.daily_fortune_engine import calc_daily_fortune, calc_weekly_fortune, date_to_ganzhi
from core.compatibility_engine import analyze_compatibility
from core.pipeline import get_ganzhi_for_year, _parse_local_datetime
from datetime import date


class TestBaziUtils:
    def test_gan_wuxing_complete(self):
        assert len(GAN_WUXING) == 10
        assert GAN_WUXING["甲"] == "wood"
        assert GAN_WUXING["癸"] == "water"

    def test_zhi_wuxing_complete(self):
        assert len(ZHI_WUXING) == 12
        assert ZHI_WUXING["子"] == "water"
        assert ZHI_WUXING["午"] == "fire"

    def test_get_shishen_same_element(self):
        assert get_shishen("甲", "乙") == "劫财"
        assert get_shishen("甲", "甲") == "比肩"

    def test_get_shishen_generates(self):
        assert get_shishen("甲", "丙") == "食神"
        assert get_shishen("甲", "丁") == "伤官"

    def test_get_shishen_controls(self):
        assert get_shishen("甲", "戊") == "偏财"
        assert get_shishen("甲", "己") == "正财"

    def test_get_shishen_invalid(self):
        assert get_shishen("X", "甲") == "比肩"
        assert get_shishen("甲", "X") == "比肩"

    def test_get_nayin(self):
        assert get_nayin("甲子") == "nayin_gold_sea"
        assert get_nayin("ZZ") == ""

    def test_get_kongwang(self):
        kw = get_kongwang("甲", "子")
        assert isinstance(kw, list)
        assert len(kw) == 2

    def test_get_kongwang_error(self):
        kw = get_kongwang("X", "Y")
        assert kw == []

    def test_get_hidden_stems(self):
        assert "癸" in get_hidden_stems("子")
        assert "甲" in get_hidden_stems("寅")


class TestWuxingEngine:
    def test_calc_wuxing_basic(self):
        bazi = {
            "year": ("丙", "戌"),
            "month": ("癸", "巳"),
            "day": ("甲", "辰"),
            "hour": ("庚", "午")
        }
        result = calc_wuxing(bazi)
        assert all(k in result for k in ["wood", "fire", "earth", "metal", "water"])
        assert all(v >= 0 for v in result.values())

    def test_calc_wuxing_no_hour(self):
        bazi = {
            "year": ("甲", "子"),
            "month": ("丙", "寅"),
            "day": ("戊", "午"),
            "hour": None
        }
        result = calc_wuxing(bazi)
        assert "wood" in result


class TestComprehensiveAnalysis:
    def test_get_relation(self):
        assert get_relation("木", "火") == "drain"
        assert get_relation("木", "水") == "help"
        assert get_relation("木", "土") == "attack"
        assert get_relation("木", "金") == "stress"
        assert get_relation("木", "木") == "self"
        assert get_relation("", "木") == "neutral"

    def test_get_life_stage(self):
        assert get_life_stage(5) == "comp_stage_childhood"
        assert get_life_stage(25) == "comp_stage_social"
        assert get_life_stage(65) == "comp_stage_later"

    def test_analyze_dayun_comprehensive(self):
        dayun_data = [
            {"start_year": 1996, "end_year": 2005, "gz": "甲子", "liunian_list": []}
        ]
        result = analyze_dayun_comprehensive(dayun_data, 1990, "木")
        assert len(result) == 1
        assert "overall_score" in result[0]
        assert "health" in result[0]

    def test_analyze_liunian_comprehensive(self):
        liunian_data = [
            {"year": 2024, "gz": "甲辰", "theme_key": "t", "desc_key": "d", "event_hint_key": "e"}
        ]
        result = analyze_liunian_comprehensive(liunian_data, 1990, "木")
        assert len(result) == 1
        assert result[0]["year"] == 2024


class TestDailyFortune:
    def test_calc_daily_fortune(self):
        result = {
            "bazi_detail": {"day": {"gan": "甲"}},
            "wuxing_strength": {"wood": 30, "fire": 20, "earth": 15, "metal": 10, "water": 25}
        }
        fortune = calc_daily_fortune(result)
        assert "score" in fortune
        assert 20 <= fortune["score"] <= 90
        assert "level" in fortune

    def test_calc_weekly_fortune(self):
        result = {
            "bazi_detail": {"day": {"gan": "甲"}},
            "wuxing_strength": {"wood": 30, "fire": 20, "earth": 15, "metal": 10, "water": 25}
        }
        weekly = calc_weekly_fortune(result)
        assert len(weekly) == 7

    def test_date_to_ganzhi(self):
        gz = date_to_ganzhi(date(1984, 1, 31))
        assert gz["gan"] == "甲"
        assert gz["zhi"] == "子"


class TestCompatibility:
    def test_analyze_compatibility(self):
        r1 = {
            "bazi_detail": {"day": {"gan": "甲", "zhi": "子"}},
            "wuxing_strength": {"wood": 30, "fire": 20, "earth": 15, "metal": 10, "water": 25},
            "personality": {"body_strength_key": "strong"}
        }
        r2 = {
            "bazi_detail": {"day": {"gan": "乙", "zhi": "丑"}},
            "wuxing_strength": {"wood": 25, "fire": 15, "earth": 25, "metal": 15, "water": 20},
            "personality": {"body_strength_key": "weak"}
        }
        result = analyze_compatibility(r1, r2)
        assert "overall_score" in result
        assert "level" in result
        assert 0 <= result["overall_score"] <= 100


class TestPipeline:
    def test_get_ganzhi_for_year(self):
        assert get_ganzhi_for_year(1984) == "甲子"
        assert get_ganzhi_for_year(2024) == "甲辰"

    def test_parse_local_datetime(self):
        dt = _parse_local_datetime("1990-05-13", "14:30")
        assert dt.year == 1990
        assert dt.month == 5
        assert dt.hour == 14

    def test_parse_local_datetime_no_time(self):
        dt = _parse_local_datetime("1990-05-13", None)
        assert dt.hour == 12
