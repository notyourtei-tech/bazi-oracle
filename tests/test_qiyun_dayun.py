import unittest
from datetime import datetime, timedelta
from core.geo_time_engine import build_time_bundle
from core.calendar_engine import compute_bazi_from_solar_time
from core.qiyun_engine import calc_qiyun_and_dayun

class TestQiYunDayun(unittest.TestCase):
    def test_dayun_starts_from_qiyun_time(self):
        local_dt = datetime(2006, 5, 13, 17, 30)
        tb = build_time_bundle("CN", local_dt)
        cal = compute_bazi_from_solar_time(tb["solar_time"])
        year_gz = "".join(cal.pillars.year)
        month_gz = "".join(cal.pillars.month)
        qiyun_info, dayun = calc_qiyun_and_dayun(
            birth_solar_dt=tb["solar_time"],
            year_gz=year_gz,
            month_gz=month_gz,
            gender="male",
            tz_offset_hours=tb["tz_offset_hours"]
        )
        self.assertEqual(dayun[0]["start_dt"], qiyun_info["qiyun_time"])
        fmt = "%Y-%m-%d %H:%M"
        start0 = datetime.strptime(dayun[0]["start_dt"], fmt)
        start1 = datetime.strptime(dayun[1]["start_dt"], fmt)
        delta = start1 - start0
        self.assertEqual(delta, timedelta(days=3650))
        for i in range(1, len(dayun)):
            prev = datetime.strptime(dayun[i-1]["start_dt"], fmt)
            curr = datetime.strptime(dayun[i]["start_dt"], fmt)
            self.assertEqual(curr - prev, timedelta(days=3650))
            # check gz progression by one each step relative to month_gz
            # ensure length is 10 years by end_dt - start_dt
            end = datetime.strptime(dayun[i]["end_dt"], fmt)
            self.assertEqual(end - curr, timedelta(days=3650) - timedelta(days=1))

if __name__ == "__main__":
    unittest.main()
