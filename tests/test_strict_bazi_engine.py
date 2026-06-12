import unittest
from datetime import datetime
from core.strict_bazi_engine import compute_bazi

class TestStrictBaziEngine(unittest.TestCase):
    def test_beijing_2006_05_13_1730(self):
        dt = datetime(2006, 5, 13, 17, 30)
        lon = 116.4074
        lat = 39.9042
        tz = 8.0
        res = compute_bazi(
            birth_dt_local=dt,
            longitude_deg=lon,
            latitude_deg=lat,
            tz_offset_hours=tz,
            dst_enabled=False,
            use_true_solar=True,
            use_zi_switch=False
        )
        self.assertEqual(res["pillars"]["year"]["gan"] + res["pillars"]["year"]["zhi"], "丙戌")
        self.assertEqual(res["pillars"]["month"]["gan"] + res["pillars"]["month"]["zhi"], "癸巳")
        self.assertEqual(res["pillars"]["day"]["gan"] + res["pillars"]["day"]["zhi"], "壬寅")
        self.assertEqual(res["pillars"]["hour"]["gan"] + res["pillars"]["hour"]["zhi"], "己酉")

    def test_month_boundary_before_after_lixia(self):
        lon = 116.4074
        lat = 39.9042
        tz = 8.0
        dt_before = datetime(2006, 5, 4, 12, 0)
        res_b = compute_bazi(
            birth_dt_local=dt_before,
            longitude_deg=lon,
            latitude_deg=lat,
            tz_offset_hours=tz,
            dst_enabled=False,
            use_true_solar=True,
            use_zi_switch=False
        )
        self.assertEqual(res_b["pillars"]["month"]["zhi"], "辰")
        self.assertEqual(res_b["pillars"]["month"]["gan"], "壬")
        dt_after = datetime(2006, 5, 6, 12, 0)
        res_a = compute_bazi(
            birth_dt_local=dt_after,
            longitude_deg=lon,
            latitude_deg=lat,
            tz_offset_hours=tz,
            dst_enabled=False,
            use_true_solar=True,
            use_zi_switch=False
        )
        self.assertEqual(res_a["pillars"]["month"]["zhi"], "巳")
        self.assertEqual(res_a["pillars"]["month"]["gan"], "癸")

if __name__ == "__main__":
    unittest.main()
