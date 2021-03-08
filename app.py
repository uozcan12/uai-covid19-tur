import asyncio
import time

import numpy as np
import pandas as pd
from flask import Flask, render_template
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.api import Holt, SimpleExpSmoothing

app=Flask(__name__)

async def async_get_seven_days_prediction(a, b):
    y_1=[]
    X=np.asarray(a)
    X=X.reshape(-1, 1)
    y=b

    # Fitting Polynomial Regression to the dataset
    poly_reg=PolynomialFeatures(degree=3)
    X_poly=poly_reg.fit_transform(X)
    pol_reg=LinearRegression()
    pol_reg.fit(X_poly, y)

    for i in range(1,8):
        y_1.append(int(pol_reg.predict(poly_reg.fit_transform([[len(y)+i]]))[0]))
    return y_1

async def get_simple_smoothing_value(first_list, date_list):
    data_series=pd.Series(first_list, date_list)
    fit=SimpleExpSmoothing(data_series).fit(smoothing_level=0.2,optimized=False)
    fcast=fit.forecast(1)
    return fcast

async def get_holt_value(first_list, date_list):
    data_series=pd.Series(first_list, date_list)
    fit=Holt(data_series).fit(smoothing_level=0.8, smoothing_trend=0.2, optimized=False)
    fcast=fit.forecast(7).rename(r'$\alpha=0.2$')
    return fcast

async def get_holt_finish(first_list, date_list, day_after):
    data_series=pd.Series(first_list, date_list)
    fit=Holt(data_series).fit(smoothing_level=0.8, smoothing_trend=0.2, optimized=False)
    fcast=fit.forecast(day_after).rename(r'$\alpha=0.2$')
    return fcast

@app.route("/")
def hello():
    def convert_date(date_string):
        date_string=date_string.split(".")
        new_date=date_string[1]+"/"+date_string[0]+"/"+date_string[2]
        return(new_date)

    def get_holt_finish_getnumber(first_list, date_list):
        try:
            data_series = pd.Series(first_list, date_list)
            fit = Holt(data_series).fit(smoothing_level=0.8, smoothing_trend=0.2, optimized=False)
            test_forecast=[]
            forecast_message=""
            for i in range(1,1000):
                test_forecast = fit.forecast(i) 
                res = all(i < j for i, j in zip(test_forecast, test_forecast[1:])) 
                if(test_forecast[-1]<=0 and str(res)):
                    forecast_message="Tahmini Bitiş Tarihi"
                    fcast = i
                    break
                else:
                    fcast = 100
                    forecast_message = "100 Gün Sonrasının Tahmini"
        except UnboundLocalError as e:
            raise e
        
        return fcast, forecast_message

    start_time = time.time()
    # data/COVID_API.csv
    # https://raw.githubusercontent.com/ozanerturk/covid19-turkey-api/master/dataset/timeline.csv
    df=pd.read_csv('https://raw.githubusercontent.com/ozanerturk/covid19-turkey-api/master/dataset/timeline.csv', index_col=False)
    titles=['Tarih', 'Günlük Vaka Sayısı', 'Toplam Vaka Sayısı', 'Günlük İyileşen Sayısı', 'Toplam İyileşen Sayısı', 
            'Günlük Vefat Sayısı', 'Toplam Vefat Sayısı', 'Günlük Test Sayısı', 'Toplam Test Sayısı']

    dates=df[df.columns[10]].tolist()
    dates=[x.replace("/",".") for x in dates]
    
    gvs=df[df.columns[0]].tolist()
    tvs=df[df.columns[1]].tolist()
    
    gis=df[df.columns[4]].tolist()
    tis=df[df.columns[5]].tolist()
    
    gvs2=df[df.columns[2]].tolist()
    tvs2=df[df.columns[3]].tolist()
    
    gts=df[df.columns[8]].tolist()
    tts=df[df.columns[9]].tolist()
    
    indexes= [i for i in range(1,len(tts)+1)]

    seven_days_period=[]
    for i in range(1,8):
        startdate=dates[-1]
        enddate=pd.to_datetime(startdate, dayfirst=True) + pd.DateOffset(days=i)
        enddate=enddate.strftime('%d.%m.%Y')
        seven_days_period.append(enddate)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    responses = loop.run_until_complete(asyncio.gather(
        async_get_seven_days_prediction(indexes,gvs),
        async_get_seven_days_prediction(indexes,tvs),
        async_get_seven_days_prediction(indexes,gis),
        async_get_seven_days_prediction(indexes,tis),
        async_get_seven_days_prediction(indexes,gvs2),
        async_get_seven_days_prediction(indexes,tvs2),
        async_get_seven_days_prediction(indexes,gts),
        async_get_seven_days_prediction(indexes,tts),
    ))    
   
    gvs_1 = responses[0]
    tvs_1 = responses[1]
    gis_1 = responses[2]
    tis_1 = responses[3]
    gvs2_1 = responses[4]
    tvs2_1 = responses[5]
    gts_1 = responses[6]
    tts_1 = responses[7]
 
    dates_range=pd.date_range(start=convert_date(dates[0]), end=convert_date(dates[-1]))

    responses_simple_smoothing = loop.run_until_complete(asyncio.gather(
        get_simple_smoothing_value(gvs,dates_range),
        get_simple_smoothing_value(tvs,dates_range),
        get_simple_smoothing_value(gis,dates_range),
        get_simple_smoothing_value(tis,dates_range),
        get_simple_smoothing_value(gvs2,dates_range),
        get_simple_smoothing_value(tvs2,dates_range),
        get_simple_smoothing_value(gts,dates_range),
        get_simple_smoothing_value(tts,dates_range)
    )) 

    gvs_simple_smoothing_tomorrow = responses_simple_smoothing[0]
    tvs_simple_smoothing_tomorrow = responses_simple_smoothing[1]
    gis_simple_smoothing_tomorrow = responses_simple_smoothing[2]
    tis_simple_smoothing_tomorrow = responses_simple_smoothing[3]
    gvs2_simple_smoothing_tomorrow = responses_simple_smoothing[4]
    tvs2_simple_smoothing_tomorrow = responses_simple_smoothing[5]
    gts_simple_smoothing_tomorrow = responses_simple_smoothing[6]
    tts_simple_smoothing_tomorrow = responses_simple_smoothing[7]

    responses_holt_value = loop.run_until_complete(asyncio.gather(
        get_holt_value(gvs,dates_range),
        get_holt_value(tvs,dates_range),
        get_holt_value(gis,dates_range),
        get_holt_value(tis,dates_range),
        get_holt_value(gvs2,dates_range),
        get_holt_value(tvs2,dates_range),
        get_holt_value(gts,dates_range),
        get_holt_value(tts,dates_range)
    )) 

    gvs_holt_week = responses_holt_value[0]
    tvs_holt_week = responses_holt_value[1]
    gis_holt_week = responses_holt_value[2]
    tis_holt_week = responses_holt_value[3]
    gvs2_holt_week = responses_holt_value[4]
    tvs2_holt_week = responses_holt_value[5]
    gts_holt_week = responses_holt_value[6]
    tts_holt_week = responses_holt_value[7]

    gvs_holt_finish, for_message = get_holt_finish_getnumber(gvs,dates_range)
    start_pred_date = dates[-1]
    end_pred_date = pd.to_datetime(start_pred_date, dayfirst=True) + pd.DateOffset(gvs_holt_finish-1)
    end_pred_date = end_pred_date.strftime('%d.%m.%Y')
    day_after = gvs_holt_finish-1

    responses_holt_finish = loop.run_until_complete(asyncio.gather(
        get_holt_finish(gvs,dates_range,day_after), 
        get_holt_finish(tvs,dates_range,day_after),
        get_holt_finish(gis,dates_range,day_after),
        get_holt_finish(tis,dates_range,day_after),
        get_holt_finish(gvs2,dates_range,day_after),
        get_holt_finish(tvs2,dates_range,day_after),
        get_holt_finish(gts,dates_range,day_after),
        get_holt_finish(tts,dates_range,day_after)
    )) 

    gvs_holt_finish = responses_holt_finish[0] 
    tvs_holt_finish = responses_holt_finish[1]
    gis_holt_finish = responses_holt_finish[2]
    tis_holt_finish = responses_holt_finish[3]
    gvs2_holt_finish = responses_holt_finish[4]
    tvs2_holt_finish = responses_holt_finish[5]
    gts_holt_finish = responses_holt_finish[6]
    tts_holt_finish = responses_holt_finish[7]
    
    end_time = time.time()
    total_time = end_time-start_time
    print(f"total_time: {total_time}")

    return render_template('dashboard.html',
        dates=dates,
        gvs=gvs,
        tvs=tvs,
        gis=gis,
        tis=tis,
        gvs2=gvs2,
        tvs2=tvs2,
        gts=gts,
        tts=tts,
        titles=titles,
        gvs_1=gvs_1,
        tvs_1=tvs_1,
        gis_1=gis_1,
        tis_1=tis_1,
        gvs2_1=gvs2_1,
        tvs2_1=tvs2_1,
        gts_1=gts_1,
        tts_1=tts_1,
        seven_days_period=seven_days_period,
        gvs_simple_smoothing_tomorrow=gvs_simple_smoothing_tomorrow,
        tvs_simple_smoothing_tomorrow=tvs_simple_smoothing_tomorrow,
        gis_simple_smoothing_tomorrow=gis_simple_smoothing_tomorrow,
        tis_simple_smoothing_tomorrow=tis_simple_smoothing_tomorrow,
        gvs2_simple_smoothing_tomorrow=gvs2_simple_smoothing_tomorrow,
        tvs2_simple_smoothing_tomorrow=tvs2_simple_smoothing_tomorrow,
        gts_simple_smoothing_tomorrow=gts_simple_smoothing_tomorrow,
        tts_simple_smoothing_tomorrow=tts_simple_smoothing_tomorrow,
        gvs_holt_week=gvs_holt_week,
        tvs_holt_week=tvs_holt_week,
        gis_holt_week=gis_holt_week,
        tis_holt_week=tis_holt_week,
        gvs2_holt_week=gvs2_holt_week,
        tvs2_holt_week=tvs2_holt_week,
        gts_holt_week=gts_holt_week,
        tts_holt_week=tts_holt_week,
        gvs_holt_finish=gvs_holt_finish,
        tvs_holt_finish=tvs_holt_finish,
        gis_holt_finish=gis_holt_finish,
        tis_holt_finish=tis_holt_finish,
        gvs2_holt_finish=gvs2_holt_finish,
        tvs2_holt_finish=tvs2_holt_finish,
        gts_holt_finish=gts_holt_finish,
        tts_holt_finish=tts_holt_finish,
        end_pred_date=end_pred_date,
        for_message=for_message
    )

if __name__ == "__main__":
    app.run(debug=True, port=5002)
