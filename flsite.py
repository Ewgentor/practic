from flask import Flask, render_template, request, url_for
import json


app = Flask(__name__)


with open('static/db/products.json', encoding='utf-8') as f:
    data = json.load(f)['products']


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/catalog")
def catalog():
    return render_template('catalog.html', data=data)


@app.route("/news")
def news():
    return render_template('news.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/search',methods=['POST'])
def search_results():
    query = request.form['query']
    result = []
    for el in data:
        if query.lower() in data[el]['name'].lower():
            result.append(data[el])
    return render_template('search_results.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)