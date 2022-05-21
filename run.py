import json
from flask import Flask, make_response
from flask_shoppigcart import ShoppingCart

app = Flask(__name__)

shopping_cart = ShoppingCart(app=app)

class MyProduct():
    name = "My Product"
    id = "abcd"
    # stock = 19


@app.route("/")
def index():
    return "Hello World!"

@app.route("/add_product/")
def add_product():
    product = MyProduct()
    return shopping_cart.add(product, 2)

@app.route("/remove_product/<product_token>")
def remove_product(product_token):
    return shopping_cart.remove(product_token)

@app.route("/substract/<product_token>/<quantity>")
def substract(product_token, quantity):
    return shopping_cart.substract(product_token, quantity)

@app.route("/get_cart/")
def get_cart():
    return make_response(shopping_cart.get_cart(), 200)

@app.route("/get_total/")
def get_total():
    return make_response(str(shopping_cart.get_cart_quantity()), 200)

@app.route("/clear_cart/")
def clear_cart():
    return shopping_cart.clear()


@app.route("/add/custom_response/")
def add_custom_response():
    product = MyProduct()
    shopping_cart.response = "This is my response" # url_for("index") || redirect("/") || redirect(url_for("index")) 
    return shopping_cart.add(product, 2)

@app.before_request 
def before_request():
    shopping_cart.response = "Shopping Cart Response"

if __name__ == "__main__":
    app.run(debug=True)