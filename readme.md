# Flask-Shoppingcart

Este proyecto es una librería para el framework [Flask](https://flask.palletsprojects.com/en/2.1.x/) para poder trabajar con un carrito de compras a nivel de cookies.

La idea es poder almacenar los datos de un carrito de compras a un nivel basico para proyectos de tiendas online simples.

## Instalación

Clonar el proyecto como normalmente clonas un proyecto de github.

```
$ git clone https://github.com/Brixt18/flask-shoppingcart
```
O descargando el archivo .zip del mismo.

## Requisitos

 * [Python >= 3.7](https://www.python.org/downloads/release/python-370/)
 * [Flask](https://flask.palletsprojects.com/en/2.1.x/)


## Cómo Usar

### Inicializar
- para aplicaciones simples:
```
from flask import Flask
app = Flask(__name__)

shopping_cart = ShoppingCart(app=app)

if __name__ == "__main__":
    app.run(debug=True)
```

- Para aplicaciones un poco más complejas:
```
from flask import Flask
app = Flask(__name__)

shopping_cart = ShoppingCart()

def create_app():
	shopping_cart.init_app(app)

    return app
```

### Usos Basicos
- Añadir un producto

Para añadir un producto es necesario una instancia del producto a añadir para poder controlar los atributos basicos, como el ID (o token) y el Stock.

```
class MyProduct:
    name = "My Product"
    id = "abcd"
    stock = 19

@app.route("/add/<product_id>/")
def add(product_id):
    product = MyProduct()
    resp = shopping_cart.add(product=product, quantity=2)

    return resp
```

En el caso de estar trabajando con [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), se puede tener una clase `Product` y usarla igualmente.

```
from app import db # db = SQLAlchemy(app)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	token = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)

	@staticmethod
	def get_by_id(id):
		return Product.query.filter_by(id=id).first()

@app.route("/add/<product_id>/")
def add(product_id):
    product = Product.get_by_id(product_id)
    resp = shopping_cart.add(product=product, quantity=2)

    return resp        
```

- Remover un producto
```
@app.route("/remove/<product_id>/")
def add(product_id):
    product_id = MyProduct().id
    resp = shopping_cart.remove(product_id)

    return resp
```

- Remover una cantidad especifica
```
@app.route("/substract/<product_id>/<quantity>/")
def add(product_id, quantity):
    product_id = MyProduct().id
    resp = shopping_cart.substract(product_id, quantity)

    return resp
```

## Configuraciones

Por defecto, la libreria retorna un json OK, a travez de un `make_response`
```
{
    "ok": True,
    "status": 200, 
    "message": "ok"
}
```
pero es posible personalizar este response utilizando:
```
shopping_cart.response = MyResponse
```
donde `MyResponse` puede ser un `url_for`, `redirect` u otro.

- Ejemplo:
```
from flask import redirect, url_for

@app.route("/")
def index():
    return "Index Page"

@app.route("/add/<product_id>/")
def add(product_id):
    product = MyProduct()

    shopping_cart.response = redirect( url_for( "index" ) )
    resp = shopping_cart.add(product, quantity=2)

    return resp  
```
De esta manera, se almacenaran los productos en cookie y el retorno será una redirección hacia `index`.

## Trabajando con AJAX
Gracias a que estamos utilizando `make_response`, es posible trabajar con [AJAX](https://es.wikipedia.org/wiki/AJAX) o [Fetch](https://developer.mozilla.org/es/docs/Web/API/Fetch_API/Using_Fetch) sin problemas.

- Ejemplo:

### En la Ruta:
```
@app.route("/add/<product_token>", methods=["POST"])
def add(product_token=None):
    product = Product.get_by_token(product_token)
    
    resp = shopping_cart.add(product, quantity=quantity)
    
    return resp
```

### En AJAX:
- Utilizando JQuery AJAX, aunque se aplica igualmente para Fetch
```
$.ajax({
    url: '/add/'+product_token,
    method: 'POST',
    contentType: "application/json",
    data: JSON.stringify({"quantity": 10}),
})
.always( function(resp){ 
    console.log(resp)
})
```
