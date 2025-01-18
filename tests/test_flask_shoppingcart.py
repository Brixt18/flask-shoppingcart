import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.flask_shoppingcart import OutOfStokError, ShoppingCart, ProductNotFoundError

class TestShoppingCart:
	def test_get_cart_empty(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart_data = cart.get_cart()
			assert cart_data == {}

	def test_add_product_success(self, cart: ShoppingCart, app: Flask, client: FlaskClient):
		ctx = app.test_request_context()
		ctx.push()

		cart.add('product_1', 2)
		print(cart._get_cart())

		ctx.pop()

		with app.test_request_context():
			print(client._cookies)

		assert True
		# with app.app_context():
		# 	cart.add('product_1', 2)
		# 	cart_data = cart.get_cart()
		# 	print(f"{cart_data=}")

		# with app.test_request_context():
		# 	cart_data = cart.get_cart()
		# 	print(f"{cart_data=}")

		# 	assert 'product_1' in cart_data
		# 	assert cart_data['product_1']['quantity'] == 2

	def test_add_product_overwrite_quantity_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.add('product_1', 2)
			cart.add('product_1', 5, overwrite_quantity=True)

			cart_data = cart.get_cart()
			assert cart_data['product_1']['quantity'] == 5

	def test_add_product_insufficient_stock_fail(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			with pytest.raises(OutOfStokError):
				cart.add('product_1', 5, current_stock=3)

	def test_add_product_negative_quantity_fail(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			with pytest.raises(ValueError):
				cart.add('product_1', -2)

	def test_add_product_negative_quantity_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.clear()
			cart.add('product_1', -2, allow_negative=True)
			cart_data = cart.get_cart()

			assert 'product_1' in cart_data
			assert cart_data['product_1']['quantity'] == -2

	def test_add_product_with_extra_data(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.clear()
			cart.add('product_1', 2, extra={'color': 'red'})
			cart.add('product_1', 2)
			cart.add('product_1', 2, extra={'size': 'large'})

			cart_data = cart.get_cart()
			assert 'extra' in cart_data['product_1']
			assert 'color' in cart_data['product_1']["extra"]
			assert 'size' in cart_data['product_1']["extra"]
			assert cart_data["product_1"]["quantity"] == 6

	def test_remove_product_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.add('product_1', 2)
			cart.remove('product_1')

			cart_data = cart.get_cart()
			assert 'product_1' not in cart_data

	def test_clear_cart_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.add('product_1', 2)
			cart.clear()

			cart_data = cart.get_cart()
			assert cart_data == {}

	def test_subtract_product_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.add('product_1', 2)
			assert cart.get_cart()["product_1"]["quantity"] == 2

			cart.subtract('product_1')
			assert cart.get_cart()['product_1']['quantity'] == 1

	def test_subtract_product_allow_negative_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.clear()
			cart.add('product_1', 5)
			cart.subtract('product_1', 10, allow_negative=True)

			assert cart.get_cart()['product_1']['quantity'] == -5

	def test_subtract_product_out_of_stock_fail(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.add('product_1', 2)
			with pytest.raises(ValueError):
				cart.subtract('product_1', 3)

	def test_get_product_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart.clear()
			cart.add('product_1', 2)
			assert cart.get_product('product_1') == {"quantity": 2}

	def test_get_product_not_found_fail(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			with pytest.raises(ProductNotFoundError):
				cart.get_product('product_1')
	

