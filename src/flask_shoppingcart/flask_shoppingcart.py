from functools import partial
from numbers import Number
from typing import Optional, Union

from .exceptions import OutOfStokError, ProductNotFoundError
from .models import CartItem
from ._shoppingcart import ShoppingCartBase


class FlaskShoppingCart(ShoppingCartBase):
	@property
	def cart(self) -> dict[str, CartItem]:
		"""
		Get the cart data.
		
		Returns:
			dict: The cart data.
		"""
		return self.get_cart()

	def _validate_stock(self, current_stock: Optional[Number], quantity_to_add: Number, current_quantity: Number) -> None:
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
		if (
			(current_stock is not None)
			and ((current_quantity + quantity_to_add) > current_stock)
		):
			raise OutOfStokError()

	def get_cart(self) -> dict[str, CartItem]:
		"""
		Get the cart data.
		
		Returns:
			dict: The cart data.
		"""
		return self._get_cart()

	def add(self,
         product_id: str,
         quantity: Number = 1,
         overwrite_quantity: bool = False,
         current_stock: Optional[Number] = None,
         extra: Optional[dict] = None,
         allow_negative: Optional[bool] = None
         ) -> None:
		"""
		Add a product to the cart or update the quantity of an existing product.
		
		Args:
			product_id (str): The ID of the product to add.
			quantity (Number): The quantity of the product to add.
			overwrite_quantity (bool): If True, the quantity will be overwritten instead of added.
			current_stock (Number, optional): The current stock of the product. If set, the stock will be validated.
			extra (dict, optional): Extra data to store in the product.
			allow_negative (bool, optional): If True, the quantity can be negative.

		Raises:
			OutOfStokError: If the product is out of stock. This error is raise if the ignore_stock is True and the quantity exceeds the current stock.
		"""
		cart: dict[str, CartItem] = self._get_cart()

		_allow_negative = allow_negative or self.allow_negative_quantity

		if not _allow_negative and quantity <= 0:
			raise ValueError("Quantity must be greater than 0.")

		product: Optional[CartItem] = cart.get(product_id, None)

		_data:CartItem = {
			"quantity": quantity,
		}

		_validate_stock: partial = partial(
			self._validate_stock, current_stock, quantity)

		if product:
			_validate_stock(product["quantity"])

			if overwrite_quantity:
				product.update(_data)

			else:
				product["quantity"] += quantity

		else:
			product = _data
			_validate_stock(0)

		if extra:
			if not isinstance(extra, dict):
				raise TypeError("Extra data must be a dictionary.")
			
			if product.get("extra"):
				product["extra"].update(extra)
			
			else:
				product["extra"] = extra

		cart[product_id] = product

		self._set_cart(cart)

	def remove(self, product_id: str) -> None:
		"""
		Removes a product from the cart.
		
		Args:
			product_id (str): The ID of the product to remove.
		"""
		cart = self._get_cart()

		if product_id in cart:
			cart.pop(product_id)
			self._set_cart(cart)

	def clear(self) -> None:
		"""
		Clears the cart.
		"""
		self._set_cart(dict())

	def subtract(self, product_id: str, quantity: Number = 1, allow_negative: bool = False) -> None:
		"""
		Substracts a quantity from a product in the cart.
		
		Args:
			product_id (str): The ID of the product to substract from.
			quantity (Number): The quantity to substract.
			allow_negative (bool): If True, the quantity can be negative.
		"""
		cart = self._get_cart()

		_allow_negative = allow_negative or self.allow_negative_quantity

		if product_id in cart:
			product = cart[product_id]			
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

			self._set_cart(cart)

	def get_product(self, product_id: str) -> CartItem:
		"""
		Retrieve a product from the shopping cart by its product ID.
		
		Args:
			product_id (str): The unique identifier of the product to retrieve.
		
		Returns:
			dict: A dictionary containing the product details.
		
		Raises:
			ProductNotFoundError: If the product with the given ID is not found in the cart.
		"""
		product = self._get_cart().get(product_id, None)

		if product is None:
			raise ProductNotFoundError()
		
		return product

	def get_product_or_none(self, product_id: str) -> Union[CartItem, None]:
		"""
		Get a product from the cart.
		
		Args:
			product_id (str): The ID of the product to get.
		
		Returns:
			dict: The product data.
		"""
		return self._get_cart().get(product_id, None)
