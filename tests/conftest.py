import pytest
from flask import Flask

from src.flask_shoppingcart._shoppingcart import ShoppingCartBase
from src.flask_shoppingcart.flask_shoppingcart import FlaskShoppingCart

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1234"
    app.config['TESTING'] = True
    app.config['FLASK_SHOPPING_CART_COOKIE_NAME'] = 'test_cart'

    return app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def cart(app: Flask):
    return FlaskShoppingCart(app)


@pytest.fixture
def cart_base(app: Flask):
    return ShoppingCartBase(app)
