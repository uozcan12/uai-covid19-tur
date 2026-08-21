from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
CSV_PATH = ROOT_DIR / "data" / "COVID.csv"

REQUIRED_COLUMNS = (
    "patients",
    "totalPatients",
    "deaths",
    "totalDeaths",
    "recovered",
    "totalRecovered",
    "tests",
    "totalTests",
    "date",
    "cases",
)


@dataclass(frozen=True)
class CovidData:
    dates: list[str]
    date_index: pd.DatetimeIndex
    gvs: list[int]
    tvs: list[int]
    gis: list[int]
    tis: list[int]
    gvs2: list[int]
    tvs2: list[int]
    gts: list[int]
    tts: list[int]
    gunluk_vaka_sayisi: list[int]
    min_date: date
    max_date: date
    selected_date: date

    def metric_series(self) -> dict[str, list[int]]:
        return {
            "gvs": self.gvs,
            "tvs": self.tvs,
            "gis": self.gis,
            "tis": self.tis,
            "gvs2": self.gvs2,
            "tvs2": self.tvs2,
            "gts": self.gts,
            "tts": self.tts,
        }


def _int_list(series: pd.Series) -> list[int]:
    return pd.to_numeric(series, errors="coerce").fillna(0).round().astype(int).tolist()


def _reconstruct_total(daily: pd.Series, total: pd.Series) -> pd.Series:
    daily_values = pd.to_numeric(daily, errors="coerce").fillna(0).tolist()
    total_values = pd.to_numeric(total, errors="coerce").tolist()
    reconstructed: list[float] = []
    running = 0.0
    for daily_value, total_value in zip(daily_values, total_values):
        if pd.notna(total_value):
            running = float(total_value)
        else:
            running += float(daily_value)
        reconstructed.append(running)
    return pd.Series(reconstructed)


def parse_until_date(value: str | None, min_date: date, max_date: date) -> date:
    if not value:
        return max_date
    if len(value) >= 10 and value[4] == "-" and value[7] == "-":
        parsed = pd.to_datetime(value[:10], format="%Y-%m-%d", errors="coerce")
    else:
        parsed = pd.to_datetime(value, dayfirst=True, errors="coerce")
    if pd.isna(parsed):
        return max_date
    chosen = parsed.date()
    return min(max(chosen, min_date), max_date)


def load_covid_data(path: Path | None = None, until: str | None = None) -> CovidData:
    csv_path = path or CSV_PATH
    if not csv_path.exists():
        raise FileNotFoundError(f"COVID veri dosyası bulunamadı: {csv_path}")

    frame = pd.read_csv(csv_path)
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"CSV içinde beklenen kolonlar yok: {', '.join(missing)}")

    parsed_dates = pd.to_datetime(frame["date"], dayfirst=True, errors="coerce")
    if parsed_dates.isna().any():
        raise ValueError("CSV içinde çözümlenemeyen tarih var.")

    min_date = parsed_dates.min().date()
    max_date = parsed_dates.max().date()
    selected_date = parse_until_date(until, min_date, max_date)
    frame = frame.loc[parsed_dates.dt.date <= selected_date].copy()
    parsed_dates = pd.to_datetime(frame["date"], dayfirst=True)
    if frame.empty:
        raise ValueError("Seçilen tarih aralığında veri yok.")

    cases = pd.to_numeric(frame["cases"], errors="coerce")
    patients = pd.to_numeric(frame["patients"], errors="coerce").fillna(cases).fillna(0)
    deaths = pd.to_numeric(frame["deaths"], errors="coerce").fillna(0)
    recovered = pd.to_numeric(frame["recovered"], errors="coerce").fillna(0)
    tests = pd.to_numeric(frame["tests"], errors="coerce").fillna(0)

    date_index = pd.DatetimeIndex(parsed_dates.tolist(), freq="D")
    return CovidData(
        dates=parsed_dates.dt.strftime("%d.%m.%Y").tolist(),
        date_index=date_index,
        gvs=_int_list(patients),
        tvs=_int_list(_reconstruct_total(patients, frame["totalPatients"])),
        gis=_int_list(recovered),
        tis=_int_list(_reconstruct_total(recovered, frame["totalRecovered"])),
        gvs2=_int_list(deaths),
        tvs2=_int_list(_reconstruct_total(deaths, frame["totalDeaths"])),
        gts=_int_list(tests),
        tts=_int_list(_reconstruct_total(tests, frame["totalTests"])),
        gunluk_vaka_sayisi=_int_list(cases.fillna(0)),
        min_date=min_date,
        max_date=max_date,
        selected_date=selected_date,
    )
