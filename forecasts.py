from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.api import Holt, SimpleExpSmoothing

POLY_DEGREE = 3
WEEK_HORIZON = 7
FINISH_CAP = 100
SES_LEVEL = 0.2
HOLT_LEVEL = 0.8
HOLT_TREND = 0.2


@dataclass(frozen=True)
class SeriesForecast:
    polynomial: list[int]
    ses: list[int]
    holt_week: list[int]
    holt_finish: list[int]


def to_nonnegative_ints(values) -> list[int]:
    return [max(0, int(round(float(value)))) for value in values]


def polynomial_forecast(history: list[int], steps: int = WEEK_HORIZON) -> list[int]:
    if len(history) <= POLY_DEGREE:
        last_value = history[-1] if history else 0
        return [max(0, int(last_value))] * steps

    X = np.arange(1, len(history) + 1, dtype=float).reshape(-1, 1)
    y = np.asarray(history, dtype=float)
    poly = PolynomialFeatures(degree=POLY_DEGREE, include_bias=True)
    model = LinearRegression().fit(poly.fit_transform(X), y)
    future = np.arange(len(history) + 1, len(history) + steps + 1, dtype=float).reshape(-1, 1)
    predictions = model.predict(poly.transform(future))
    return to_nonnegative_ints(predictions)


def _as_daily_series(history: list[int], dates: pd.DatetimeIndex) -> pd.Series:
    if len(history) != len(dates):
        raise ValueError("Seri uzunluğu tarih indeksi ile eşleşmiyor.")
    series = pd.Series(np.asarray(history, dtype=float), index=dates)
    return series.asfreq("D")


def ses_forecast(history: list[int], dates: pd.DatetimeIndex, steps: int = 1) -> list[int]:
    series = _as_daily_series(history, dates)
    fitted = SimpleExpSmoothing(series, initialization_method="legacy-heuristic").fit(
        smoothing_level=SES_LEVEL,
        optimized=False,
    )
    return to_nonnegative_ints(fitted.forecast(steps))


def _fit_holt(history: list[int], dates: pd.DatetimeIndex):
    series = _as_daily_series(history, dates)
    return Holt(series, initialization_method="legacy-heuristic").fit(
        smoothing_level=HOLT_LEVEL,
        smoothing_trend=HOLT_TREND,
        optimized=False,
    )


def holt_forecast(history: list[int], dates: pd.DatetimeIndex, steps: int) -> list[int]:
    fitted = _fit_holt(history, dates)
    return to_nonnegative_ints(fitted.forecast(max(steps, 1)))


def holt_horizon_until_zero(
    history: list[int],
    dates: pd.DatetimeIndex,
    cap: int = FINISH_CAP,
) -> tuple[int, str]:
    predictions = holt_forecast(history, dates, cap)
    for day, value in enumerate(predictions, start=1):
        if value <= 0:
            return day, "forecast_end_date"
    return cap, "forecast_capped"


def forecast_series(
    history: list[int],
    dates: pd.DatetimeIndex,
    finish_steps: int,
) -> SeriesForecast:
    fitted = _fit_holt(history, dates)
    return SeriesForecast(
        polynomial=polynomial_forecast(history),
        ses=ses_forecast(history, dates, steps=1),
        holt_week=to_nonnegative_ints(fitted.forecast(WEEK_HORIZON)),
        holt_finish=to_nonnegative_ints(fitted.forecast(max(finish_steps, 1))),
    )


def next_dates(last_date: str, days: int) -> list[str]:
    start = pd.to_datetime(last_date, dayfirst=True)
    return [
        (start + pd.DateOffset(days=offset)).strftime("%d.%m.%Y")
        for offset in range(1, days + 1)
    ]
