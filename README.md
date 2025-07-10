# Flask-Shoppingcart
Flask-Shoppingcart is an extension to help you to build a simple shopping-cart to your e-commerce or anything that needs a shopping-cart usage in your [Flask](https://flask.palletsprojects.com/en/stable/) application.

## Instalation
Install the extension with pip:
```shell
$ pip install flask-shoppingcart 
```
Find Flask-Shoppingcart at [PyPI](https://pypi.org/project/flask-shoppingcart/0.1.0/)

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

### Methods

#### add()
The `add()` method allows you to add a product to the cart or update the quantity of an existing product.

```python
shopping_cart.add(
    product_id,
    quantity=1,
    overwrite_quantity=False,
    current_stock=None,
    extra=None,
    allow_negative=None
)
```

**Parameters:**
- `product_id` (str): The unique identifier of the product to add to the cart. This ID will be used as the key to store and retrieve the product from the cart.
- `quantity` (Number, optional): The amount of the product to add to the cart. If the product already exists in the cart, this quantity will be added to the existing quantity unless `overwrite_quantity` is set to `True`. Default is 1.
- `overwrite_quantity` (bool, optional): When `True`, the existing quantity of the product in the cart will be replaced with the new quantity value instead of adding to it. When `False`, the new quantity will be added to any existing quantity. Default is `False`.
- `current_stock` (Number, optional): The current available stock for this product. When provided, the method will validate that the total quantity in the cart (existing + new) doesn't exceed this stock limit. If the stock limit would be exceeded, an `OutOfStokError` will be raised. When `None`, no stock validation is performed.
- `extra` (dict, optional): Additional metadata to store with the product in the cart, such as color, size, or any other custom attributes. If the product already exists in the cart and has existing extra data, the new extra data will be merged with the existing data. When `None`, no extra data is added.
- `allow_negative` (bool, optional): When `True`, allows the quantity to be negative, which can be useful for scenarios like returns or adjustments. When `False`, negative quantities will raise a `ValueError`. If not specified, the method will use the instance's default `allow_negative_quantity` setting.
- `overwrite_extra` (bool, optional): When `True`, replaces any existing `extra` data for the product with the new `extra` dictionary provided. When `False`, the new `extra` data will be merged with any existing data (existing keys will be updated, new keys will be added). Default is `False`. If `extra=None` and `overwrite_extra=True`, the `'extra'` key will be deleted from the product.

**Example:**
```python
# Add a product with ID 'product_1' and quantity 2
shopping_cart.add('product_1', 2)

# Add a product with extra data
shopping_cart.add('product_1', 1, extra={'color': 'red', 'size': 'large'})

# Overwrite the quantity instead of adding to it
shopping_cart.add('product_1', 5, overwrite_quantity=True)
```

#### subtract()
The `subtract()` method allows you to subtract a quantity from a product in the cart.

```python
shopping_cart.subtract(
    product_id,
    quantity=1,
    allow_negative=False,
    autoremove_if_0=True
)
```

**Parameters:**
- `product_id` (str): The unique identifier of the product from which to subtract quantity. The product must already exist in the cart, otherwise a `ProductNotFoundError` will be raised.
- `quantity` (Number, optional): The amount to subtract from the product's current quantity in the cart. The result will be the current quantity minus this value. Default is 1.
- `allow_negative` (bool, optional): When `True`, allows the resulting quantity to be negative, which can be useful for scenarios like returns or overpayments. When `False`, if the subtraction would result in a negative quantity, either the product will be removed (if `autoremove_if_0` is `True`) or a `QuantityError` will be raised. Default is `False`.
- `autoremove_if_0` (bool, optional): When `True` and `allow_negative` is `False`, the product will be automatically removed from the cart if the quantity reaches 0 or below. When `False`, a `QuantityError` will be raised instead. This parameter cannot be `True` when `allow_negative` is `True`. Default is `True`.

**Example:**
```python
# Subtract 1 from the quantity
shopping_cart.subtract('product_1')

# Subtract 3 from the quantity
shopping_cart.subtract('product_1', 3)

# Allow negative quantities
shopping_cart.subtract('product_1', 10, allow_negative=True)
```

#### remove()
The `remove()` method removes a product completely from the cart.

```python
shopping_cart.remove(product_id)
```

**Parameters:**
- `product_id` (str): The unique identifier of the product to completely remove from the cart. If the product doesn't exist in the cart, the method will silently do nothing (no error is raised). All data associated with this product, including quantity and extra data, will be permanently deleted from the cart.

**Example:**
```python
shopping_cart.remove('product_1')
```

#### clear()
The `clear()` method removes all products from the cart, making it empty.

```python
shopping_cart.clear()
```

**Parameters:** None - This method takes no parameters and will remove all products and their associated data from the cart, effectively resetting it to an empty state.

**Example:**
```python
shopping_cart.clear()
```

#### get_cart()
The `get_cart()` method returns the current cart data as a dictionary.

```python
cart_data = shopping_cart.get_cart()
```

**Parameters:** None - This method takes no parameters and returns a complete snapshot of the current cart state.

**Returns:**
- `dict`: A dictionary containing all products in the cart, where the keys are product IDs and the values are dictionaries containing product details such as quantity and extra data.

**Example:**
```python
cart_data = shopping_cart.get_cart()
print(cart_data)
# Output: {'product_1': {'quantity': 2, 'extra': {'color': 'red'}}}
```

#### get_product()
The `get_product()` method retrieves a specific product from the cart by its ID.

```python
product = shopping_cart.get_product(product_id)
```

**Parameters:**
- `product_id` (str): The unique identifier of the product to retrieve from the cart. The product must exist in the cart, otherwise a `ProductNotFoundError` will be raised.

**Returns:**
- `dict`: A dictionary containing the product details, including quantity and any extra data that was stored with the product.

**Raises:**
- `ProductNotFoundError`: If the product with the specified ID is not found in the cart.

**Example:**
```python
try:
    product = shopping_cart.get_product('product_1')
    print(f"Quantity: {product['quantity']}")
except ProductNotFoundError:
    print("Product not found in cart")
```

#### get_product_or_none()
The `get_product_or_none()` method retrieves a specific product from the cart by its ID, or returns `None` if not found.

```python
product = shopping_cart.get_product_or_none(product_id)
```

**Parameters:**
- `product_id` (str): The unique identifier of the product to retrieve from the cart. Unlike `get_product()`, this method will not raise an error if the product is not found.

**Returns:**
- `dict` or `None`: A dictionary containing the product details if the product exists in the cart, or `None` if the product is not found. This provides a safe way to check for product existence without handling exceptions.

**Example:**
```python
product = shopping_cart.get_product_or_none('product_1')
if product:
    print(f"Quantity: {product['quantity']}")
else:
    print("Product not found in cart")
```

### Properties

#### cart
The `cart` property provides direct access to the cart data.

```python
cart_data = shopping_cart.cart
```

**Returns:**
- `dict`: The current cart data, equivalent to calling `get_cart()` but accessed as a property for convenience.

**Example:**
```python
print(shopping_cart.cart)
# Output: {'product_1': {'quantity': 2, 'extra': {'color': 'red'}}}
```

### Exceptions

The extension provides custom exceptions to handle different error scenarios:

#### OutOfStokError
Raised when trying to add a product with a quantity that exceeds the available stock.

#### ProductNotFoundError
Raised when trying to access a product that doesn't exist in the cart.

#### QuantityError
Raised when a quantity operation would result in an invalid state, such as a negative quantity when negative quantities are not allowed.

**Example:**
```python
from flask_shoppingcart import OutOfStokError, ProductNotFoundError, QuantityError

try:
    shopping_cart.add('product_1', 10, current_stock=5)
except OutOfStokError:
    print("Not enough stock available")

try:
    shopping_cart.get_product('nonexistent_product')
except ProductNotFoundError:
    print("Product not found in cart")

try:
    shopping_cart.subtract('product_1', 5, allow_negative=False)
except QuantityError:
    print("Invalid quantity")
```