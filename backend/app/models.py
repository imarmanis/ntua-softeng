from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.mysql import MEDIUMTEXT

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(MEDIUMTEXT)
    category = db.Column(db.String(128), nullable=False)
    withdrawn = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.Column(MEDIUMTEXT)


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
