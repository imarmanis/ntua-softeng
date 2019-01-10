from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import validate

from app.models import db, ma, Product
from app.resources.auth import requires_auth

class ProductSchema(ma.ModelSchema):
    # TODO: set which fields are to be serialized
    class Meta:
        model = Product

bad_request = '', 400
prod_schema = ProductSchema()


class ProductsResource(Resource):
    _STATUS_CHOICE = ['ALL', 'WITHDRAWN', 'ACTIVE']
    _SORT_CHOICE = ['id|ASC', 'id|DESC', 'name|ASC', 'name|DESC']

    @use_args({
        'start': fields.Int(missing=0, location='query', validate=validate.Range(min=0)),
        'count': fields.Int(missing=20, location='query', validate=validate.Range(min=1)),
        'status': fields.Str(missing='ACTIVE', location='query',
                             validate=validate.OneOf(_STATUS_CHOICE)),
        'sort': fields.Str(missing='id|DESC', location='query',
                           validate=validate.OneOf(_SORT_CHOICE)),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, args, **_kwargs):
        start = args['start'] + 1   # Pagination is 1-indexed
        count = args['count']
        status = args['status']
        sort = {
            'id|ASC': Product.id.asc(),
            'id|DESC': Product.id.desc(),
            'name|ASC': Product.name.asc(),
            'name|DESC': Product.name.desc()
        }[args['sort']]
        products = Product.query.filter_by(withdrawn=status).order_by(sort). \
                paginate(start, count, False)  # don't return 404 if there are no products

        return {
            'start': products.page - 1,
            'count': products.items,
            'total': products.total,
            'products': prod_schema.dump(products.items, many=True).data
        }

    @requires_auth
    @use_args({
        'name': fields.Str(location='json', required=True),
        'description': fields.Str(location='json', required=True),
        'category': fields.Str(location='json', required=True),
        'tags': fields.List(fields.Str(), location='json', required=True),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def post(self, args, **_kwargs):
        del args['format']  # don't pass format to Product's constructor
        product = Product(**{**args, 'withdrawn': False})
        db.session.add(product)
        db.session.commit()

        return prod_schema.dump(product).data

class ProductResource(Resource):
    @use_args({
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, prod_id, **_kwargs):
        product = Product.query.get_or_404(prod_id)

        return prod_schema.dump(product).data

    @requires_auth
    @use_args({
        'name': fields.Str(location='json', required=True),
        'description': fields.Str(location='json', required=True),
        'category': fields.Str(location='json', required=True),
        'tags': fields.List(fields.Str(), location='json', required=True),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def put(self, prod_id, args, **_kwargs):
        product = Product.query.get_or_404(prod_id)
        product.name = args['name']
        product.description = args['description']
        product.category = args['category']
        product.tags = args['tags']
        db.session.commit()

        return prod_schema.dump(product).data

    @requires_auth
    @use_args({
        'name': fields.Str(location='json'),
        'description': fields.Str(location='json'),
        'category': fields.Str(location='json'),
        'tags': fields.List(fields.Str(), location='json'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def patch(self, prod_id, args, **_kwargs):
        if len(args) != 2:
            # Only one of name, description, category and tags should be specified
            return bad_request
        del args['format']
        changed = next(iter(args.keys()))
        product = Product.query.get_or_404(prod_id)
        setattr(product, changed, args[changed])
        db.session.commit()

        return prod_schema.dump(product).data

    @requires_auth
    @use_args({
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def delete(self, prod_id, is_admin, **_kwargs):
        product = Product.query.get_or_404(prod_id)

        if is_admin:
            db.session.delete(product)
        else:
            product.withdrawn = True

        db.session.commit()
        return {'message': 'OK'}
