from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_args
import marshmallow
from marshmallow import post_dump
from sqlalchemy.exc import IntegrityError
from app.models import db, ma, Product, ProductTag
from app.resources.auth import requires_auth
from app.resources.utils import unique_stripped, custom_error, ErrorCode


class ProductTagSchema(ma.ModelSchema):
    # This is necessary because we require tags to be a list of names (strings),
    # but by default it would be a list of {'name': <name>} dicts
    @post_dump
    def flatten(self, data):
        return data['name']

    class Meta:
        model = ProductTag
        # Fields to be included in the output
        fields = ('name', )


class ProductSchema(ma.ModelSchema):
    # Override tags field to use a nested representation rather than keys
    tags = marshmallow.fields.Nested(ProductTagSchema, many=True)

    class Meta:
        model = Product
        # Fields to be included in the output
        fields = ('id', 'name', 'description', 'category', 'tags', 'withdrawn')


prod_schema = ProductSchema()


class ProductsResource(Resource):
    _STATUS_CHOICE = ['ALL', 'WITHDRAWN', 'ACTIVE']
    _SORT_CHOICE = ['id|ASC', 'id|DESC', 'name|ASC', 'name|DESC']

    @use_args({
        'start': fields.Int(missing=0, location='query', validate=validate.Range(min=0)),
        'count': fields.Int(missing=20, location='query', validate=validate.Range(min=0)),
        'status': fields.Str(missing='ACTIVE', location='query',
                             validate=validate.OneOf(_STATUS_CHOICE)),
        'sort': fields.Str(missing='id|DESC', location='query',
                           validate=validate.OneOf(_SORT_CHOICE)),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, args, **_kwargs):
        start = args['start']
        count = args['count']
        status = args['status']
        sort = {
            'id|ASC': Product.id.asc(),
            'id|DESC': Product.id.desc(),
            'name|ASC': Product.name.asc(),
            'name|DESC': Product.name.desc()
        }[args['sort']]
        query = Product.query
        if status != 'ALL':
            query = query.filter_by(withdrawn=(status == 'WITHDRAWN'))
        total = query.count()
        products = query.order_by(sort).offset(start).limit(count).all()

        return {
            'start': start,  # rows skipped due to offset
            'count': len(products),
            'total': total,
            'products': prod_schema.dump(products, many=True).data
        }

    @requires_auth
    @use_args({
        'name': fields.Str(location='form', required=True),
        'description': fields.Str(location='form', required=True),
        'category': fields.Str(location='form', required=True),
        'tags': fields.List(fields.Str(), location='form', required=True),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def post(self, args, **_kwargs):
        product = Product(name=args['name'], description=args['description'],
                          category=args['category'], withdrawn=False)
        product.tags = [ProductTag(name=tag, product=product) for tag in
                        unique_stripped(args['tags'])]
        db.session.add(product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return custom_error('tags', ['Duplicate tags']), ErrorCode.BAD_REQUEST  # we should never get here

        return prod_schema.dump(product).data


class ProductResource(Resource):
    @use_args({
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, _args, prod_id):
        product = Product.query.get_or_404(prod_id)

        return prod_schema.dump(product).data

    @requires_auth
    @use_args({
        'name': fields.Str(location='form', required=True),
        'description': fields.Str(location='form', required=True),
        'category': fields.Str(location='form', required=True),
        'tags': fields.List(fields.Str(), location='form', required=True),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def put(self, args, prod_id, **_kwargs):
        product = Product.query.get_or_404(prod_id)
        product.name = args['name']
        product.description = args['description']
        product.category = args['category']
        for tag in product.tags:
            db.session.delete(tag)  # delete old product tags
        db.session.flush()
        # flush delete's to db to ensure delete stmts precedes insert stmt and avoid integrity error
        product.tags = [ProductTag(name=tag, product=product) for tag in
                        unique_stripped(args['tags'])]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return custom_error('tags', ['Duplicate tags']), ErrorCode.BAD_REQUEST  # we should never get here

        return prod_schema.dump(product).data

    @requires_auth
    @use_args({
        'name': fields.Str(location='form'),
        'description': fields.Str(location='form'),
        'category': fields.Str(location='form'),
        'tags': fields.List(fields.Str(), location='form'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def patch(self, args, prod_id, **_kwargs):
        del args['format']
        if len(args) != 1:
            return custom_error('patch', ['Specify exactly one of: name, description, category or tags']),\
                   ErrorCode.BAD_REQUEST

        product = Product.query.get_or_404(prod_id)
        changed = next(iter(args.keys()))
        if changed == 'tags':
            for tag in product.tags:
                db.session.delete(tag)  # delete old product tags
            db.session.flush()
            product.tags = [ProductTag(name=tag, product=product) for tag in
                            unique_stripped(args['tags'])]
        else:
            setattr(product, changed, args[changed])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            custom_error('tags', ['Duplicate tags']), ErrorCode.BAD_REQUEST  # we should never get here

        return prod_schema.dump(product).data

    @requires_auth
    @use_args({
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def delete(self, _args, prod_id, is_admin, **_kwargs):
        product = Product.query.get_or_404(prod_id)

        if is_admin:
            db.session.delete(product)
        else:
            product.withdrawn = True

        db.session.commit()

        return {'message': 'OK'}
