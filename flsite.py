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
    page = request.args.get('page', default=1, type=int)
    per_page = 6
    total_pages = len(data) // per_page + 1
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = data[start:end]
    return render_template('catalog.html', products=paginated_products, total_pages=total_pages)
    # return render_template('catalog.html', data=data)


@app.route("/news")
def news():
    return render_template('news.html')


# Илья, иди нахуй
@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/search',methods=['POST'])
def search_results():
    query = request.form['query']
    result = []
    for product in data:
        if query.lower() in product['name'].lower():
            result.append(product)
    return render_template('search_results.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)