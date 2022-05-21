import json, logging, math

from flask import request, make_response

class Response:
	pass

class Product(object):
	id = None
	token = None
	stock = None

def _parse_int(num):
	if isinstance(num, int):
		return num
	else:
		if (isinstance(num, str)) and (num.isdigit()):
			return int(num)
		else:
			raise ValueError("Not a valid integer")

class ShoppingCart(object):
	def __init__(self, app=None, *args, **kwargs):
		if app is not None:
			self.init_app(app, *args, **kwargs)

	def init_app(self, app, **kwargs):
		with app.app_context():
			self.app = app

			self.response = {"ok": True, "status": 200, "message": "ok"}

			self.out_of_stock = make_response({"message": "product out of stock", "ok": False}, 200)
			self.not_found    = make_response({"message": "product not found", "ok": False}, 404)

			self.ignore_stock = kwargs.get("ignore_stock", False)

			app.shopping_cart = self

	def _validate_product(self, product:Product):
		if not getattr(product, "id", None):
			raise ValueError("Product has no 'id' attribute. A unique identifier is required.")
		
		if not getattr(product, "token", None):
			logging.warning("Product has no 'token' attribute. ID will be used instead.")
			product.token = str(product.id)
			# setattr(product, "token", product.id)

		if not getattr(product, "stock", None):
			logging.warning("Product has no 'stock' attribute, the stock will be ignored for the validations.")
			product.stock = math.inf
			# setattr(product, "stock", math.inf)
			self.ignore_stock = True

	@staticmethod
	def get_cart_quantity() -> int:
		"""
			Returns the total quantity of products in the cart.
		"""
		if "products" in request.cookies:
			products_list = json.loads(request.cookies.get("products"))
		
		else:
			products_list = []
		
		return sum([x["quantity"] for x in products_list])

	@staticmethod
	def get_cart() -> list:
		"""
			Returns a list of products in the cart.
			```
			[
				{
					"token": "product_token", # or "id"
					"quantity": 1
				},
				...
			]
			```
		"""
		if "products" in request.cookies:
			products_list = json.loads(request.cookies.get("products"))
		
		else:
			products_list = []
		
		return products_list


	def add(self, product:Product, quantity:int=1, ignore_stock:bool=None) -> Response:
		"""
		Adds a product to the cart.

		Params
		------
		product: Product object
		quantity: Quantity of the product to add
		ignore_stock: If True, the stock will be ignored.
		
		Returns
		-------
		Response object
		"""
		quantity = _parse_int(quantity)

		if quantity <= 0:
			raise ValueError("Quantity must be greater than zero.")

		self._validate_product(product)

		product_query = product

		if product_query:
			if ignore_stock is None:
				pass
			
			elif ignore_stock in (True, False):
				self.ignore_stock = ignore_stock
			
			else:
				raise ValueError("ignore_stock must be True or False")
			
			logging.info("Ignore stock flag set to: %s", self.ignore_stock)

			if (self.ignore_stock) or ((product_query.stock > 0) and (product_query.stock >= quantity)):
				product_token = product.token or product.id
				
				# load cart
				products_list = self.get_cart()
				
				# create product template
				product = {
					"token": product_token,
					"quantity": 0
				}

				# check if product already in cart
				for _product in products_list:
					# if product exists in cart, update template
					if _product["token"] == product_token:
						if  (self.ignore_stock) or (product_query.stock > _product["quantity"]): # check stock
							product = _product
							break
						
						else:
							return self.out_of_stock

				# update product quantity
				product["quantity"] += quantity
				
				# update cart
				if product in products_list:
					# if product exists in cart, update it
					products_list[ products_list.index(product) ] = product
				
				else:
					# if product not exists in cart, add it
					products_list.append(product)

				# update response
				response = make_response(self.response, 200)

				# creat cookie
				response.set_cookie("products", json.dumps(products_list))

				return response
			
			else:
				return self.out_of_stock
		
		else:
			return self.not_found

	def remove(self, product_token) -> Response:
		"""
		Removes a product from the cart.

		Params
		------
		product_token: Product token or id

		Returns
		-------
		Response object
		"""
		# load cart
		products_list = self.get_cart()

		# check if product exists in cart
		for product in products_list:
			if str(product["token"]) == str(product_token):
				products_list.remove(product)
				break

		# update response
		response = make_response(self.response, 200)

		# creat cookie
		response.set_cookie("products", json.dumps(products_list))

		return response

	def substract(self, product_token, quantity:int=1) -> Response:
		"""
		Substracts a quantity of a product from the cart.

		Params
		------
		product_token: Product token or id
		quantity: Quantity of the product to substract
		
		Returns
		-------
		Response object
		"""
		quantity = _parse_int(quantity)
		
		if quantity <= 0:
			raise ValueError("Quantity must be greater than zero.")

		# load cart
		products_list = self.get_cart()

		product = {
			"token": None,
			"quantity": 0
		}

		# check if product already in cart
		for _product in products_list:
			if str(_product["token"]) == str(product_token):
				product = _product
				break

		product["quantity"] -= quantity

		if product in products_list:
			products_list[ products_list.index(product) ] = product

		else:
			raise ValueError("Product not found in cart.")

		# update response
		response = make_response(self.response, 200)

		# creat cookie
		response.set_cookie("products", json.dumps(products_list))

		return response

	def clear(self) -> Response:
		"""
		Clears the cart.
		
		Returns
		-------
		Response object
		"""
		# update response
		response = make_response(self.response, 200)

		# creat cookie
		response.set_cookie("products", json.dumps([]))

		return response




