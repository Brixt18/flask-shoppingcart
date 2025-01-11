import pytest
from flask import Flask, Response

from src.flask_shoppingcart import OutOfStokError, ShoppingCart


@pytest.mark.usefixtures("app", "client", "cart")
class TestShoppingCart:

	def _get_cookie(self, response: Response):
		cookie_header = response.headers.getlist('Set-Cookie')[-1]
		assert 'test_cart' in cookie_header

		return cookie_header

	def test_init_app(self, cart: ShoppingCart):
		assert cart.app is not None
		assert cart.cookie_name == 'test_cart'

	def test_get_cart_empty(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			cart_data = cart.get_cart()
			assert cart_data == {}

	def test_add_product_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response = cart.add('product_1', 2)
			cookie_header = self._get_cookie(response)

		with app.test_request_context(headers={'Cookie': cookie_header}):
			cart_data = cart.get_cart()
			
			assert 'product_1' in cart_data
			assert cart_data['product_1']['quantity'] == 2

	def test_add_product_overwrite_quantity_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 2)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}) as ctx:
			response2 = cart.add('product_1', 5, overwrite_quantity=True)
		
		with app.test_request_context(headers={'Cookie': self._get_cookie(response2)}) as ctx:
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
			response = cart.add('product_1', -2, allow_negative=True)
			cookie_header = self._get_cookie(response)

		with app.test_request_context(headers={'Cookie': cookie_header}):
			cart_data = cart.get_cart()
			assert 'product_1' in cart_data
			assert cart_data['product_1']['quantity'] == -2

	def test_add_product_with_extra_data(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 2, extra={'color': 'red'})
		
		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}):
			response2 = cart.add('product_1', 2)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response2)}):
			response3 = cart.add('product_1', 2, extra={'size': 'large'})

		with app.test_request_context(headers={'Cookie': self._get_cookie(response3)}):
			cart_data = cart.get_cart()
			assert 'color' in cart_data['product_1']
			assert 'size' in cart_data['product_1']
			assert cart_data["product_1"]["quantity"] == 6

	def test_remove_product_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 2)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}):
			response2 = cart.remove('product_1')

		with app.test_request_context(headers={'Cookie': self._get_cookie(response2)}):
			cart_data = cart.get_cart()
			assert 'product_1' not in cart_data

	def test_clear_cart_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 2)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}):
			response2 = cart.clear()

		with app.test_request_context(headers={'Cookie': self._get_cookie(response2)}):
			cart_data = cart.get_cart()
			assert cart_data == {}

	def test_subtract_product_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 2)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}):
			response2 = cart.subtract('product_1')

		with app.test_request_context(headers={'Cookie': self._get_cookie(response2)}):
			cart_data = cart.get_cart()
			assert cart_data['product_1']['quantity'] == 1

	def test_subtract_product_allow_negative_success(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 5)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}):
			response2 = cart.subtract('product_1', 10, allow_negative=True)

		with app.test_request_context(headers={'Cookie': self._get_cookie(response2)}):
			cart_data = cart.get_cart()
			assert cart_data['product_1']['quantity'] == -5

	def test_subtract_product_out_of_stock_fail(self, cart: ShoppingCart, app: Flask):
		with app.test_request_context():
			response1 = cart.add('product_1', 2)
		
		with app.test_request_context(headers={'Cookie': self._get_cookie(response1)}):
			with pytest.raises(ValueError):
				cart.subtract('product_1', 3)