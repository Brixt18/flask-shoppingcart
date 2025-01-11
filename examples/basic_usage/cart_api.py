from flask import Flask, redirect, url_for, jsonify, make_response, request, render_template_string
from src.flask_shoppingcart import ShoppingCart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

shopping_cart = ShoppingCart(app)


# Sample products list
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.0},
    {'id': 2, 'name': 'Product 2', 'price': 20.0},
    {'id': 3, 'name': 'Product 3', 'price': 30.0},
]

@app.before_request
def before_request():
    shopping_cart.response = make_response(redirect(url_for('view_cart')))

@app.route('/add/<product_id>')
def add_to_cart(product_id: str):
    product = next((p for p in products if str(p['id']) == product_id), None)
    if product:
        shopping_cart.add(product_id, request.args.get('quantity', 1, type=int))

    return shopping_cart.response

@app.route('/subtract/<product_id>')
def subtract_from_cart(product_id):
    shopping_cart.subtract(str(product_id), request.args.get('quantity', 1, type=int))
    return shopping_cart.response

@app.route('/remove/<product_id>')
def remove_from_cart(product_id):
    shopping_cart.remove(product_id)
    return shopping_cart.response

@app.route('/clear')
def clear_cart():
    shopping_cart.clear()
    return shopping_cart.response

@app.route('/cart')
def view_cart():
    return jsonify(shopping_cart.get_cart())

@app.route('/render-html')
def render_html():
    shopping_cart.response = make_response(
        render_template_string("<h1>Shopping Cart</h1>"),
        200
    )
    shopping_cart.add("1", 2)

    return shopping_cart.response

if __name__ == '__main__':
    app.run(debug=True)
