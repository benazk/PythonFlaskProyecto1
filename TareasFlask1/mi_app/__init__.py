from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from  mi_app.catalogo.vistas import catalog
# si se pone aquí da un problema de importación circular
# ImportError: cannot import name 'db' from partially 
# #initialized module 'mi_app' (most likely due to a circular 
# import). Normal, en vistas se hace import db, todavía no creado.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://benat:12345678@localhost:5432/eval2'
db = SQLAlchemy(app)
from  mi_app.catalogo.vistas import catalog
app.register_blueprint(catalog)
with app.app_context():
    db.create_all()