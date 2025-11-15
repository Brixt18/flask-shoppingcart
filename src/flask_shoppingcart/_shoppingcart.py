from typing import Optional

from flask import Flask, session

from .config import (FLASK_SHOPPING_CART_ALLOW_NEGATIVE_QUANTITY,
                     FLASK_SHOPPING_CART_SESSION_NAME)
from .models import CartItem


class ShoppingCartBase:
	def __init__(self, app: Optional[Flask] = None) -> None:
		if app is not None:
			self.init_app(app)

	def init_app(self, app: Flask) -> None:
		self.session_cart_name: str = str(app.config.get("FLASK_SHOPPING_CART_SESSION_NAME", FLASK_SHOPPING_CART_SESSION_NAME))  # noqa
		self.allow_negative_quantity: bool = bool(app.config.get("FLASK_SHOPPING_CART_ALLOW_NEGATIVE_QUANTITY", FLASK_SHOPPING_CART_ALLOW_NEGATIVE_QUANTITY))  # noqa

	@property
	def cart(self) -> dict[str, CartItem]:
		"""
		Get the cart data.
		
		Returns:
			dict: The cart data.
		"""
		return self.get_cart()

	def get_cart(self) -> dict[str, CartItem]:
		"""
		Get the cart data.
		
		Returns:
			dict: The cart data.
		"""
		return session.get(self.session_cart_name, dict())

	def _set_cart(self, cart: dict[str, CartItem]) -> None:
		"""
		Set the cart data.
		Using the session to store the cart data, to persist across multiple uses between an instance, 
		such as add, remove or modify extra data before saving the cookie.
		
		Args:
			cart (dict): The cart data to set.
		"""
		session[self.session_cart_name] = cart