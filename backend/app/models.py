from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from geoalchemy2 import Geometry


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


class Price(db.Model):
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id', ondelete="CASCADE"), nullable=False)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    category = db.Column(db.String(128), nullable=False)
    withdrawn = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.relationship('ProductTag', lazy='joined', backref='product',
                           passive_deletes=True, cascade="all, delete-orphan")
    prices = db.relationship('Price', lazy='joined', backref='product',
                             passive_deletes=True, cascade="all, delete-orphan")


class ProductTag(db.Model):
    __tablename__ = 'productTag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False)


class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    tags = db.relationship('ShopTag', lazy='joined', backref='shop',
                           passive_deletes=True, cascade="all, delete-orphan")
    prices = db.relationship('Price', lazy='joined', backref='shop',
                             passive_deletes=True, cascade="all, delete-orphan")
    withdrawn = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(255), nullable=False)


class ShopTag(db.Model):
    __tablename__ = 'shopTag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id', ondelete="CASCADE"), nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(32), nullable=True, default=None, unique=True)

    @property
    def password(self):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
