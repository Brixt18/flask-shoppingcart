from typing import TypedDict

from .utils import Number

#* We could use NotRequired from typing, but it is only available in Python 3.11+
#* -> https://peps.python.org/pep-0655/ <-
#* So, as we're tring to add support for this library to Python 3.9+, we will use this approach

class _OptionalFields(TypedDict, total=False):
    extra: dict

class CartItem(_OptionalFields):
    quantity: Number
