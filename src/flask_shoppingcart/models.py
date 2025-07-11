from numbers import Number
from typing import TypedDict

class _CartITem(TypedDict):
    extra: dict

class CartItem(_CartITem, total=False):
    quantity: Number
