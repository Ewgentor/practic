from flask import Flask, render_template, url_for
import json


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/catalog")
def catalog():
    with open('static/db/products.json', encoding='utf-8') as f:
        data = json.load(f)['products']
    return render_template('catalog.html', data=data)


@app.route("/news")
def news():
    return render_template('news.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)