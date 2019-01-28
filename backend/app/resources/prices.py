import itertools
from datetime import date, timedelta
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import validate
from marshmallow.decorators import post_dump, pre_dump
from app.models import Product, Shop, Price, db, ma, ProductTag, ShopTag
from sqlalchemy import asc, desc, func, or_
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


SORT_CHOICE = list(map('|'.join, itertools.product(['geoDist', 'price', 'date'],
                                                   ['ASC', 'DESC'])))

bad_request = '', 400


class PricesResource(Resource):
    class PriceSchema(ma.ModelSchema):
        class ProductSchema(ma.ModelSchema):
            class ProductTagSchema(ma.ModelSchema):
                name = fields.String()

                @post_dump
                def flatten(self, data):
                    return data['name']

            productId = fields.Int(attribute="id")
            productName = fields.String(attribute="name")
            productTags = fields.Nested(ProductTagSchema, many=True, attribute='tags')

        class ShopSchema(ma.ModelSchema):
            class ShopTagSchema(ma.ModelSchema):
                name = fields.String()

                @post_dump
                def flatten(self, data):
                    return data['name']

            shopId = fields.Int(attribute='id')
            shopName = fields.Str(attribute='name')
            shopTags = fields.Nested(ShopTagSchema, many=True, attribute='tags')
            shopAddress = fields.Str(attribute='address')

        price = fields.Float()
        date = fields.Date()
        product = fields.Nested(ProductSchema)
        shop = fields.Nested(ShopSchema)
        shopDist = fields.Float(attribute='dist')

        @pre_dump
        def handle_tuple(self, data):
            # if with_geo: query result = list of tuple(product, distance)
            if not isinstance(data, tuple):
                return data
            data[0].dist = data[1]
            return data[0]

        @post_dump
        def refactor(self, data):
            # flatten shop, product entries of data dict
            t_shop = data['shop']
            t_prod = data['product']
            del data['shop']
            del data['product']
            data.update(t_shop)
            data.update(t_prod)
            return data

    @use_args({
        'start': fields.Int(missing=0, location='query', validate=validate.Range(min=0)),
        'count': fields.Int(missing=20, location='query', validate=validate.Range(min=0)),  # zero count is ok ?
        'geoDist': fields.Float(missing=None, location='query'),
        'geoLng': fields.Float(missing=None, location='query'),
        'geoLat': fields.Float(missing=None, location='query'),
        'dateFrom': fields.Date(missing=None, location='query'),
        'dateTo': fields.Date(missing=None, location='query'),
        'sort': fields.Str(missing='price|ASC', location='query',
                           many=True, validate=validate.OneOf(SORT_CHOICE)),
        'shops': fields.List(fields.Int(), missing=None, location='query'),
        'products': fields.List(fields.Int(), missing=None, location='query'),
        'tags': fields.List(fields.Str(), missing=None, location='query'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, args):
        shop_ids = args['shops']
        product_ids = args['products']
        tags = args['tags']

        with_geo = args['geoDist'] is not None and args['geoLng'] is not None and args['geoLat'] is not None
        no_geo = args['geoDist'] is None and args['geoLng'] is None and args['geoLat'] is None
        if not (with_geo or no_geo):
            return bad_request

        with_date = (args['dateFrom'] is not None and args['dateTo'] is not None) and \
                    (args['dateFrom'] <= args['dateTo'])
        no_date = args['dateFrom'] is None and args['dateTo'] is None
        if not (with_date or no_date):
            return bad_request

        sort = args['sort'].split('|')
        if (sort[0] == 'geoDist' and no_geo) or (sort[0] == 'date' and no_date):
            return bad_request

        # extra validation, some combinations are illegal

        dist_col = None
        if with_geo:
            dist = func.ST_Distance(Shop.position, from_shape(Point(args['geoLng'], args['geoLat']), srid=4326), True).\
                label('dist')
            query = db.session.query(Price, dist)
        else:
            query = Price.query

        query = query.join(Price.product, Price.shop)
        today = date.today()
        date_from = args['dateFrom'] if args['dateFrom'] else today
        date_to = args['dateTo'] if args['dateTo'] else today
        query = query.filter(Price.date.between(date_from, date_to))

        if shop_ids:
            query = query.filter(Shop.id.in_(shop_ids))
        if product_ids:
            query = query.filter(Product.id.in_(product_ids))

        if tags:
            query = query.filter(or_(Product.tags.any(func.lower(ProductTag.name).in_(map(str.lower, tags))),
                                 Shop.tags.any(func.lower(ShopTag.name).in_(map(str.lower, tags)))))

        if with_geo:
            subq = query.subquery()
            dist_col = subq.c.dist
            query = db.session.query(Price, dist_col).select_entity_from(subq).filter(dist_col < args['geoDist'])
            # nested query to avoid recalculating distance expr
            # WHERE and HAVING clauses can't refer to column names (dist)

        sort_field = {
            'geoDist': dist_col,
            'price': Price.price,
            'date': Price.date
        }[sort[0]]

        sort_order = {
            'ASC': asc,
            'DESC': desc
        }[sort[1]]

        query = query.order_by(sort_order(sort_field))

        start = args['start']
        count = args['count']
        prices_page = query.paginate(start + 1, count, False)
        prices = PricesResource.PriceSchema(many=True).dump(prices_page.items).data
        return {
            'start': start,
            'count': count,
            'total': prices_page.total,
            'prices': prices
        }

    @use_args({
        'price': fields.Float(required=True, location='form'),
        'dateFrom': fields.Date(required=True, location='form'),
        'dateTo': fields.Date(required=True, location='form'),
        'productId': fields.Int(required=True, attribute='product_id', location='form'),
        'shopId': fields.Int(required=True, attribute='shop_id', location='form'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def post(self, args):
        date1 = args['dateFrom']
        date2 = args['dateTo']
        if not (date1 <= date2):
            return bad_request

        shop = Shop.query.filter_by(id=args['shop_id']).first()
        product = Product.query.filter_by(id=args['product_id']).first()
        if not (shop and product):
            return bad_request
        del args['format']
        del args['dateFrom']
        del args['dateTo']

        new_prices = [Price(**args, date=d) for d in
                      [date1 + timedelta(days=x) for x in range((date2-date1).days + 1)]]
        db.session.add_all(new_prices)
        db.session.commit()
        # TODO
        # UniqueConstraint on (shop_id, product_id, date) necessary ?
        # Maybe use '~ INSERT [] ON DUPLICATE KEY UPDATE' dbms specific statement
        return PricesResource.PriceSchema(many=True).dump(new_prices).data
