from flask  import request, jsonify, Blueprint, render_template
from mi_app import db
from mi_app.catalogo.modelos import Product, Category

catalog = Blueprint('catalog',__name__)

@catalog.route('/')
def home():
    return render_template("index.html")

@catalog.route('/productos-form')
def form():
    return render_template("anadir.html")

@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return f"Producto: {product.name}; {product.price}€."


@catalog.route('/products')
def products():
    products = Product.query.all()
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': str(product.price),
            'category': product.category.name
        }
    return jsonify(res)

@catalog.route('/product-create', methods=['POST'])
def create_product():
    
    name = request.args.get('name')
    price = request.args.get('price')
    #price = request.form.get('price') #form -> Postman: en la pestaña Body, selecciona x-www-form-urlencoded    
    categName = request.args.get('category')
    category = Category.query.filter_by(name=categName).first() #first devuelve un objeto, no una lista de un solo objeto.
    if not category:
        category = Category(categName)
    product = Product(name,price,category)
    print(f"categoría del producto: {product.category.name}")    

    """
    Aquí, la relación en SQLAlchemy funciona así:
    - Cuando pasas un objeto de clase Category al constructor de Product, lo que realmente haces es asignar 
      el objeto al atributo category de la instancia de Product
    - SQLAlchemy automáticamente gestionará los valores de las claves foráneas, vinculando el 
      category.id (clave primaria de Category) al category_id (clave foránea en Product).

    - En cuanto asocias esta nueva categoría a un producto, y luego haces db.session.add(product) seguido de db.session.commit(),
      SQLAlchemy detectará que también debe insertar la nueva categoría en la base de datos. 
      Esto sucede porque SQLAlchemy rastrea todos los objetos que están vinculados.
    
    Si no ponemos la relación, debemos crear la cateogoría a mano y después
    el producto (y modificar su constructor):
    '
    class Product(db.Model):    
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255))
        price = db.Column(db.Float)
        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id
    '
    # Crear una nueva categoría
    category = Category(name="Furniture")
    db.session.add(category)
    db.session.commit()

    # Crear un producto asociado a la nueva categoría
    product = Product(name="Table", price=200.00, category_id=category.id)
    db.session.add(product)
    db.session.commit()

    En este caso, a pesar de que no hemos creado la relación, la clave foránea
    sigue asegurando la integridad referencial, lo que significa que:
    - El valor de category_id en la tabla Product debe coincidir con un valor existente en la columna id de la tabla Category.
    - Esto evita inconsistencias, como asignar un category_id que no corresponde a ninguna categoría válida.
    - Se garantiza que category_id apunta a una categoría válida.
    """

    db.session.add(product)
    db.session.commit()
    print(f"primer producto de la categoría: {product.category.products.first().name}")
    return 'producto creado.'
