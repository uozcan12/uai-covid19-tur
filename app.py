from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    user = {'username': 'Miguel'}
    return render_template('dashboard.html', title='Home', user=user)

if __name__ == "__main__":
    app.run(debug=True)
