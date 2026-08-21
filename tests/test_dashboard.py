from pathlib import Path

import pandas as pd
import pytest

from app import app
from dataset import load_covid_data
from forecasts import (
    WEEK_HORIZON,
    forecast_series,
    holt_horizon_until_zero,
    next_dates,
    polynomial_forecast,
    ses_forecast,
)


def test_load_covid_data_uses_named_columns():
    data = load_covid_data()
    assert data.dates[0] == "11.03.2020"
    assert data.dates[-1] == "31.05.2022"
    assert len(data.dates) == 812
    assert data.gvs[0] == 1
    assert data.gunluk_vaka_sayisi[-1] == 975
    assert data.max_date.isoformat() == "2022-05-31"


def test_until_date_filters_history():
    data = load_covid_data(until="2021-07-03")
    assert data.dates[-1] == "03.07.2021"
    assert len(data.dates) == 480
    assert data.tvs[-1] == 5_440_368


def test_missing_csv_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_covid_data(tmp_path / "missing.csv")


def test_forecast_lengths_match_dashboard_tables():
    data = load_covid_data()
    history = data.gvs[-30:]
    dates = data.date_index[-30:]
    horizon, message_key = holt_horizon_until_zero(history, dates)
    forecast = forecast_series(history, dates, horizon)

    assert len(polynomial_forecast(history)) == WEEK_HORIZON
    assert len(ses_forecast(history, dates)) == 1
    assert len(forecast.holt_week) == WEEK_HORIZON
    assert len(forecast.holt_finish) == horizon
    assert horizon >= 1
    assert message_key in {"forecast_end_date", "forecast_capped"}


def test_next_dates_are_dayfirst():
    assert next_dates("03.07.2021", 2) == ["04.07.2021", "05.07.2021"]


def test_invalid_columns_are_rejected(tmp_path: Path):
    csv_path = tmp_path / "bad.csv"
    pd.DataFrame({"date": ["01.01.2021"], "patients": [1]}).to_csv(csv_path, index=False)
    with pytest.raises(ValueError, match="kolonlar"):
        load_covid_data(csv_path)


def test_dashboard_defaults_to_turkish():
    response = app.test_client().get("/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Türkiye Verileri" in body
    assert "31.05.2022" in body
    assert 'lang="tr"' in body


def test_dashboard_english_and_date_filter():
    response = app.test_client().get("/?lang=en&until=2021-07-03")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Turkey Data" in body
    assert "Daily Patients" in body
    assert "03.07.2021" in body
    assert "31.05.2022" not in body
