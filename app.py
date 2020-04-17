from flask import Flask, render_template
import csv
import pandas as pd
app = Flask(__name__)

@app.route("/")
def hello():
    df = pd.read_csv('./data/COVID.csv', index_col=False)

    s_array = df["Günlük Vaka Sayısı"]
    print(s_array[0])
    return render_template('dashboard.html', title='Home')
    
if __name__ == "__main__":
    app.run(debug=True)


