"""Regression checks for the mobile app-shell interaction contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mobile_viewport_disables_browser_zoom():
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")

    assert "maximum-scale=1.0" in base
    assert "user-scalable=no" in base
    assert "viewport-fit=cover" in base


def test_mobile_shell_locks_background_and_preserves_normal_single_touch_scroll():
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    stylesheet = (ROOT / "static" / "style.css").read_text(encoding="utf-8")

    assert "function setPageScrollLocked(shouldLock)" in base
    assert "function syncPageScrollLock()" in base
    assert "event.touches.length > 1" in base
    assert "gesturestart" in base
    assert "body.is-scroll-locked" in stylesheet
    assert "overscroll-behavior: none" in stylesheet
    assert "-webkit-overflow-scrolling: touch" in stylesheet


def test_every_fullscreen_overlay_participates_in_scroll_locking():
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    picker = (ROOT / "static" / "timepicker.js").read_text(encoding="utf-8")

    assert ".loading-overlay.active, .time-picker-overlay.active" in base
    assert "showLanguageModal();" in base
    assert "showOnboardModal();" in base
    assert picker.count("syncPageScrollLock()") == 2
