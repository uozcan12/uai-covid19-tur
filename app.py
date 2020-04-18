from flask import Flask, render_template
import csv
import pandas as pd
app = Flask(__name__)


@app.route("/")
def hello():
    df = pd.read_csv('./data/COVID.csv', index_col=False)
    #map(lambda x: x if x != '-' else '0', df)
    titles = list(df.columns.values)
    dates = df[df.columns[0]].tolist()
    gvs = df[df.columns[1]].tolist()
    tvs = df[df.columns[2]].tolist()
    gis = df[df.columns[3]].tolist()
    tis = df[df.columns[4]].tolist()
    gvs2 = df[df.columns[5]].tolist()
    tvs2 = df[df.columns[6]].tolist()
    gts = df[df.columns[7]].tolist()
    #gts = list(map(lambda b: b.replace("-","0"), gts))
    tts = df[df.columns[8]].tolist()
    #tts = list(map(lambda b: b.replace("-","0"), tts))

    return render_template('dashboard.html', dates=dates, gvs=gvs, tvs=tvs, gis=gis, tis=tis, gvs2=gvs2, tvs2=tvs2, gts=gts, tts=tts, titles=titles)


if __name__ == "__main__":
    app.run(debug=True)
