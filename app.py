from flask import Flask, render_template
import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import datetime
app = Flask(__name__)


@app.route("/")
def hello():

    def get_seven_days_prediction(a, b):
        y_7 = []
        X = np.asarray(a)
        X = X.reshape(-1, 1)
        y = b

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Fitting Polynomial Regression to the dataset
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(X)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, y)

        for i in range(1,8):
            y_7.append(int(pol_reg.predict(poly_reg.fit_transform([[len(y)+i]]))[0]))

        return y_7

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
        enddate = pd.to_datetime(startdate) + pd.DateOffset(days=i)
        enddate = enddate.strftime('%d.%m.%Y')
        seven_days_period.append(enddate)

    gvs_7 = get_seven_days_prediction(indexes,gvs)
    tvs_7 = get_seven_days_prediction(indexes,tvs)

    gis_7 = get_seven_days_prediction(indexes,gis)
    tis_7 = get_seven_days_prediction(indexes,tis)

    gvs2_7 = get_seven_days_prediction(indexes,gvs2)
    tvs2_7 = get_seven_days_prediction(indexes,tvs2)

    gts_7 = get_seven_days_prediction(indexes,gts)
    tts_7 = get_seven_days_prediction(indexes,tts)

    print(tvs_7)

    return render_template('dashboard.html', dates=dates, gvs=gvs, tvs=tvs, gis=gis, tis=tis, gvs2=gvs2, tvs2=tvs2, gts=gts, tts=tts, titles=titles,
        gvs_7=gvs_7, tvs_7=tvs_7, gis_7=gis_7, tis_7=tis_7, gvs2_7=gvs2_7, tvs2_7=tvs2_7, gts_7=gts_7, tts_7 = tts_7, seven_days_period=seven_days_period)


if __name__ == "__main__":
    app.run(debug=True)
