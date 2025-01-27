# Flask-Shoppingcart
Flask-Shoppingcart is an extension to help you to build a simple shopping-cart to your e-commerce or anything that needs a shopping-cart usage.

## A Basic Example
Let's walk through setting up a basic application. Note that this is a very basic guide: we will be taking shortcuts here that you should never take in a real application.

To begin we'll set up a Flask app and a `ShoppingCart` from Flask-Shoppingcart.

```python
import flask
import flask_shoppingcart

app = flask.Flask(__name__)
app.secret_key = "super secret string"  # Change this!

shoppingcart_manager = flask_shoppingcart.ShoppingCart()
shoppingcart_manager.init_app(app)
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
```
To know more about each functionality please read the doc-strings in code.