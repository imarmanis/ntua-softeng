from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import validate

from app.models import Product, ProductSchema
from app.resources.auth import requires_auth

SORT_CHOICE = ['id|ASC', 'id|DESC', 'name|ASC', 'name|DESC']
prod_schema = ProductSchema()


class ProductsResource(Resource):

    @requires_auth
    @use_args({
        'start': fields.Int(missing=1, location='query'),
        'count': fields.Int(missing=20, location='query'),
        'status': fields.Str(missing='ACTIVE', location='query'),
        'sort': fields.Str(missing='id|DESC', location='query', validate=validate.OneOf(SORT_CHOICE)),
        'format': fields.Str(location='query', validate=validate.Equal('json'))
    })
    def get(self, args):
        start = args['start']
        count = args['count']
        products = Product.query.paginate(start, count)
        # TODO : use sort arg
        # ex : .order_by(Product.id.desc())
        # + paginate error_out param
        total = products.total
        products = prod_schema.dump(products.items, many=True).data
        return {
            'start': start,
            'count': count,
            'total': total,
            'products': products
        }

    def post(self):
        raise NotImplementedError
        # db.session.add(product_object)
        # db.session.commit()

class ProductResource(Resource):
    pass
