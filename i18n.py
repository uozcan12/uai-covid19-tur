from __future__ import annotations

SUPPORTED_LANGUAGES = ("tr", "en")
DEFAULT_LANGUAGE = "tr"

TRANSLATIONS = {
    "tr": {
        "page_title": "COVID UAI Team",
        "brand": "UAI Team",
        "dashboard": "Dashboard",
        "daily_patients": "Günlük Hasta Sayısı",
        "total_patients": "Toplam Hasta Sayısı",
        "daily_cases": "Günlük Vaka Sayısı",
        "daily_recovered": "Günlük İyileşen Sayısı",
        "total_recovered": "Toplam İyileşen Sayısı",
        "daily_deaths": "Günlük Vefat Sayısı",
        "total_deaths": "Toplam Vefat Sayısı",
        "daily_tests": "Günlük Test Sayısı",
        "total_tests": "Toplam Test Sayısı",
        "turkey_data": "Türkiye Verileri",
        "date": "Tarih",
        "forecast_end_date": "Tahmini Bitiş Tarihi",
        "forecast_capped": "{days} Gün Sonrasının Tahmini",
        "holt_week": "7 Günlük Tahmini Veriler (Holt)",
        "poly_tomorrow": "Yarının Tahmini Verisi (Polinom Regresyon)",
        "ses_tomorrow": "Yarının Tahmini Verisi (Basit Düzleştirme)",
        "coded_by": "Geliştiren",
        "loading": "Yükleniyor",
        "select_date": "Veriyi bu tarihe kadar göster",
        "lang_tr": "Türkçe",
        "lang_en": "English",
    },
    "en": {
        "page_title": "COVID UAI Team",
        "brand": "UAI Team",
        "dashboard": "Dashboard",
        "daily_patients": "Daily Patients",
        "total_patients": "Total Patients",
        "daily_cases": "Daily Cases",
        "daily_recovered": "Daily Recovered",
        "total_recovered": "Total Recovered",
        "daily_deaths": "Daily Deaths",
        "total_deaths": "Total Deaths",
        "daily_tests": "Daily Tests",
        "total_tests": "Total Tests",
        "turkey_data": "Turkey Data",
        "date": "Date",
        "forecast_end_date": "Estimated End Date",
        "forecast_capped": "Forecast {days} Days Ahead",
        "holt_week": "7-Day Forecast (Holt)",
        "poly_tomorrow": "Tomorrow's Forecast (Polynomial Regression)",
        "ses_tomorrow": "Tomorrow's Forecast (Simple Smoothing)",
        "coded_by": "Coded by",
        "loading": "Loading",
        "select_date": "Show data up to this date",
        "lang_tr": "Turkish",
        "lang_en": "English",
    },
}


def normalize_language(value: str | None) -> str:
    if value in SUPPORTED_LANGUAGES:
        return value
    return DEFAULT_LANGUAGE


def translations(lang: str) -> dict[str, str]:
    language = normalize_language(lang)
    return TRANSLATIONS[language]


def table_titles(lang: str) -> list[str]:
    t = translations(lang)
    return [
        t["date"],
        t["daily_patients"],
        t["total_patients"],
        t["daily_recovered"],
        t["total_recovered"],
        t["daily_deaths"],
        t["total_deaths"],
        t["daily_tests"],
        t["total_tests"],
    ]
