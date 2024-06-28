from flask import Flask, render_template, request, url_for, session, jsonify
import datetime
import json


app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(minutes=1)

app.secret_key = b'0hLZKNwf_9urI.x5'
session = session
with open('static/db/products.json', encoding='utf-8') as f:
    data = json.load(f)['products']


def count_products(cart):
    counts = {}
    for item in cart:
        item_id = item['id']
        if item_id in counts:
            counts[item_id] += 1
        else:
            counts[item_id] = 1
    return counts


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


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    product = next((p for p in data if p['id'] == product_id), None)
    if product:
        session['cart'].append(product)
        session.modified = True
        return jsonify({'message': f'{product["name"]} добавлен(а) в корзину.'})
    else:
        return jsonify({'message': 'Товар не найден.'}), 404


@app.route("/news")
def news():
    return render_template('news.html')


@app.route("/cart")
def cart():
    cart = session.get('cart', [])
    product_counts = count_products(cart)
    return render_template('cart.html', cart=cart, product_counts=product_counts)


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