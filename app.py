from __future__ import annotations

from flask import Flask, make_response, render_template, request, url_for

from dataset import CovidData, load_covid_data
from forecasts import WEEK_HORIZON, forecast_series, holt_horizon_until_zero, next_dates
from i18n import normalize_language, table_titles, translations

app = Flask(__name__)


def build_dashboard_context(data: CovidData, lang: str) -> dict:
    t = translations(lang)
    metrics = data.metric_series()
    finish_steps, message_key = holt_horizon_until_zero(metrics["gvs"], data.date_index)
    finish_message = t[message_key].format(days=finish_steps)
    context = {
        "lang": lang,
        "t": t,
        "titles": table_titles(lang),
        "dates": data.dates,
        "gunluk_vaka_sayisi": data.gunluk_vaka_sayisi,
        "seven_days_period": next_dates(data.dates[-1], WEEK_HORIZON),
        "end_pred_date": next_dates(data.dates[-1], finish_steps)[-1],
        "for_message": finish_message,
        "min_date": data.min_date.isoformat(),
        "max_date": data.max_date.isoformat(),
        "selected_date": data.selected_date.isoformat(),
        "tr_url": url_for("dashboard", lang="tr", until=data.selected_date.isoformat()),
        "en_url": url_for("dashboard", lang="en", until=data.selected_date.isoformat()),
        **metrics,
    }
    for key, history in metrics.items():
        forecast = forecast_series(history, data.date_index, finish_steps)
        context[f"{key}_1"] = forecast.polynomial
        context[f"{key}_simple_smoothing_tomorrow"] = forecast.ses
        context[f"{key}_holt_week"] = forecast.holt_week
        context[f"{key}_holt_finish"] = forecast.holt_finish
    return context


@app.route("/")
def dashboard():
    lang = normalize_language(request.args.get("lang") or request.cookies.get("lang"))
    data = load_covid_data(until=request.args.get("until"))
    response = make_response(render_template("dashboard.html", **build_dashboard_context(data, lang)))
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=False)
