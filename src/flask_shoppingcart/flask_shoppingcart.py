from flask import make_response, Response, request, Flask
import json
import logging
from typing import Any
from numbers import Number
from functools import partial
from .exceptions import OutOfStokError


class ShoppingCart:
	def __init__(self, app: Flask=None) -> None:
		if app is not None:
			self.init_app(app)
		
	def init_app(self, app: Flask) -> None:
		self.app = app
		
		with self.app.app_context():
			self.response: Response = make_response({}, 204)

		self._init_config()
	
	def _init_config(self) -> None:
		self.cookie_name: str = self.app.config.get("SHOPPING_CART_COOKIE_NAME", "products")
		self.allow_negative_quantity: bool = bool(self.app.config.get("FLASK_SHOPPING_CART_ALLOW_NEGATIVE_QUANTITY", 0))

	def _validate_stock(self, current_stock: Number, quantity_to_add: Number, current_quantity: Number) -> None:
		"""
		Validates if the stock is sufficient for the quantity to be added.
		
		Args:
			ignore_stock (bool): Flag to ignore stock validation.
			current_stock (Number): The current stock available.
			quantity_to_add (Number): The quantity of items to add.
			current_quantity (Number): The current quantity of items in the cart.
			
		Raises:
			OutOfStockError: If the total quantity exceeds the current stock.
		"""
		logging.info("Validating stock")

		if (
			(current_stock is not None)
			and ((current_quantity + quantity_to_add) > current_stock)
		):
			raise OutOfStokError()

	def get_cart(self) -> dict[Any, dict]:
		"""
		Retrieve the shopping cart from cookies.
		This method attempts to load the shopping cart data stored in cookies.
		If the cookie with the specified name exists, it will parse the JSON data
		and return it as a dictionary. If the cookie does not exist, it will return
		an empty dictionary.
		
		Returns:
			dict[Any, dict]: The shopping cart data as a dictionary. If the cookie
			does not exist, an empty dictionary is returned.
		"""
		logging.info("Getting cart from cookies")

		cart = (
			json.loads(request.cookies.get(self.cookie_name)) 
			if self.cookie_name in request.cookies 
			else dict()
		)
		logging.debug(f"{cart=}")

		return cart

	def add(self,
		 product_id: str,
		 quantity: Number=1,
		 overwrite_quantity: bool = False,
		 current_stock: Number | None = None,
		 extra: dict | None = None,
		 allow_negative: bool = None
	) -> Response:
		"""
		Add a product to the cart or update the quantity of an existing product.
		
		Args:
			product_id (Any): The ID of the product to add.
			quantity (Number): The quantity of the product to add.
			overwrite_quantity (bool): If True, the quantity will be overwritten instead of added.
			current_stock (Number, optional): The current stock of the product. If set, the stock will be validated.
			extra (dict, optional): Extra data to store in the product.
			allow_negative (bool, optional): If True, the quantity can be negative.
		
		Returns:
			Response: The response after adding the product to the cart.

		Raises:
			OutOfStokError: If the product is out of stock. This error is raise if the ignore_stock is True and the quantity exceeds the current stock.
		"""
		logging.info(f"Adding product to cart")

		_allow_negative = allow_negative or self.allow_negative_quantity
		logging.debug(f"Allow negative quantity flag set to: {_allow_negative}")

		if not _allow_negative and quantity <= 0:
			raise ValueError("Quantity must be greater than 0.")
		
		# Get the products in the cart
		cart: dict[Any, dict] = self.get_cart()
		logging.debug(f"{cart=}")

		product: dict = cart.get(product_id, {})
		logging.debug(f"{product=}")

		_data = {
			"quantity": quantity,
		}

		_validate_stock: partial = partial(self._validate_stock, current_stock, quantity)

		if product:
			logging.debug("Product already in cart")
			_validate_stock(product["quantity"])

			if overwrite_quantity:
				logging.debug("Overwriting product quantity")
				product.update(_data)

			else:
				logging.debug("Adding quantity to product")
				product["quantity"] += quantity
					
		else:
			logging.debug("Product not in cart")
			product = _data
			_validate_stock(0)

		if extra:
			product.update(extra)

		cart[product_id] = product

		self.response.set_cookie(self.cookie_name, json.dumps(cart))
		return self.response
	
	def remove(self, product_id: str) -> Response:
		"""
		Removes a product from the cart.
		
		Args:
			product_id (Any): The ID of the product to remove.
		
		Returns:
			Response: The response after removing the product from the cart.
		"""
		logging.info("Removing product from cart")
		cart: dict[Any, dict] = self.get_cart()
		
		if product_id in cart:
			cart.pop(product_id)
			self.response.set_cookie(self.cookie_name, json.dumps(cart))
		
		return self.response

	def clear(self) -> Response:
		"""
		Clears the cart.
		
		Returns:
			Response: The response after clearing the cart.
		"""
		logging.info("Clearing cart")
		self.response.set_cookie(self.cookie_name, json.dumps({}))

		return self.response
	
	def subtract(self, product_id: str, quantity: Number=1, allow_negative: bool = False) -> Response:
		"""
		Substracts a quantity from a product in the cart.
		
		Args:
			product_id (Any): The ID of the product to substract from.
			quantity (Number): The quantity to substract.
			allow_negative (bool): If True, the quantity can be negative.
		
		Returns:
			Response: The response after substracting the quantity from the product.
		"""
		logging.info("Substracting quantity from product in cart")

		_allow_negative = allow_negative or self.allow_negative_quantity
		logging.debug(f"Allow negative quantity flag set to: {_allow_negative}")

		cart: dict[Any, dict] = self.get_cart()

		if product_id in cart:
			product: dict = cart[product_id]
			product["quantity"] -= quantity

			if (
				not _allow_negative 
				and product["quantity"] <= 0
			):
				raise ValueError(
					"Product quantity cannot be negative nor 0. "
					"To allow negative quantity, set the allow_negative flag to True. "
					"0 values are not allowed, use the remove method instead."
				)
			
			self.response.set_cookie(self.cookie_name, json.dumps(cart))
		
		return self.response