import itertools
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_args
from marshmallow.decorators import post_dump, pre_dump
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import lazyload
from app.models import Shop, ShopTag, db, ma
from app.resources.auth import requires_auth
from app.resources.utils import unique_stripped, custom_error, ErrorCode


SORT_CHOICE = list(map('|'.join, itertools.product(['name', 'id'],
                                                   ['ASC', 'DESC'])))
STATUS_CHOICE = ['ALL', 'WITHDRAWN', 'ACTIVE']


class ShopTagSchema(ma.ModelSchema):
    @post_dump
    def flatten(self, data):
        return data['name']

    class Meta:
        model = ShopTag
        fields = ('name',)


class ShopSchema(ma.ModelSchema):
    tags = fields.Nested(ShopTagSchema, many=True)
    lng = fields.Float()
    lat = fields.Float()

    class Meta:
        model = Shop
        fields = ('id', 'name', 'tags', 'lat', 'lng', 'address', 'withdrawn')

    @pre_dump
    def position_to_xy(self, data):
        point = to_shape(data.position)
        data.lng, data.lat = point.x, point.y
        return data


shop_schema = ShopSchema()


class ShopDistSchema(ma.ModelSchema):
    lng = fields.Float()
    lat = fields.Float()
    dist = fields.Float()

    class Meta:
        model = Shop
        fields = ('id', 'name', 'lat', 'lng', 'address', 'dist')

    @pre_dump
    def flatten(self, data):
        ret = data[0]
        ret.position = data[1]
        ret.dist = data[2]
        return ret

    @pre_dump
    def position_to_xy(self, data):
        point = to_shape(data.position)
        data.lng, data.lat = point.x, point.y
        return data


class ShopsDistResource(Resource):
    @use_args({
        'count': fields.Int(missing=20, location='query', validate=validate.Range(min=0)),
        'dist': fields.Float(required=True, location='query', validate=validate.Range(min=0)),
        'lng': fields.Float(required=True, location='query'),
        'lat': fields.Float(required=True, location='query')
    })
    def get(self, args):
        dist = func.ST_Distance(Shop.position, from_shape(Point(args['lng'], args['lat']), srid=4326), True). \
            label('dist')
        query = db.session.query(Shop, Shop.position, dist).options(lazyload('prices'), lazyload('tags')).\
            order_by(dist.asc()).limit(args['count'])
        shops = query.all()
        return ShopDistSchema().dump(shops, many=True).data


class ShopsResource(Resource):
    @use_args({
        'start': fields.Int(missing=0, location='query', validate=validate.Range(min=0)),
        'count': fields.Int(missing=20, location='query', validate=validate.Range(min=0)),
        'sort': fields.List(
            fields.Str(validate=validate.OneOf(SORT_CHOICE)), missing=['id|DESC'], location='query'
            # default sort order not explicitly specified, maybe same as products?
        ),
        'status': fields.Str(missing='ACTIVE', location='query',
                             validate=validate.OneOf(STATUS_CHOICE)),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, args):
        query = Shop.query
        start = args['start']
        count = args['count']
        status = args['status']
        sorts = [x.split('|') for x in args['sort']]

        def to_sort_operator(field, order):
            sort_field = {
                'id': Shop.id,
                'name': Shop.name
            }[field]

            sort_order = {
                'ASC': asc,
                'DESC': desc
            }[order]

            return sort_order(sort_field)

        if status != 'ALL':
            query = query.filter_by(withdrawn=(status == 'WITHDRAWN'))
        query = query.order_by(
            *[to_sort_operator(field, order) for field, order in sorts]
        )
        total = query.count()
        shops_page = query.offset(start).limit(count).all()
        shops = shop_schema.dump(shops_page, many=True).data
        return {
            'start': start,
            'count': count,
            'total': total,
            'shops': shops
        }

    @requires_auth
    @use_args({
        'name': fields.Str(required=True, location='form'),
        'address': fields.Str(required=True, location='form'),
        'lng': fields.Float(required=True, location='form'),
        'lat': fields.Float(required=True, location='form'),
        'tags': fields.List(fields.String(), required=True, location='form'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def post(self, args, **_kwargs):
        position = from_shape(Point(args['lng'], args['lat']), srid=4326)
        new_shop = Shop(name=args['name'], address=args['address'], position=position,
                        withdrawn=False)
        new_shop.tags = [ShopTag(name=tag, shop=new_shop) for tag in unique_stripped(args['tags'])]
        db.session.add(new_shop)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "shop_pna_c" in e.orig:
                return custom_error('Address/Position/Name', ['Same address, position and name with existing shop']), \
                       ErrorCode.BAD_REQUEST
            else:
                return custom_error('tags', ['Duplicate tags']), ErrorCode.BAD_REQUEST  # we should never get here
        return shop_schema.dump(new_shop).data


class ShopResource(Resource):
    @use_args({
        'format': fields.Str(location='query', validate=validate.Equal('json'))
    })
    def get(self, _args, shop_id):
        shop = Shop.query.get_or_404(shop_id)
        return shop_schema.dump(shop).data

    @requires_auth
    @use_args({
        'name': fields.Str(required=True, location='form'),
        'address': fields.Str(required=True, location='form'),
        'lng': fields.Float(required=True, location='form'),
        'lat': fields.Float(required=True, location='form'),
        'tags': fields.List(fields.Str(), required=True, location='form'),
        'format': fields.Str(location='query', validate=validate.Equal('json'))
    })
    def put(self, args, shop_id, **_kwargs):
        shop = Shop.query.get_or_404(shop_id)
        shop.name = args['name']
        shop.address = args['address']
        shop.position = from_shape(Point(args['lng'], args['lat']), srid=4326)
        for tag in shop.tags:
            db.session.delete(tag)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            return custom_error('Address/Position/Name', ['Same address, position and name with existing shop']), \
                   ErrorCode.BAD_REQUEST
        # flush delete's to db to ensure delete stmts precede insert stmt and avoid integrity error
        shop.tags = [ShopTag(name=tag, shop=shop) for tag in unique_stripped(args['tags'])]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return custom_error('tags', ['Duplicate tags']), ErrorCode.BAD_REQUEST  # we should never get here
        return shop_schema.dump(shop).data

    @requires_auth
    @use_args({
        'name': fields.Str(location='form'),
        'address': fields.Str(location='form'),
        'lng': fields.Float(location='form'),
        'lat': fields.Float(location='form'),
        'tags': fields.List(fields.Str(), location='form'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def patch(self, args, shop_id, **_kwargs):
        del args['format']
        if len(args) != 1:
            return custom_error('patch', ['Specify exactly one of: name, address, lng, lat, tags']), \
                   ErrorCode.BAD_REQUEST
        shop = Shop.query.get_or_404(shop_id)
        changed = next(iter(args.keys()))
        if changed == 'tags':
            for tag in shop.tags:
                db.session.delete(tag)
            db.session.flush()
            shop.tags = [ShopTag(name=tag, shop=shop) for tag in unique_stripped(args['tags'])]
        elif changed == 'lat':
            old = to_shape(shop.position)
            shop.position = from_shape(Point(old.x, args['lat']), srid=4326)
        elif changed == 'lng':
            old = to_shape(shop.position)
            shop.position = from_shape(Point(args['lng'], old.y), srid=4326)
        else:
            setattr(shop, changed, args[changed])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if changed == 'tags':
                return custom_error('tags', ['Duplicate tags']), ErrorCode.BAD_REQUEST  # we should never get here
            else:
                return custom_error('Address/Position/Name', ['Same address, position and name with existing shop']), \
                       ErrorCode.BAD_REQUEST

        return ShopSchema().dump(shop).data

    @requires_auth
    @use_args({
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def delete(self, _args, shop_id, is_admin, **_kwargs):
        shop = Shop.query.get(shop_id)
        if not shop:
            return custom_error('shop', ['Invalid shop id']), ErrorCode.NOT_FOUND
        if is_admin:
            db.session.delete(shop)
        else:
            shop.withdrawn = True
        db.session.commit()
        return {'message': 'OK'}
