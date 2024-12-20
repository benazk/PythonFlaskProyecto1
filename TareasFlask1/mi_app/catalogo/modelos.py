from mi_app import db

class Product(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category', backref=db.backref('products', lazy='dynamic')
    )
    """
    lazy='dynamic' -> devuelve un objeto de tipo consulta dinámica (un objeto Query).
    Esto te permite construir consultas adicionales sobre esa relación sin cargar 
    los datos inmediatamente desde la base de datos.
    Al crear la relación, estamos creando:
    - Un atributo (de relación) category en la clase Product que permite acceder a la categoría a la que pertenece un producto.
      product.category devuelve un objeto de clase Category (siendo product un objeto de clase Product).
    - Un atributo (de relación) products en la clase Category, que devuelve una consulta 
      SQLAlchemy que representa todos los productos relacionados con una categoría específica.
    - En 'products_list = category.products.all()':
        category.products:
            Con lazy='dynamic', el atributo products devuelve un objeto de tipo Query, que representa una consulta diferida.
            Aún no se ejecuta la consulta SQL, por lo que no se recuperan datos de la base de datos en este punto.
        .all():
            Este método ejecuta la consulta asociada al objeto Query y recupera todos los resultados coincidentes.
            Los resultados se devuelven como una lista de objetos del modelo relacionado (Product en este caso).      

    """
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    def __repr__(self):
        return f'<Product {self.id}>'

class Category(db.Model):
    # __tablename__ = 'category'  es el nombre que le da flask por defecto a la tabla de la BD
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Category {self.id}>'

