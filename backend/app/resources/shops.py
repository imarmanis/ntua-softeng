import itertools
from datetime import date
from flask_restful import Resource
from flask import request
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import validate, ValidationError
from marshmallow.decorators import post_dump, pre_dump
from app.models import Product, Shop, Price, db, ma
from sqlalchemy import asc, desc

SORT_CHOICE = list(map('|'.join, itertools.product(['geoDist', 'price', 'date'],
                                                   ['ASC', 'DESC'])))

ids_field = fields.List(fields.Int())
bad_request = '', 400
not_found = '', 404


class ShopsResource(Resource):
    class ShopSchema(ma.ModelSchema):
        name = fields.String()
    
    @use_args({
        'start': fields.Int(missing=1, location='json'),
        'count': fields.Int(missing=20, location='json'),
        'sort': fields.Str(missing='price|ASC', location='json',
                           many=True, validate=validate.OneOf(SORT_CHOICE)),
        'format': fields.Str(location='query', validate=validate.Equal('json'))
    })
    def get(self, args):
        #sort = args['sort'].split('|')
        query = db.session.query(Shop.name)
        #sort_order = 'ASC'
        #query = query.order_by(sort_order)
        start = args['start']
        count = args['count']
        shops_page = query.paginate(start, count)
        shops = ShopsResource.ShopSchema(many=True).dump(shops_page.items).data
        return {
            'start': start,
            'count': count,
            'total': shops_page.total,
            'shops': shops
        }

    @use_args({
        'name': fields.String(required=True, location='json'),
        'format': fields.Str(location='query', validate=validate.Equal('json'))
    })
    def post(self, args):
        new_shop = Shop(name=args['name'])
        db.session.add(new_shop)
        db.session.commit()
        return ShopsResource.ShopSchema().dump(new_shop).data
