from flask import Flask, jsonify, request

from src.flask_shoppingcart.flask_shoppingcart import ShoppingCart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

shopping_cart = ShoppingCart(app)


# Sample products list
products = [
    {'id': i}
    for i in range(1, 1000000)
]


@app.route('/add/<product_id>')
def add_to_cart(product_id: str):
    product = next((p for p in products if str(p['id']) == product_id), None)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    shopping_cart.add(product_id, request.args.get('quantity', 1, type=int))

    return jsonify(shopping_cart.get_cart())

@app.route('/subtract/<product_id>')
def subtract_from_cart(product_id):
    shopping_cart.subtract(str(product_id), request.args.get('quantity', 1, type=int))
    
    return jsonify(shopping_cart.get_cart())


@app.route('/remove/<product_id>')
def remove_from_cart(product_id):
    shopping_cart.remove(product_id)
    return jsonify(shopping_cart.get_cart())


@app.route('/clear')
def clear_cart():
    shopping_cart.clear()
    return jsonify(shopping_cart.get_cart())


@app.route('/cart')
def view_cart():
    return jsonify(shopping_cart.get_cart())


@app.route('/cart/<product_id>')
def view_cart_product(product_id):
    return jsonify(shopping_cart.get_product(product_id))


if __name__ == '__main__':
    app.run(debug=True)
