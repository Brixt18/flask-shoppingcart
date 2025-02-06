# Flask-Shoppingcart
Flask-Shoppingcart is an extension to help you to build a simple shopping-cart to your e-commerce or anything that needs a shopping-cart usage in your [Flask](https://flask.palletsprojects.com/en/stable/) application.

## Instalation
Install the extension with pip:
```shell
$ pip install flask-shoppingcart 
```

## A Basic Example
Let's walk through setting up a basic application. Note that this is a very basic guide: we will be taking shortcuts here that you should never take in a real application.

To begin we'll set up a Flask app and a `FlaskShoppingCart` from Flask-Shoppingcart.

```python
import flask
from flask_shoppingcart import FlaskShoppingCart

app = flask.Flask(__name__)
app.secret_key = "super secret string"  # Change this!

shoppingcart = FlaskShoppingCart(app)
```

Then we will be able to manage our shopping cart from it:
```python
@app.route("/")
def example_route():
    my_product_id = 1  # this could be a query to the database, get by a query-param in the URL or something like that
    
    # Adding a product to the cart
    shopping_cart.add(my_product_id, quantity=5)  # the quantity is 1 by default

    # Subtracting a specific quantity from the cart 
    shopping_cart.subtract(my_product_id, quantity=3) # Now the quantity in the cart for this product should be 2

    # Removing it from the cart. Other products in the cart will ramain unmodified
    shopping_cart.remove(my_product_id)

    # Removing all items from the cart, the cart now is empty
    shopping_cart.clear()

    return "wow, this is awesome!"
```

## API Reference
If you are looking for information on a specific function, class or method, this part of the documentation is for you.

we will be taking shortcuts here that you should never take in a real application or take some things for granted (like imports).

### The FlaskShoppingCart class
The `FlaskShoppingCart` is the main class that you will use to manage your cart throughout your entire application, with it you will be able to `add`, `subtract`, `remove` and `clear` your user's carts, along with other methods that you might add.

You can instance it as a simple Flask application:
```python
from flask import Flask
from flask_shoppingcart import FlaskShoppingCart

app = Flask(__name__)
shopping_cart = FlaskShoppingcart(app)
```

or as an advanced one:
```python
from flask import Flask
from flask_shoppingcart import FlaskShoppingCart

app = Flask(__name__)
shopping_cart = FlaskShoppingcart(app)

def create_app():
    shopping_cart.init_app(app)

    return app
```

and then use it as others extensions
```python
from app import shopping_cart

@app.route("/")
def my_route():
    shopping_cart.add(1)

    return jsonify(shopping_cart.cart)
```
In order to work with the application's cookies, `FlaskShoppingCart` adds an [`after_request`](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.after_request) to the application to apply the modified and/or created cookie to manage the cart, otherwise the extension would not be able to manage the products in the user's cart.