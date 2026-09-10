"""Regression checks for the client-side localization contract."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
I18N_DIR = ROOT / "static" / "i18n"
LOCALES = ("zh", "en", "ja", "ko", "vi", "my")
INTENTIONALLY_EMPTY = {"score_unit", "year_suffix"}


def _reject_duplicate_keys(pairs: list[tuple[str, str]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate translation key: {key}")
        result[key] = value
    return result


def _load_locale(locale: str) -> dict[str, str]:
    with (I18N_DIR / f"{locale}.json").open(encoding="utf-8") as source:
        return json.load(source, object_pairs_hook=_reject_duplicate_keys)


def test_all_locales_have_the_same_translation_keys():
    base_keys = set(_load_locale("zh"))
    for locale in LOCALES[1:]:
        assert set(_load_locale(locale)) == base_keys, locale


def test_localized_strings_are_present_when_the_ui_needs_them():
    for locale in LOCALES:
        empty = {
            key
            for key, value in _load_locale(locale).items()
            if not isinstance(value, str) or not value.strip()
        }
        assert empty <= INTENTIONALLY_EMPTY, f"{locale}: {sorted(empty)}"


def test_static_i18n_references_are_defined_in_the_base_locale():
    base_keys = set(_load_locale("zh"))
    references: set[str] = set()
    for template in (ROOT / "templates").glob("*.html"):
        text = template.read_text(encoding="utf-8")
        references.update(re.findall(r'data-i18n="([a-zA-Z0-9_]+)"', text))
        references.update(re.findall(r'data-i18n-(?:placeholder|title|aria-label|content)="([a-zA-Z0-9_]+)"', text))
        references.update(re.findall(r'title-i18n="([a-zA-Z0-9_]+)"', text))
    assert references <= base_keys, sorted(references - base_keys)


def test_non_cjk_locales_do_not_contain_accidental_chinese_characters():
    han = re.compile(r"[\u4e00-\u9fff]")
    for locale in ("en", "ko", "vi", "my"):
        offenders = {
            key: value
            for key, value in _load_locale(locale).items()
            if han.search(value)
        }
        assert not offenders, f"{locale}: {offenders}"


def test_five_element_reading_advice_is_localized():
    """Prevent the visible result-page advice from silently falling back to English."""
    english = _load_locale("en")
    prefixes = ("wx_analysis_", "wx_advice_")

    for locale in ("ja", "ko", "vi", "my"):
        localized = _load_locale(locale)
        for key, english_value in english.items():
            if key.startswith(prefixes):
                assert localized[key] != english_value, (
                    f"{locale}.json:{key} unexpectedly falls back to English"
                )
