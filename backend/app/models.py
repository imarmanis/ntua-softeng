from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy import func
import math

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


class Price(db.Model):
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    # dateFrom = db.Column(db.Date, nullable=False)
    # dateTo = db.Column(db.Date, nullable=False)
    # doesn't make sense ??? api-specs-v2 p8 implies just date ???
    date = db.Column(db.Date, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(MEDIUMTEXT)
    category = db.Column(db.String(128), nullable=False)
    withdrawn = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.Column(MEDIUMTEXT)
    prices = db.relationship('Price', lazy='joined', backref='product')


class Shop(db.Model):
    __table__name = 'shop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lng = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)

    @hybrid_method
    def distance(self, lat, lng):
        return math.acos(math.cos(math.radians(self.lat)) * math.cos(math.radians(lat)) *
                         math.cos(math.radians(self.lng) - math.radians(lng)) +
                         math.sin(math.radians(self.lat)) * math.sin(math.radians(lat))) * 6371

    @distance.expression
    def distance(cls, lat, lng):
        return func.acos(func.cos(func.radians(cls.lat)) * func.cos(func.radians(lat)) *
                         func.cos(func.radians(lng) - func.radians(cls.lng)) +
                         func.sin(func.radians(cls.lat)) * func.sin(func.radians(lat))) * 6371

    prices = db.relationship('Price', lazy='joined', backref='shop')


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
