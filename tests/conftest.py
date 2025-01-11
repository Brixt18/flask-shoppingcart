import pytest
from flask import Flask
from src.flask_shoppingcart import ShoppingCart

@pytest.fixture(scope='class')
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SHOPPING_CART_COOKIE_NAME'] = 'test_cart'

    yield app


@pytest.fixture(scope='class')
def client(app: Flask):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='class')
def cart(app: Flask):
    yield ShoppingCart(app)
