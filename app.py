from flask import Flask, render_template
import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import datetime
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

app = Flask(__name__)

@app.route("/")
def hello():
    def convert_date(date_string):
        date_string = date_string.split(".")
        new_date = date_string[1]+"/"+date_string[0]+"/"+date_string[2]
        return(new_date)

    def get_simple_smoothing_value(first_list, date_list):
        data_series = pd.Series(first_list, date_list)
        fit = SimpleExpSmoothing(data_series).fit(smoothing_level=0.2,optimized=False)
        fcast = fit.forecast(1)
        return fcast

    def get_holt_value(first_list, date_list):
        data_series = pd.Series(first_list, date_list)
        fit = Holt(data_series).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
        fcast = fit.forecast(7).rename(r'$\alpha=0.2$')
        return fcast

    def get_holt_finish_getnumber(first_list, date_list):
        data_series = pd.Series(first_list, date_list)
        fit = Holt(data_series).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
        #fcast = fit.forecast(125).rename(r'$\alpha=0.2$')
        fcast = []
        i=1
        while True:
            fcast = fit.forecast(i).rename(r'$\alpha=0.2$')
            i+=1
            if(fcast[-1]<=0):
                break
        return fcast

    def get_holt_finish(first_list, date_list, day_after):
        data_series = pd.Series(first_list, date_list)
        fit = Holt(data_series).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
        fcast = fit.forecast(day_after).rename(r'$\alpha=0.2$')
        return fcast

    def get_seven_days_prediction(a, b):
        y_1 = []
        X = np.asarray(a)
        X = X.reshape(-1, 1)
        y = b

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Fitting Polynomial Regression to the dataset
        poly_reg = PolynomialFeatures(degree=3)
        X_poly = poly_reg.fit_transform(X)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, y)

        for i in range(1,8):
            y_1.append(int(pol_reg.predict(poly_reg.fit_transform([[len(y)+i]]))[0]))
        return y_1

    df = pd.read_csv('./data/COVID.csv', index_col=False)
    titles = list(df.columns.values)
    titles.pop()
    dates = df[df.columns[0]].tolist()
    gvs = df[df.columns[1]].tolist()
    tvs = df[df.columns[2]].tolist()
    gis = df[df.columns[3]].tolist()
    tis = df[df.columns[4]].tolist()
    gvs2 = df[df.columns[5]].tolist()
    tvs2 = df[df.columns[6]].tolist()
    gts = df[df.columns[7]].tolist()
    tts = df[df.columns[8]].tolist()
    indexes = df[df.columns[9]].tolist()

    seven_days_period = []
    for i in range(1,8):
        startdate = dates[-1]
        enddate = pd.to_datetime(startdate, dayfirst=True) + pd.DateOffset(days=i)
        enddate = enddate.strftime('%d.%m.%Y')
        seven_days_period.append(enddate)

    gvs_1 = get_seven_days_prediction(indexes,gvs)
    tvs_1 = get_seven_days_prediction(indexes,tvs)
    gis_1 = get_seven_days_prediction(indexes,gis)
    tis_1 = get_seven_days_prediction(indexes,tis)
    gvs2_1 = get_seven_days_prediction(indexes,gvs2)
    tvs2_1 = get_seven_days_prediction(indexes,tvs2)
    gts_1 = get_seven_days_prediction(indexes,gts)
    tts_1 = get_seven_days_prediction(indexes,tts)

    dates_range = pd.date_range(start = convert_date(dates[0]), end = convert_date(dates[-1]))

    gvs_simple_smoothing_tomorrow = get_simple_smoothing_value(gvs,dates_range);
    tvs_simple_smoothing_tomorrow = get_simple_smoothing_value(tvs,dates_range)
    gis_simple_smoothing_tomorrow = get_simple_smoothing_value(gis,dates_range)
    tis_simple_smoothing_tomorrow = get_simple_smoothing_value(tis,dates_range)
    gvs2_simple_smoothing_tomorrow = get_simple_smoothing_value(gvs2,dates_range)
    tvs2_simple_smoothing_tomorrow = get_simple_smoothing_value(tvs2,dates_range)
    gts_simple_smoothing_tomorrow = get_simple_smoothing_value(gts,dates_range)
    tts_simple_smoothing_tomorrow = get_simple_smoothing_value(tts,dates_range)

    gvs_holt_week = get_holt_value(gvs,dates_range)
    tvs_holt_week = get_holt_value(tvs,dates_range)
    gis_holt_week = get_holt_value(gis,dates_range)
    tis_holt_week = get_holt_value(tis,dates_range)
    gvs2_holt_week = get_holt_value(gvs2,dates_range)
    tvs2_holt_week = get_holt_value(tvs2,dates_range)
    gts_holt_week = get_holt_value(gts,dates_range)
    tts_holt_week = get_holt_value(tts,dates_range)

    gvs_holt_finish = get_holt_finish_getnumber(gvs,dates_range)
    print(len(gvs_holt_finish))
    start_pred_date = dates[-1]
    end_pred_date = pd.to_datetime(start_pred_date, dayfirst=True) + pd.DateOffset(len(gvs_holt_finish))
    end_pred_date = end_pred_date.strftime('%d.%m.%Y')
    print(end_pred_date)

    day_after = len(gvs_holt_finish)
    tvs_holt_finish = get_holt_finish(tvs,dates_range,day_after)
    gis_holt_finish = get_holt_finish(gis,dates_range,day_after)
    tis_holt_finish = get_holt_finish(tis,dates_range,day_after)
    gvs2_holt_finish = get_holt_finish(gvs2,dates_range,day_after)
    tvs2_holt_finish = get_holt_finish(tvs2,dates_range,day_after)
    gts_holt_finish = get_holt_finish(gts,dates_range,day_after)
    tts_holt_finish = get_holt_finish(tts,dates_range,day_after)

    return render_template('dashboard.html', dates=dates, gvs=gvs, tvs=tvs, gis=gis, tis=tis, gvs2=gvs2, tvs2=tvs2, gts=gts, tts=tts, titles=titles,
        gvs_1=gvs_1, tvs_1=tvs_1, gis_1=gis_1, tis_1=tis_1, gvs2_1=gvs2_1, tvs2_1=tvs2_1, gts_1=gts_1, tts_1 = tts_1, seven_days_period=seven_days_period,
        gvs_simple_smoothing_tomorrow = gvs_simple_smoothing_tomorrow,
        tvs_simple_smoothing_tomorrow = tvs_simple_smoothing_tomorrow,
        gis_simple_smoothing_tomorrow = gis_simple_smoothing_tomorrow,
        tis_simple_smoothing_tomorrow = tis_simple_smoothing_tomorrow,
        gvs2_simple_smoothing_tomorrow = gvs2_simple_smoothing_tomorrow,
        tvs2_simple_smoothing_tomorrow = tvs2_simple_smoothing_tomorrow,
        gts_simple_smoothing_tomorrow = gts_simple_smoothing_tomorrow,
        tts_simple_smoothing_tomorrow = tts_simple_smoothing_tomorrow,
        gvs_holt_week = gvs_holt_week,
        tvs_holt_week = tvs_holt_week,
        gis_holt_week = gis_holt_week,
        tis_holt_week = tis_holt_week,
        gvs2_holt_week = gvs2_holt_week,
        tvs2_holt_week = tvs2_holt_week,
        gts_holt_week = gts_holt_week,
        tts_holt_week = tts_holt_week,
        gvs_holt_finish = gvs_holt_finish,
        tvs_holt_finish = tvs_holt_finish,
        gis_holt_finish = gis_holt_finish,
        tis_holt_finish = tis_holt_finish,
        gvs2_holt_finish = gvs2_holt_finish,
        tvs2_holt_finish = tvs2_holt_finish,
        gts_holt_finish = gts_holt_finish,
        tts_holt_finish = tts_holt_finish,
        end_pred_date = end_pred_date
        )

if __name__ == "__main__":
    app.run(debug=True)
