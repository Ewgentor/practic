from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/catalog")
def catalog():
    return render_template('catalog.html')


@app.route("/news")
def news():
    return render_template('news.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)